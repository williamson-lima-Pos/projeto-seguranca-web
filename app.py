from datetime import timedelta
from functools import wraps
import hmac
import os
import re
import secrets
from flask import Flask, abort, flash, g, redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

# Configurações básicas da aplicação
# Em conformidade com Secure by Design, chaves e parâmetros sensíveis
# devem ser carregados a partir de variáveis de ambiente.
app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY", "dev-secret-key-change-in-production"
)

# Configuração do banco de dados SQLite local (sem caminhos absolutos)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "sqlite:///app.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Configurações de segurança dos cookies de sessão
# HTTPOnly impede que scripts no cliente (XSS) acessem o cookie de sessão
app.config["SESSION_COOKIE_HTTPONLY"] = True

# SameSite=Lax mitiga o envio inadvertido do cookie em requisições cross-site de terceiros
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

# Secure: False em ambiente local de desenvolvimento (HTTP) e True em produção (HTTPS)
app.config["SESSION_COOKIE_SECURE"] = os.environ.get("SESSION_COOKIE_SECURE", "0") == "1"

# Tempo de expiração padrão para sessões configuradas como permanentes (session.permanent = True)
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=30)

db = SQLAlchemy(app)


# Proteção contra CSRF nativa (Secure by Design)
def generate_csrf_token() -> str:
    """Gera ou recupera o token CSRF criptograficamente seguro na sessão."""
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_hex(32)
    return session["csrf_token"]


def validate_csrf_token(token: str | None) -> bool:
    """Valida o token CSRF recebido utilizando comparação em tempo constante."""
    stored_token = session.get("csrf_token")
    if not stored_token or not token:
        return False
    return hmac.compare_digest(stored_token, token)


@app.context_processor
def inject_csrf_token():
    """Disponibiliza a função csrf_token() para todos os templates Jinja2."""
    return dict(csrf_token=generate_csrf_token)


# Modelo de Usuário
class User(db.Model):
    """Modelo de usuário para autenticação e autorização."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    @staticmethod
    def validate_username(username: str) -> tuple[bool, str | None]:
        """Valida a política de nome de usuário no backend.

        Requisitos:
        - Mínimo de 3 caracteres;
        - Máximo de 30 caracteres;
        - Permitido apenas letras, números, sublinhado (_) e hífen (-).
        """
        if not isinstance(username, str) or not username:
            return False, "O nome de usuário é obrigatório."

        if len(username) < 3 or len(username) > 30:
            return False, "O nome de usuário deve ter entre 3 e 30 caracteres."

        if not re.match(r"^[a-zA-Z0-9_-]+$", username):
            return (
                False,
                "O nome de usuário deve conter apenas letras, números, sublinhado (_) e hífen (-).",
            )

        return True, None

    @staticmethod
    def validate_password(password: str) -> tuple[bool, str | None]:
        """Valida a política de senha de acordo com requisitos mínimos de segurança."""
        if not isinstance(password, str) or not password:
            return False, "A senha é obrigatória."

        if len(password) < 8:
            return False, "A senha deve possuir no mínimo 8 caracteres."

        if not any(c.islower() for c in password):
            return False, "A senha deve conter pelo menos uma letra minúscula."

        if not any(c.isupper() for c in password):
            return False, "A senha deve conter pelo menos uma letra maiúscula."

        if not any(c.isdigit() for c in password):
            return False, "A senha deve conter pelo menos um número."

        return True, None

    def set_password(self, password: str) -> None:
        """Valida a política de senha e armazena exclusivamente o hash criptográfico."""
        is_valid, error_message = self.validate_password(password)
        if not is_valid:
            raise ValueError(error_message)
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Verifica se a senha fornecida corresponde ao hash armazenado."""
        if not self.password_hash or not password:
            return False
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"


@app.before_request
def load_logged_in_user():
    """Carrega o usuário autenticado na requisição com base no user_id da sessão."""
    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
    else:
        g.user = db.session.get(User, user_id)
        # Se o usuário não for mais encontrado no banco, descarta a sessão obsoleta
        if g.user is None:
            session.clear()


def login_required(view):
    """Decorador para proteger rotas que exigem autenticação prévia."""

    @wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            flash("Acesso restrito. Faça login para continuar.", "error")
            return redirect(url_for("login"))
        return view(**kwargs)

    return wrapped_view


def admin_required(view):
    """Decorador para proteger rotas exclusivas para administradores.

    Requisitos de segurança:
    1. Exige autenticação prévia (redireciona para login se anônimo);
    2. Exige privilégio administrativo ativo verificado no banco (is_admin=True);
    3. Nega acesso com HTTP 403 Forbidden para usuários comuns autenticados.
    """

    @wraps(view)
    def wrapped_view(**kwargs):
        # 1. Usuário não autenticado: segue fluxo padrão de login
        if g.user is None:
            flash("Acesso restrito. Faça login para continuar.", "error")
            return redirect(url_for("login"))

        # 2. Usuário autenticado sem privilégio administrativo: nega acesso seguro
        if not g.user.is_admin:
            abort(403)

        # 3. Usuário autenticado e com privilégio administrativo
        return view(**kwargs)

    return wrapped_view


@app.after_request
def apply_security_headers(response):
    """Aplica cabeçalhos básicos de segurança nas respostas HTTP (Secure by Design)."""
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return response


@app.route("/")
def index():
    """Rota inicial para validação do funcionamento da aplicação."""
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Rota para cadastro de novos usuários com proteção CSRF e validações estritas."""
    if g.user is not None:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        # 1. Validação obrigatória do token CSRF em tempo constante
        csrf_token_received = request.form.get("csrf_token")
        if not validate_csrf_token(csrf_token_received):
            flash("Requisição inválida ou token de segurança expirado.", "error")
            return render_template("register.html"), 400

        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        # 2. Validação de preenchimento dos campos obrigatórios
        if not username or not password or not confirm_password:
            flash("Todos os campos são obrigatórios.", "error")
            return render_template("register.html", username=username), 400

        # 3. Validação da política de username no servidor
        is_valid_username, username_error = User.validate_username(username)
        if not is_valid_username:
            flash(username_error, "error")
            return render_template("register.html", username=username), 400

        # 4. Verificação de correspondência das senhas
        if password != confirm_password:
            flash("As senhas informadas não coincidem.", "error")
            return render_template("register.html", username=username), 400

        # 5. Consulta parametrizada por usuário existente (SQLAlchemy ORM)
        existing_user = db.session.execute(
            db.select(User).filter_by(username=username)
        ).scalar_one_or_none()

        if existing_user:
            flash("Nome de usuário indisponível.", "error")
            return render_template("register.html"), 400

        # 6. Instanciação segura com is_admin explicitamente False
        new_user = User(username=username, is_admin=False)

        # 7. Aplicação da política e geração do hash via modelo User
        try:
            new_user.set_password(password)
        except ValueError as e:
            flash(str(e), "error")
            return render_template("register.html", username=username), 400

        # 8. Persistência transacional com rollback preventivo
        try:
            db.session.add(new_user)
            db.session.commit()
            flash("Cadastro realizado com sucesso! Faça login para continuar.", "success")
            return redirect(url_for("login"))
        except Exception:
            db.session.rollback()
            flash("Ocorreu um erro ao processar o cadastro. Tente novamente.", "error")
            return render_template("register.html"), 500

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Rota para autenticação de usuários por username e senha com proteção CSRF."""
    # Redireciona usuários já autenticados para a área privada
    if g.user is not None:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        # 1. Validação obrigatória do token CSRF em tempo constante
        csrf_token_received = request.form.get("csrf_token")
        if not validate_csrf_token(csrf_token_received):
            flash("Requisição inválida ou token de segurança expirado.", "error")
            return render_template("login.html"), 400

        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        # 2. Validação básica de preenchimento dos campos obrigatórios
        if not username or not password:
            flash("Todos os campos são obrigatórios.", "error")
            return render_template("login.html", username=username), 400

        # 3. Consulta parametrizada por usuário existente (SQLAlchemy ORM)
        user = db.session.execute(
            db.select(User).filter_by(username=username)
        ).scalar_one_or_none()

        # 4. Verificação da senha utilizando o método check_password() do modelo.
        # Não reaplica a política de complexidade da senha durante o login.
        # Mensagem genérica para mitigar enumeração de contas (OWASP Authentication Cheat Sheet).
        if user is None or not user.check_password(password):
            flash("Usuário ou senha incorretos.", "error")
            return render_template("login.html", username=username), 401

        # 5. Eliminação do estado da sessão anterior antes de criar a sessão autenticada
        session.clear()

        # 6. Configuração explícita de sessão permanente com tempo de expiração configurado (30 min)
        session.permanent = True

        # 7. Armazenamento exclusivo do identificador essencial (nunca senha ou hash na sessão)
        session["user_id"] = user.id

        # 8. Geração de um novo token CSRF para o contexto da sessão autenticada
        session["csrf_token"] = secrets.token_hex(32)

        flash(f"Bem-vindo, {user.username}!", "success")
        return redirect(url_for("dashboard"))

    return render_template("login.html")


@app.route("/logout", methods=["POST"])
@login_required
def logout():
    """Rota para encerramento de sessão com proteção CSRF."""
    csrf_token_received = request.form.get("csrf_token")
    if not validate_csrf_token(csrf_token_received):
        flash("Requisição inválida ou token de segurança expirado.", "error")
        return redirect(url_for("login")), 400

    # Limpeza total da sessão do usuário
    session.clear()
    flash("Sessão encerrada com sucesso.", "success")
    return redirect(url_for("login"))


@app.route("/dashboard")
@login_required
def dashboard():
    """Área privada acessível exclusivamente por usuários autenticados."""
    return render_template("dashboard.html", user=g.user)


@app.route("/admin")
@admin_required
def admin():
    """Área administrativa restrita exclusivamente a administradores (RBAC)."""
    # Consulta via SQLAlchemy ORM; o ORM e o uso de consultas parametrizadas
    # mitigam injeção de SQL ao evitar concatenação direta de entradas em comandos SQL.
    users = db.session.execute(
        db.select(User).order_by(User.id.asc())
    ).scalars().all()

    return render_template("admin.html", users=users)


@app.route("/admin/users/<int:user_id>/promote", methods=["POST"])
@admin_required
def promote_user(user_id: int):
    """Promove um usuário comum para a função de administrador."""
    # 1. Validação obrigatória do token CSRF em tempo constante
    csrf_token_received = request.form.get("csrf_token")
    if not validate_csrf_token(csrf_token_received):
        flash("Requisição inválida ou token de segurança expirado.", "error")
        return redirect(url_for("admin"))

    # 2. Localização segura do usuário via ORM
    target_user = db.session.get(User, user_id)
    if target_user is None:
        flash("Usuário não encontrado.", "error")
        return redirect(url_for("admin"))

    # 3. Verificação de estado redundante
    if target_user.is_admin:
        flash(f"O usuário '{target_user.username}' já é um administrador.", "error")
        return redirect(url_for("admin"))

    # 4. Alteração estrita do privilégio exclusivamente pelo backend
    target_user.is_admin = True
    try:
        db.session.commit()
        flash(
            f"Usuário '{target_user.username}' promovido a administrador com sucesso.",
            "success",
        )
    except Exception:
        db.session.rollback()
        flash("Erro ao atualizar privilégios do usuário. Tente novamente.", "error")

    return redirect(url_for("admin"))


@app.route("/admin/users/<int:user_id>/demote", methods=["POST"])
@admin_required
def demote_user(user_id: int):
    """Revoga o privilégio administrativo de um administrador (exceto o próprio)."""
    # 1. Validação obrigatória do token CSRF em tempo constante
    csrf_token_received = request.form.get("csrf_token")
    if not validate_csrf_token(csrf_token_received):
        flash("Requisição inválida ou token de segurança expirado.", "error")
        return redirect(url_for("admin"))

    # 2. Localização segura do usuário via ORM
    target_user = db.session.get(User, user_id)
    if target_user is None:
        flash("Usuário não encontrado.", "error")
        return redirect(url_for("admin"))

    # 3. Proteção contra auto-revogação (impede bloqueio do administrador ativo)
    if target_user.id == g.user.id:
        flash(
            "Operação negada: você não pode remover seu próprio privilégio de administrador.",
            "error",
        )
        return redirect(url_for("admin"))

    # 4. Verificação de estado redundante
    if not target_user.is_admin:
        flash(
            f"O usuário '{target_user.username}' não possui privilégios de administrador.",
            "error",
        )
        return redirect(url_for("admin"))

    # 5. Alteração estrita do privilégio exclusivamente pelo backend
    target_user.is_admin = False
    try:
        db.session.commit()
        flash(
            f"Privilégio de administrador revogado para '{target_user.username}'.",
            "success",
        )
    except Exception:
        db.session.rollback()
        flash("Erro ao atualizar privilégios do usuário. Tente novamente.", "error")

    return redirect(url_for("admin"))




if __name__ == "__main__":
    # Modo debug desligado por padrão para evitar vazamento de informações sensíveis (OWASP)
    debug_mode = os.environ.get("FLASK_DEBUG", "0") == "1"
    app.run(host="127.0.0.1", port=5000, debug=debug_mode)
