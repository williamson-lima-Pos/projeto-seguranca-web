import os
from flask import Flask, render_template

app = Flask(__name__)

# Configurações básicas da aplicação
# Em conformidade com Secure by Design, chaves e parâmetros sensíveis
# devem ser carregados a partir de variáveis de ambiente.
app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY", "dev-secret-key-change-in-production"
)


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
