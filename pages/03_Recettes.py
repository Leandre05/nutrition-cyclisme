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


# 👉 Colle ici le code de la page Entraînement (calcul gels/boissons…)

import streamlit as st

st.title("🍚 Recettes d'aliments faits maison")

with st.expander("🍙 Rice Cake maison (version riz rond)"):
    st.markdown("""
    **Ingrédients :**
    - 250 g de riz rond (type riz à risotto)  
    - 500 mL d'eau  
    - 100 g de sucre  
    - 1 pincée de sel  

    **Préparation :**
    1. Laver le riz à l'eau claire.  
    2. Mettre le riz et l'eau ensemble dans une casserole **à froid**.  
    3. Porter le mélange à ébullition.  
    4. Une fois l'ébullition atteinte, ajouter le sucre et le sel.  
    5. Couvrir et laisser cuire à feu doux pendant **20 minutes**.  
    6. En fin de cuisson, vous pouvez ajouter un **topping** au choix :  
       - pâte de spéculoos  
       - chocolat  
       - caramel  
       ⚠️ Évitez d'en mettre trop pour **limiter les graisses**.  
    7. Verser dans un plat tapissé de film plastique.  
    8. Recouvrir la surface avec du film plastique et laisser **reposer toute une nuit au réfrigérateur**.  

    **Découpe :**
    - Couper en **16 parts**.

    ---

    🍏 **Informations nutritionnelles (par portion)** :  
    - Environ **20 g de glucides**  
    - Très faible en matières grasses (hors topping)

    - Tu peux remplacer les 100g de sucre par 100g de fructose et tu obtiendras des portion avec un ratio de 1.08 avec 13g de glucose et 7g de fructose   

    📦 **Conservation :**  
    - Se conserve **3 à 4 jours** au réfrigérateur  
    """)


with st.expander("🍫 Rice Crispy Bar maison"):
    st.markdown("""
    **Ingrédients :**
    - 60 g de beurre ou huile de coco  
    - 300 g de marshmallows  
    - 200 g de Rice Krispies  

    **Préparation :**
    1. Tapisser un moule avec du papier cuisson.  
    2. Faire fondre le beurre à feu doux dans une grande casserole.  
    3. Ajouter les marshmallows et continuer à faire fondre.  
       *Si vous utilisez de gros marshmallows, les couper en morceaux facilite la fonte.*  
    4. Une fois presque fondu, retirer du feu et continuer à mélanger.  
    5. Ajouter les Rice Krispies et bien enrober.  
       *Utiliser un feu doux et retirer avant d’ajouter les céréales évite une texture caoutchouteuse.*  
    6. Presser uniformément dans le moule.  
       *Utiliser une spatule légèrement beurrée ou mouillée pour éviter que ça colle.*  
    7. Laisser refroidir complètement avant de découper en portions.  

    ---

    🍏 **Informations nutritionnelles** *(pour une portion si coupée en 15 parts)* :  
    - Calories : **158 kcal**  
    - Glucides : **30 g**  
    - Protéines : **2 g**  
    - Lipides : **3 g**
    """)
