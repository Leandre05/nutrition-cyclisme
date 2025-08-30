import streamlit as st
import streamlit_authenticator as stauth

st.set_page_config(page_title="Nutrition Cyclisme", page_icon="🚴", layout="wide")

# -- secrets -> dicts mutables
users_ss = st.secrets["credentials"]["usernames"]
credentials = {
    "usernames": {
        u: {"name": info["name"], "email": info["email"], "password": info["password"]}
        for u, info in users_ss.items()
    }
}
cookie_ss = st.secrets["cookie"]
cookie_name = cookie_ss["name"]
cookie_key = cookie_ss["key"]
cookie_days = int(cookie_ss["expiry_days"])

# -- IMPORTANT : appel en arguments positionnels (compat 0.3.2)
authenticator = stauth.Authenticate(credentials, cookie_name, cookie_key, cookie_days)

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
st.write("Contenu protégé… (colle ensuite ton app ici)")

