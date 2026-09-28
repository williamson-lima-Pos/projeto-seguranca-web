import os
from flask import Flask, render_template
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

db = SQLAlchemy(app)


# Modelo de Usuário
class User(db.Model):
    """Modelo de usuário para autenticação e autorização."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

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


if __name__ == "__main__":
    # Modo debug desligado por padrão para evitar vazamento de informações sensíveis (OWASP)
    debug_mode = os.environ.get("FLASK_DEBUG", "0") == "1"
    app.run(host="127.0.0.1", port=5000, debug=debug_mode)
