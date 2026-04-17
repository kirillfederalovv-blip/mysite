from flask import Flask, request, redirect, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = "secret123"

# список банов
banned_ips = []

# логирование
def log(ip, path):
    with open("logs.txt", "a") as f:
        f.write(f"{datetime.now()} | {ip} | {path}\n")

# проверка бана
@app.before_request
def check_ip():
    ip = request.remote_addr
    if ip in banned_ips:
        return "Ты забанен 😈", 403

# главная
@app.route("/")
def home():
    ip = request.remote_addr
    log(ip, "/")
    return f"""
    <h1>Главная страница</h1>
    <p>Твой IP: {ip}</p>
    <a href='/admin'>Админка</a>
    """

# админ логин
@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        if request.form["password"] == "admin123":
            session["admin"] = True
            return redirect("/panel")
    return """
    <form method="post">
        <input type="password" name="password" placeholder="Пароль">
        <button>Войти</button>
    </form>
    """

# панель
@app.route("/panel")
def panel():
    if not session.get("admin"):
        return redirect("/admin")

    with open("logs.txt", "r") as f:
        logs = f.read()

    return f"""
    <h1>Админ панель</h1>
    <pre>{logs}</pre>

    <form method="post" action="/ban">
        <input name="ip" placeholder="IP для бана">
        <button>Забанить</button>
    </form>
    """

# бан IP
@app.route("/ban", methods=["POST"])
def ban():
    if not session.get("admin"):
        return redirect("/admin")

    ip = request.form["ip"]
    banned_ips.append(ip)
    return f"IP {ip} забанен <br><a href='/panel'>Назад</a>"

if __name__ == "__main__":
    app.run()