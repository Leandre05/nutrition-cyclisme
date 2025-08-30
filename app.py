import streamlit as st
import streamlit_authenticator as stauth

# -------------------------------------------------
# CONFIG DE LA PAGE
# -------------------------------------------------
st.set_page_config(page_title="Nutrition Cyclisme", page_icon="🚴", layout="wide")

# -------------------------------------------------
# LIRE LES SECRETS ET LES CONVERTIR EN DICTS MUTABLES
# (évite l'erreur 'Secrets does not support item assignment')
# -------------------------------------------------
# Secrets attendus :
# [credentials.usernames.<username>]
# name="...", email="...", password="$2b$..."
# [cookie] name="...", key="...", expiry_days=30

users_ss = st.secrets["credentials"]["usernames"]
credentials = {
    "usernames": {
        u: {
            "name": info["name"],
            "email": info["email"],
            "password": info["password"],  # hash bcrypt ($2b$...)
        }
        for u, info in users_ss.items()
    }
}

cookie_ss = st.secrets["cookie"]
cookie_name = cookie_ss["name"]
cookie_key = cookie_ss["key"]
cookie_days = int(cookie_ss["expiry_days"])

# -------------------------------------------------
# INITIALISER AUTHENTICATOR
# (compat 0.3.x et 0.4+)
# -------------------------------------------------
try:
    # Signature ancienne (0.3.x) : positionnels
    authenticator = stauth.Authenticate(credentials, cookie_name, cookie_key, cookie_days)
except TypeError:
    # Signature récente (0.4+) : mots-clés
    authenticator = stauth.Authenticate(
        credentials=credentials,
        cookie_name=cookie_name,
        key=cookie_key,
        cookie_expiry_days=cookie_days,
    )

# -------------------------------------------------
# LOGIN (compat nouvelles & anciennes versions)
# -------------------------------------------------
try:
    # Nouvelle API (>=0.4) : uniquement location=
    name, auth_status, username = authenticator.login(location="main")
except TypeError:
    # Ancienne API (<=0.3.x) : (form_name, location)
    name, auth_status, username = authenticator.login("Connexion", "main")

# ÉTAT DE CONNEXION
if auth_status is False:
    st.error("Identifiants incorrects.")
    st.stop()
elif auth_status is None:
    st.info("Merci de vous connecter pour accéder à l’application.")
    st.stop()

# -------------------------------------------------
# CONTENU (UTILISATEUR CONNECTÉ)
# -------------------------------------------------
with st.sidebar:
    st.success(f"Connecté : {name}")
    try:
        authenticator.logout(button_name="Se déconnecter", location="sidebar")
    except TypeError:
        authenticator.logout("Se déconnecter", "sidebar")

st.title("Interface Nutrition Cyclisme")
st.write("Contenu protégé… (colle ensuite ton app ici)")


