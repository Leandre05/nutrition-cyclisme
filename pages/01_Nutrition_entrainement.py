import streamlit as st, streamlit_authenticator as stauth

# --- Auth (même logique que dans app.py) ---
users_ss = st.secrets["credentials"]["usernames"]
credentials = {"usernames": {u: {"name": i["name"], "email": i["email"], "password": i["password"]} for u,i in users_ss.items()}}
c = st.secrets["cookie"]
authenticator = stauth.Authenticate(credentials, c["name"], c["key"], int(c["expiry_days"]))
name, auth_status, username = authenticator.login("Connexion", "main")
if not auth_status: st.stop()

st.title("Nutrition — Entraînement")
# 👉 Colle ici le code de la page Entraînement (calcul gels/boissons…)
