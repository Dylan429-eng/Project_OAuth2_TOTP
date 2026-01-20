from flask import Flask, request
import pyotp, qrcode, sqlite3, os
BASE_STYLE = """
<style>
    body {
        font-family: Arial, sans-serif;
        background: #f4f6f9;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
    }

    .container {
        background: white;
        padding: 30px;
        width: 380px;
        border-radius: 10px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        text-align: center;
    }

    h2, h3 {
        margin-bottom: 20px;
        color: #2c3e50;
    }

    input {
        width: 100%;
        padding: 10px;
        margin: 10px 0;
        border-radius: 6px;
        border: 1px solid #ccc;
        font-size: 14px;
    }

    button {
        background: #2c7be5;
        color: white;
        border: none;
        padding: 10px;
        width: 100%;
        border-radius: 6px;
        font-size: 15px;
        cursor: pointer;
        margin-top: 10px;
    }

    button:hover {
        background: #1a5fd0;
    }

    a {
        display: block;
        margin-top: 15px;
        text-decoration: none;
        color: #2c7be5;
        font-size: 14px;
    }

    img {
        margin-top: 15px;
        width: 200px;
    }

    .success {
        color: green;
        font-weight: bold;
    }

    .error {
        color: red;
        font-weight: bold;
    }
</style>
"""

app = Flask(__name__)

DB_NAME = "users.db"
QR_DIR = "static/qrcodes"

# ---- DATABASE ----
def get_db():
    conn = sqlite3.connect(DB_NAME, timeout=10)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT,
            secret TEXT
        )
    """)
    return conn

# ---- HOME ----
@app.route("/")
def home():
    return BASE_STYLE + """
    <div class="container">
        <h2>🔐 MFA Demo</h2>
        <p>Authentification multi-facteurs avec OTP</p>
        <a href="/register">➡ S'inscrire</a>
        <a href="/login">➡ Se connecter</a>
    </div>
    """
# ---- REGISTER ----
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user = request.form["username"]
        pwd = request.form["password"]

        secret = pyotp.random_base32()

        conn = get_db()
        try:
            conn.execute(
                "INSERT INTO users VALUES (?, ?, ?)",
                (user, pwd, secret)
            )
            conn.commit()
        except sqlite3.IntegrityError:
            return "Utilisateur déjà existant"
        finally:
            conn.close()  # 
        uri = pyotp.totp.TOTP(secret).provisioning_uri(
            name=user,
            issuer_name="MFA-DEMO"
        )

        img = qrcode.make(uri)
        qr_path = f"{QR_DIR}/{user}.png"
        img.save(qr_path)

        return BASE_STYLE + f"""
<div class="container">
    <h3>Compte créé ✅</h3>
    <p>Scanne ce QR code avec Google Authenticator</p>
    <img src='/{qr_path}'>
    <a href="/login">➡ Connexion MFA</a>
</div>
"""

    return BASE_STYLE + """
<div class="container">
    <h3>Inscription</h3>
    <form method="post">
        <input name="username" placeholder="Nom d'utilisateur" required>
        <input type="password" name="password" placeholder="Mot de passe" required>
        <button>S'inscrire</button>
    </form>
    <a href="/">⬅ Retour</a>
</div>
"""

# ---- LOGIN ----
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["username"]
        pwd = request.form["password"]
        otp = request.form["otp"]

        conn = get_db()
        row = conn.execute(
            "SELECT secret FROM users WHERE username=? AND password=?",
            (user, pwd)
        ).fetchone()
        conn.close()

        if not row:
            return BASE_STYLE + """
            <div class="container">
                <h3 class="error">Identifiants incorrects ❌</h3>
                <a href="/login">Réessayer</a>
            </div>
            """

        totp = pyotp.TOTP(row[0])
        if totp.verify(otp):
            return BASE_STYLE + """
            <div class="container">
                <h3 class="success">Authentification réussie ✅</h3>
                <p>Accès sécurisé accordé</p>
            </div>
            """
        else:
            return BASE_STYLE + """
            <div class="container">
                <h3 class="error">OTP invalide ❌</h3>
                <a href="/login">Réessayer</a>
            </div>
            """

    # GET (AFFICHAGE DU FORMULAIRE)
    return BASE_STYLE + """
    <div class="container">
        <h3>Connexion MFA</h3>
        <form method="post">
            <input name="username" placeholder="Nom d'utilisateur" required>
            <input type="password" name="password" placeholder="Mot de passe" required>
            <input name="otp" placeholder="Code OTP" required>
            <button>Se connecter</button>
        </form>
        <a href="/">⬅ Retour</a>
    </div>
    """

if __name__ == "__main__":
    app.run(debug=True)
