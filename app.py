import streamlit as st
import streamlit_authenticator as stauth

st.set_page_config(page_title="Nutrition Cyclisme", page_icon="🚴", layout="wide")

# -------- Convertir st.secrets -> vrais dicts (mutables) --------
# Utilisateurs
users_ss = st.secrets["credentials"]["usernames"]
credentials = {
    "usernames": {
        username: {
            "name": info["name"],
            "email": info["email"],
            "password": info["password"],  # hash bcrypt commençant par $2b$
        }
        for username, info in users_ss.items()
    }
}

# Cookie
cookie_ss = st.secrets["cookie"]
cookie_name = cookie_ss["name"]
cookie_key = cookie_ss["key"]
cookie_days = int(cookie_ss["expiry_days"])

# -------- Initialiser l'auth --------
# (Pas de st.secrets passés directement)
authenticator = stauth.Authenticate(
    credentials=credentials,
    cookie_name=cookie_name,
    key=cookie_key,
    cookie_expiry_days=cookie_days,
)

name, auth_status, username = authenticator.login("Connexion", "main")

if auth_status is False:
    st.error("Identifiants incorrects.")
    st.stop()
elif auth_status is None:
    st.info("Merci de vous connecter pour accéder à l’application.")
    st.stop()

with st.sidebar:
    st.success(f"Connecté : {name}")
    authenticator.logout("Se déconnecter", "sidebar")

st.title("Interface Nutrition Cyclisme")
st.write("Contenu protégé… (colle ton app ici)")
