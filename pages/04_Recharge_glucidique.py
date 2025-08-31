import streamlit as st
import streamlit_authenticator as stauth

# --- Auth header (compatible toutes versions) ---
users_ss = st.secrets["credentials"]["usernames"]
credentials = {"usernames": {u: {"name": i["name"], "email": i["email"], "password": i["password"]}
                             for u, i in users_ss.items()}}
c = st.secrets["cookie"]
cookie_name, cookie_key, cookie_days = c["name"], c["key"], int(c["expiry_days"])

# Instanciation compat (0.3.x et 0.4+)
try:
    authenticator = stauth.Authenticate(credentials, cookie_name, cookie_key, cookie_days)
except TypeError:
    authenticator = stauth.Authenticate(
        credentials=credentials,
        cookie_name=cookie_name,
        key=cookie_key,
        cookie_expiry_days=cookie_days,
    )

# Login compat (0.3.x et 0.4+)
try:
    name, auth_status, username = authenticator.login(location="main")
except TypeError:
    name, auth_status, username = authenticator.login("Connexion", "main")

if not auth_status:
    st.stop()

# (facultatif) bouton logout cohérent
with st.sidebar:
    st.success(f"Connecté : {name}")
    try:
        authenticator.logout(button_name="Se déconnecter", location="sidebar")
    except TypeError:
        authenticator.logout("Se déconnecter", "sidebar")

import streamlit as st

st.set_page_config(page_title="Recharge glucidique", layout="centered")

st.title("🍝 Recharge glucidique")
poids = st.number_input("Poids du cycliste (kg)", min_value=30.0, max_value=100.0, step=0.5)

st.header("📅 Recharge les jours avant la course")

type_course = st.selectbox("Type de course", [
    "Course < 90 min ou chrono sans autre course",
    "Course > 90 min"
])

if type_course == "Course < 90 min ou chrono sans autre course":
    min_g = 7 * poids
    max_g = 12 * poids
    st.markdown(f"➡️ **Objectif : entre 7 et 12 g/kg sur 24h**")
    st.markdown(f"👉 Soit **entre {min_g:.0f} et {max_g:.0f} g** de glucides à répartir la veille de la course.")
else:
    min_g = 10 * poids
    max_g = 12 * poids
    st.markdown("➡️ **Objectif : entre 10 et 12 g/kg sur 24h** à répartir entre J–2 et J–1 (36 à 48h avant la course).")
    st.markdown(f"👉 Soit **entre {min_g:.0f} et {max_g:.0f} g** de glucides.")

st.divider()

st.header("⏰ Juste avant la course")

repas_min = 2 * poids
repas_max = 4 * poids
collation = 0.5 * poids

st.markdown("➡️ **Repas pré-course (2 à 3 h avant)** : 2 à 4 g/kg")
st.markdown(f"👉 Soit **entre {repas_min:.0f} et {repas_max:.0f} g** de glucides")

st.markdown("➡️ **Collation juste avant la course** : 0,5 g/kg")
st.markdown(f"👉 Soit **{collation:.0f} g** de glucides")

st.divider()

st.header("🔁 Après la course")

suite = st.radio("Y a-t-il une autre course dans la journée ?", ["Oui", "Non"])

if suite == "Oui":
    min_post = 1.0 * poids * 4
    max_post = 1.2 * poids * 4
    st.markdown("➡️ **Objectif : 1 à 1,2 g/kg/h pendant 4 h après l’effort**")
    st.markdown(f"👉 Soit **entre {min_post:.0f} et {max_post:.0f} g** de glucides (en 4 h)")
else:
    recup = 3 * poids
    st.markdown("➡️ **Objectif : 3 g/kg immédiatement après l’effort**")
    st.markdown(f"👉 Soit **{recup:.0f} g** de glucides")

st.divider()

st.header("🌙 Repas du soir")

repas_soir = 3 * poids
st.markdown("➡️ **Objectif : 3 g/kg pour le dîner**")
st.markdown(f"👉 Soit **{repas_soir:.0f} g** de glucides")


