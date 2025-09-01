import streamlit as st
import streamlit_authenticator as stauth
from pathlib import Path

# -------------------------------------------------
# CONFIG DE LA PAGE
# -------------------------------------------------
st.set_page_config(page_title="Nutrition Cyclisme", page_icon="🚴", layout="wide")

# Helper chemin vers /assets
def asset_path(filename: str) -> Path:
    """Chemin robuste vers /assets depuis app.py ou une page /pages/*."""
    here = Path(__file__).resolve()
    root = here.parents[1] if here.parent.name == "pages" else here.parent
    return root / "assets" / filename

# Logo dans la barre latérale (visible tout le temps)
with st.sidebar:
    logo_sidebar = asset_path("logohg.png")  # <-- nom EXACT du fichier dans /assets
    if logo_sidebar.exists():
        st.image(str(logo_sidebar), width=140)

# -------------------------------------------------
# LIRE LES SECRETS ET LES CONVERTIR EN DICTS MUTABLES
# -------------------------------------------------
# Secrets attendus :
# [credentials.usernames.<username>]
# name="...", email="(optionnel)", password="$2b$..."
# [cookie] name="...", key="...", expiry_days=30
users_ss = st.secrets["credentials"]["usernames"]
credentials = {
    "usernames": {
        u: {
            "name": info.get("name", u),
            "email": info.get("email", ""),        # email optionnel
            "password": info["password"],          # hash bcrypt ($2b$...)
        }
        for u, info in users_ss.items()
    }
}

cookie_ss = st.secrets["cookie"]
cookie_name = cookie_ss["name"]
cookie_key = cookie_ss["key"]
cookie_days = int(cookie_ss["expiry_days"])

# -------------------------------------------------
# INITIALISER AUTHENTICATOR (compat 0.3.x et 0.4+)
# -------------------------------------------------
try:
    # Signature ancienne (0.3.x) : arguments positionnels
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

# --- Accueil ---
logo_center = asset_path("logohg.png")  # <-- nom EXACT du fichier
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if logo_center.exists():
        st.image(str(logo_center), width=260,
                 caption="Comité Haute-Garonne de Cyclisme", use_container_width=False)
    else:
        st.warning("Logo introuvable : vérifie assets/logohg.png")

st.title("Comité Haute-Garonne de Cyclisme — Nutrition")
st.markdown("""
Bienvenue sur l’outil créé par le **Comité Haute-Garonne de Cyclisme**.

**Objectif du site**  
Aider les cyclistes à **bien aborder la nutrition pendant l’effort** (boissons, gels, barres, rice cakes) et à **préparer l’alimentation en vue d’un objectif**, en s’appuyant sur les recommandations scientifiques actuelles.

**Navigation**  
Utilise le menu à gauche pour accéder aux calculateurs et fiches :
- *Nutrition entraînement* : apports glucidiques et hydratation selon la durée et l’intensité.
- *Nutrition course* : stratégies d’apport pour la compétition.
- *Recharge glucidique* : protocoles de chargement avant l’épreuve.
- *Recettes* : idées pratiques (rice cakes, boissons, etc.).
""")
st.divider()
st.caption("Ce site a une visée pédagogique et ne remplace pas un avis médical ou diététique personnalisé.")




