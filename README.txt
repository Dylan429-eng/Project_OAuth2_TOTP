#  MFA Demo – Authentification Multi-Facteurs avec OTP

##  Description
Ce projet est une application web pédagogique démontrant la mise en œuvre d’une
**authentification multi-facteurs (MFA)** basée sur :
- un **mot de passe** (facteur de connaissance),
- un **code OTP temporel (TOTP)** généré par une application mobile
  comme Google Authenticator (facteur de possession).

Le projet illustre les concepts de **contrôle d’accès**, **secret partagé** et
**authentification forte**, conformément aux standards de sécurité actuels.

---

## 🧠 Concepts de sécurité abordés
- Authentification multi-facteurs (MFA)
- TOTP (Time-based One-Time Password – RFC 6238)
- Secret partagé
- Protection contre les attaques par rejeu
- Enrôlement via QR code

---

## ⚙️ Prérequis

- Python **3.8+**
- pip
- virtualenv (recommandé)
- Une application OTP :
  - Google Authenticator
  - Microsoft Authenticator
  - FreeOTP

---

##  Installation

### Cloner le dépôt

git clone https://github.com/Dylan429-eng/Project_OAuth2_TOTP.git
cd mfa-demo
## Créer un environnement virtuel
python -m venv venv
#Activer l’environnement virtuel
source venv/bin/activate
#Installer les dépendances
pip install -r requirements.txt
#Lancement de l'application
python app2.py
