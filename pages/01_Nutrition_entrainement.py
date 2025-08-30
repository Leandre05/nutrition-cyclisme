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


st.title("Nutrition — Entraînement")
# 👉 Colle ici le code de la page Entraînement (calcul gels/boissons…)

import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Calcul nutrition", layout="centered")

st.title("🧪 Calcul des besoins en fonction de ton entrainement")

# Durée de l'entraînement
duree_entrainement = st.slider("⏱️ Durée totale de l'entraînement (en heures)", 1.0, 6.0, 3.0, step=0.25)

# Intensités spécifiques
st.subheader("🎯 Durée des intensités (en minutes)")
z6 = st.number_input("Zone 6/5 (VO2 max)", min_value=0, step=1)
z4 = st.number_input("Zone 4 (Seuil)", min_value=0, step=1)
z3 = st.number_input("Zone 3 (Tempo)", min_value=0, step=1)

# === Fonctions ===
def calcul_apport_glucides(duree_h, z6_min, z4_min, z3_min):
    if duree_h <= 1.5:
        base = 20
    elif duree_h >= 6:
        base = 120
    else:
        base = 20 + (duree_h - 1.5) * (100 / 4.5)
    glucides_base_totaux = base * duree_h
    ajout = z6_min * 2 + z4_min * 1 + z3_min * 0.5
    total = glucides_base_totaux + ajout
    total_par_heure = total / duree_h
    if total_par_heure > 120:
        total_par_heure = 120
        total = 120 * duree_h
    return round(total), round(total_par_heure)

def get_ratio_info(glucides_par_heure, total_glucides):
    if glucides_par_heure <= 50:
        ratio = (1, 0)
    elif glucides_par_heure <= 70:
        ratio = (1, 0.5)
    elif glucides_par_heure <= 100:
        ratio = (1, 0.8)
    else:
        ratio = (1, 1)
    glucose_fraction = 1 / (1 + ratio[1])
    fructose_fraction = ratio[1] / (1 + ratio[1])
    glucose_total = round(total_glucides * glucose_fraction)
    fructose_total = round(total_glucides * fructose_fraction)
    return ratio, glucose_total, fructose_total

def recommander_boisson(glucides_par_heure, ratio):
    boisson_ml = 500
    glucides_boisson = glucides_par_heure if glucides_par_heure < 50 else 40
    if ratio[1] == 0:
        glucose = round(glucides_boisson)
        fructose = 0
        type_boisson = "💧 Eau + glucose (dextrose ou maltodextrine)"
    else:
        glucose_fraction = 1 / (1 + ratio[1])
        fructose_fraction = ratio[1] / (1 + ratio[1])
        glucose = round(glucides_boisson * glucose_fraction)
        fructose = round(glucides_boisson * fructose_fraction)
        type_boisson = "💧 Eau + glucose + fructose (respect du ratio)"
    return type_boisson, boisson_ml, glucose, fructose, glucides_boisson

# === Calculs ===
glucides_totaux, glucides_par_heure = calcul_apport_glucides(duree_entrainement, z6, z4, z3)
ratio, glucose_g, fructose_g = get_ratio_info(glucides_par_heure, glucides_totaux)
type_boisson, volume_ml, glucose_bois, fructose_bois, glucides_boisson = recommander_boisson(glucides_par_heure, ratio)

# === Affichage des résultats ===
st.success(f"Apport total recommandé : {glucides_totaux} g de glucides")
st.info(f"Soit environ {glucides_par_heure} g/h")

st.subheader("🔬 Recommandation de répartition Glucose / Fructose")
st.write(f"✅ Ratio recommandé : **{ratio[0]} / {ratio[1]}**")
st.write(f"Quantité de glucose (ou dextrose ou maltodextrine) : **{glucose_g} g**")
st.write(f"Quantité de fructose : **{fructose_g} g**")

st.subheader("🚰 Recommandation de boisson par heure")
st.markdown(f"""
> **Si utilisation de boisson d'effort :**  
> Boire **{volume_ml} mL/h**  
> Glucides : **{glucides_boisson} g/h**  
> Glucose : **{glucose_bois} g**  
> Fructose : **{fructose_bois} g**
""")

# === Fonction jauge ===
def afficher_jauge_panier(valeur, cible_min, cible_max, valeur_max=None):
    if valeur_max is None:
        valeur_max = cible_max + 20
    fig, ax = plt.subplots(figsize=(6, 1.2))
    ax.set_xlim(0, valeur_max)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.axvspan(0, cible_min, color="#f4cccc", alpha=0.6)
    ax.axvspan(cible_min, cible_max, color="#d9ead3", alpha=0.7)
    ax.axvspan(cible_max, valeur_max, color="#fce5cd", alpha=0.6)
    ax.plot([valeur, valeur], [0, 1], color="black", linewidth=3)
    ax.text(valeur, 1.05, f"{round(valeur)} g/h", ha="center", fontsize=10)
    ax.text((cible_min + cible_max)/2, -0.1, f"Zone cible : {round(cible_min)}–{round(cible_max)} g/h", ha="center", fontsize=9, color="green")
    st.pyplot(fig)

# === Panier interactif ===
with st.expander("🧺 Construis ton panier nutritionnel (par heure)"):
    objectif_min = glucides_par_heure - 3
    objectif_max = glucides_par_heure + 3

    produits_disponibles = {
        "Rice Cake (20g sans fructose)": {"glucose": 20, "fructose": 0},
        "Rice Cake (20g avec frcutose)": {"glucose": 13, "fructose": 7},
        "Rice Crispy Bar (30g)": {"glucose": 30, "fructose": 0},
        "Gel 25g (1/0)": {"glucose": 25, "fructose": 0},
        "Gel 30g (1/0)": {"glucose": 30, "fructose": 0},
        "Gel 30g (1/0.8)": {"glucose": 17, "fructose": 13},
        "Gel 35g (1/0)": {"glucose": 35, "fructose": 0},
        "Gel 35g (1/0.8)": {"glucose": 19, "fructose": 16},
        "Gel 40g (1/0)": {"glucose": 40, "fructose": 0},
        "Gel 40g (1/0.8)": {"glucose": 22, "fructose": 18},
        "Gel 45g (1/0)": {"glucose": 45, "fructose": 0},
        "Gel 45g (1/0.8)": {"glucose": 25, "fructose": 20},
    }

    panier = {}
    for nom, data in produits_disponibles.items():
        quantite = st.number_input(f"{nom} - nombre par heure :", min_value=0, step=1, key=nom)
        panier[nom] = {
            "quantite": quantite,
            "glucose": data["glucose"] * quantite,
            "fructose": data["fructose"] * quantite,
        }

    # Total (solides + boisson)
    total_glucose = sum([item["glucose"] for item in panier.values()]) + glucose_bois
    total_fructose = sum([item["fructose"] for item in panier.values()]) + fructose_bois
    total_g = total_glucose + total_fructose

    # Affichage
    st.markdown("### 📊 Résumé du panier (solides + boisson)")
    st.write(f"Glucose total : **{total_glucose} g**")
    st.write(f"Fructose total : **{total_fructose} g**")
    st.write(f"🧮 Total glucides : **{total_g} g/h**")

    st.markdown("### 📈 Visualisation de la quantité de glucides (par heure)")
    afficher_jauge_panier(total_g, objectif_min, objectif_max)

    # Ratio réel
    if total_fructose == 0:
        ratio_panier = float("inf") if total_glucose > 0 else 0
    else:
        ratio_panier = round(total_glucose / total_fructose, 2)
        ratio_cible = float("inf") if ratio[1] == 0 else round(ratio[0] / ratio[1], 2)
        ecart_ratio = abs(ratio_panier - ratio_cible)
        ratio_valide = ecart_ratio <= 0.4

        st.write(f"⚖️ Ratio glucose/fructose dans le panier : **{ratio_panier}** (objectif : {ratio_cible})")

        if objectif_min <= total_g <= objectif_max and ratio_valide:
            st.success("✅ Ton panier respecte les apports recommandés (quantité + ratio) !")
        elif not ratio_valide and objectif_min <= total_g <= objectif_max:
            st.warning("⚠️ Quantité OK, mais le ratio glucose/fructose n'est pas adapté.")
        elif ratio_valide and not (objectif_min <= total_g <= objectif_max):
            st.warning("⚠️ Ratio OK, mais la quantité de glucides est hors cible.")
        else:
            st.error("❌ Ni la quantité ni le ratio ne respectent les recommandations.")

            # Objectif total g/h (dans plage centrale)
            cible_glucides = (objectif_min + objectif_max) / 2
            cible_ratio = ratio_cible

            # Objectif glucose/fructose depuis ratio cible
            fructose_cible = cible_glucides / (1 + cible_ratio)
            glucose_cible = cible_glucides - fructose_cible

            manque_glucose = round(glucose_cible - total_glucose)
            manque_fructose = round(fructose_cible - total_fructose)

            texte_glu = f" Ajoute **{abs(manque_glucose)} g de glucose**" if manque_glucose > 0 else f"➖ Retire **{abs(manque_glucose)} g de glucose**"
            texte_fru = f" Ajoute **{abs(manque_fructose)} g de fructose**" if manque_fructose > 0 else f"➖ Retire **{abs(manque_fructose)} g de fructose**"

            st.markdown("### 🛠️ Suggestion d'ajustement :")
            st.markdown(f"- {texte_glu}")
            st.markdown(f"- {texte_fru}")


# === Conseils pratiques ===
with st.expander("🍴 Recommandations sur les aliments solides"):
    st.markdown("""
    - ✅ Privilégier les **gels** pour les efforts de haute intensité ou en course.
    - 🏠 Les **recettes maison** sont pratiques, digestes, économiques.
    - 🔎 Si vous achetez des produits, **Vérifiez** les valeurs nutritionnelles :
      - ❌ Évitez > 2 g de lipides / protéines / fibres par portion.
    """)

with st.expander("🔍 À propos des produits industriels"):
    st.markdown("""
    ⚠️ Ne pas acheter des produits qui contiennent additifs, édulcorants, colorants ou substances chimique délétèrre pour votre santé.  
    👉 Éviter les bonbons : leur composition n'est souvent pas saine.
    """)

