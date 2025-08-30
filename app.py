import streamlit as st
import streamlit_authenticator as stauth

st.set_page_config(page_title="Nutrition Cyclisme", page_icon="🚴", layout="wide")

# --- Auth ---
credentials = st.secrets["credentials"]
cookie = st.secrets["cookie"]

authenticator = stauth.Authenticate(
    credentials,          # dict: usernames -> {name, email, password}
    cookie["name"],       # nom du cookie
    cookie["key"],        # clé secrète du cookie (longue !)
    cookie["expiry_days"] # durée de validité
)

name, auth_status, username = authenticator.login("Connexion", "main")

if auth_status is False:
    st.error("Identifiants incorrects.")
    st.stop()
elif auth_status is None:
    st.info("Merci de vous connecter pour accéder à l’application.")
    st.stop()

# --- App (utilisateur connecté) ---
with st.sidebar:
    st.success(f"Connecté : {name}")
    authenticator.logout("Se déconnecter", "sidebar")

st.title("Interface Nutrition Cyclisme")
st.write("Contenu protégé…")
# 👉 Ici, colle ensuite TON code Streamlit existant (onglets, calculs, etc.)
