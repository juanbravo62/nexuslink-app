from flask import Flask, render_template, request, redirect, url_for, session
import json
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "nexuslink_secret")

# arquivo de usuários
USUARIOS_FILE = "usuarios.json"

def carregar_usuarios():
    try:
        with open(USUARIOS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# LOGIN
@app.route("/", methods=["GET", "POST"])
def login():
    erro = None
    if request.method == "POST":
        user = request.form.get("usuario")
        senha = request.form.get("senha")

        usuarios = carregar_usuarios()
        encontrado = False
        for u in usuarios:
            if u["usuario"] == user and u["senha"] == senha:
                encontrado = True
                break

        if encontrado:
            session["logado"] = True
            return redirect(url_for("app_nexus"))
        else:
            erro = "Login inválido"

    return render_template("login.html", erro=erro)

# FERRAMENTA (GERADOR)
@app.route("/app", methods=["GET", "POST"])
def app_nexus():
    if not session.get("logado"):
        return redirect(url_for("login"))

    texto = ""
    if request.method == "POST":
        produto = request.form["produto"]
        loja = request.form["loja"]
        preco_normal = request.form["preco_normal"]
        preco_promocional = request.form["preco_promocional"]
        link = request.form["link"]

        if not preco_normal.startswith("R$"):
            preco_normal = f"R$ {preco_normal}"
        if not preco_promocional.startswith("R$"):
            preco_promocional = f"R$ {preco_promocional}"

        try:
            p1 = float(preco_normal.replace("R$", "").replace(",", ".").strip())
            p2 = float(preco_promocional.replace("R$", "").replace(",", ".").strip())
            desconto = int(((p1 - p2) / p1) * 100)
        except:
            desconto = 0

        texto = f"""🔥 OFERTA IMPERDÍVEL 🔥

🛍 Produto: {produto}
🏪 Loja: {loja}

💸 De: {preco_normal}
🔥 Por: {preco_promocional}

🎯 Desconto: {desconto}% OFF

⚡ Aproveite agora:
{link}

🚀 Corre que pode acabar!
"""

    return render_template("index.html", texto=texto)

# LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
