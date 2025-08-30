import streamlit as st, streamlit_authenticator as stauth

# --- Auth (même logique que dans app.py) ---
users_ss = st.secrets["credentials"]["usernames"]
credentials = {"usernames": {u: {"name": i["name"], "email": i["email"], "password": i["password"]} for u,i in users_ss.items()}}
c = st.secrets["cookie"]
authenticator = stauth.Authenticate(credentials, c["name"], c["key"], int(c["expiry_days"]))
name, auth_status, username = authenticator.login("Connexion", "main")
if not auth_status: st.stop()

st.title("Nutrition — Course")
# 👉 Colle ici le code de la page Entraînement (calcul gels/boissons…)



st.set_page_config(page_title="Course - Nutrition", layout="centered")

st.title("🏁 Calcul nutrition course")

st.markdown("Choisissez vos conditions de course :")

# === CONDITIONS NORMALES ===
with st.expander("🟢 Conditions normales (<27 °C)", expanded=True):

    duree_course = st.slider("⏱️ Durée prévue de la course (h)", 2.0, 3.0, 2.5, 0.25)

    apport_cible = round(90 + (duree_course - 2) * 30)
    glucides_totaux = round(apport_cible * duree_course)

    st.success(f"Objectif : {apport_cible} g/h → {glucides_totaux} g au total")

    st.subheader("🚰 Boisson (entraînement ou course)")

    nb_bidons = round(duree_course)
    eau = nb_bidons * 500
    glucides_boisson = nb_bidons * 40

    st.markdown(f"""
    - 💧 {nb_bidons} bidons de 500 mL → **{eau} mL**
    - 🍬 {glucides_boisson} g via boisson (40 g/bidon)
    """)

    # Calcul du reste à couvrir avec des gels
    glucides_gels = glucides_totaux - glucides_boisson

    st.subheader("🍯 Gels à prévoir")

    st.markdown(f"""
    - Apport total via boisson : **{glucides_boisson} g**  
    - Apport cible total : **{glucides_totaux} g**  
    - ✅ Il reste à consommer via gels : **{glucides_gels} g**

    **Répartition par heure :**

    - {round(glucides_gels / duree_course)} g de glucides par heure via gels  
    - Exemple :  
        - {round((glucides_gels / duree_course) / 30, 1)} gel(s) de 30 g / h  
        - ou {round((glucides_gels / duree_course) / 25, 1)} gel(s) de 25 g / h  
    """)

    st.info("Ratio glucose/fructose à respecter dans les gels : entre **1 / 0.8** et **1 / 1**")


with st.expander("🔥 Conditions chaudes (>27 °C)", expanded=False):
    st.markdown("En cas de forte chaleur, séparer les fonctions de chaque bidon :")

    # Durée de l'effort
    duree_chaud = st.slider("⏱️ Durée prévue de l'effort (h)", 2.0, 3.0, 2.5, 0.25, key="durée_chaud")

    # Calcul de l'apport cible
    apport_cible_chaud = round(90 + (duree_chaud - 2) * 30)  # linéaire 90 → 120 g/h
    glucides_totaux_chaud = round(apport_cible_chaud * duree_chaud)

    st.success(f"Objectif : **{apport_cible_chaud} g/h** → **{glucides_totaux_chaud} g** au total")

    # Bidon 1 : eau + sel
    st.subheader("💧 Bidon 1 : réhydratation (eau + sel)")
    volume1 = st.number_input("Volume du bidon n°1 (mL)", value=500, step=100, key="bidon1")
    st.markdown("""
    - Eau plate ou légèrement minéralisée  
    - 1 pincée de sel (~1 g, soit ≈ 400 mg sodium)  
    - À boire **en petites gorgées régulières**
    """)

    # Bidon 2 : énergétique
    st.subheader("⚡ Bidon 2 : boisson énergétique concentrée")
    volume2 = st.number_input("Volume du bidon n°2 (mL)", value=500, step=100, key="bidon2")
    glucides2 = st.slider("Quantité de glucides (g)", 40, 90, 80, 5, key="glucides2")

    st.markdown("""
    - Eau + **maltodextrine + fructose** (respect du ratio 1/0.8 à 1/1)  
    - 1 pincée de sel pour soutenir la rétention d’eau  
    - ⚠️ Ne pas dépasser 90 g pour 500 mL pour éviter les troubles digestifs
    """)

    # Calcul du reste à couvrir
    nb_bidons = duree_chaud  # 1 jeu de bidons par heure
    glucides_boisson = glucides2 * nb_bidons
    glucides_gels = max(0, glucides_totaux_chaud - glucides_boisson)

    st.subheader("🍯 Gels à prévoir")

    st.markdown(f"""
    - Total apport via boisson : **{glucides_boisson} g**  
    - ✅ Il reste à consommer via gels : **{glucides_gels} g**  
    - Exemples :
        - {glucides_gels // 30} gels de 30 g
        - {glucides_gels // 25} gels de 25 + 1 peu plus
    """)

    st.info("Ratio glucose/fructose à respecter : entre **1 / 0.8** et **1 / 1**")

import streamlit as st
from datetime import datetime, timedelta

with st.expander("☕ Plan Caféine"):
    st.subheader("Calculateur de prise de caféine")

    # Entrée poids
    poids = st.number_input("Entrez votre poids (kg)", min_value=40.0, max_value=120.0, step=0.5)

    # Type de course
    type_course = st.radio("Type de course :", ["Course en ligne", "Course en ligne + CLM"])

    # Option heure départ
    use_time = st.checkbox("Indiquer heure(s) de départ pour afficher les horaires exacts")

    if type_course == "Course en ligne":
        forme = st.radio("Forme de prise :", ["Chwingum (30 min avant)", "Autre (1 h avant)"])
        dose = 4 * poids  # mg
        if forme.startswith("Chwingum"):
            offset = 30
        else:
            offset = 60

        if use_time:
            depart = st.time_input("Heure de départ de la course (HH:MM)")
            depart_dt = datetime.combine(datetime.today(), depart)
            prise_time = (depart_dt - timedelta(minutes=offset)).strftime("%H:%M")
            st.write(f"✅ {dose:.0f} mg → {prise_time} ({offset} min avant départ)")
        else:
            st.write(f"✅ {dose:.0f} mg → {offset} min avant départ")

    elif type_course == "Course en ligne + CLM":
        dose_clm = 3 * poids
        dose_course = 2 * poids

        if use_time:
            depart_clm = st.time_input("Heure de départ CLM (HH:MM)")
            depart_course = st.time_input("Heure de départ course (HH:MM)")
            clm_dt = datetime.combine(datetime.today(), depart_clm)
            course_dt = datetime.combine(datetime.today(), depart_course)
            prise_clm = (clm_dt - timedelta(hours=1)).strftime("%H:%M")
            prise_course = (course_dt - timedelta(minutes=30)).strftime("%H:%M")
            st.write(f"✅ CLM : {dose_clm:.0f} mg → {prise_clm} (1 h avant CLM)")
            st.write(f"✅ Course : {dose_course:.0f} mg → {prise_course} (30 min avant course)")
        else:
            st.write(f"✅ CLM : {dose_clm:.0f} mg → 1 h avant CLM")
            st.write(f"✅ Course : {dose_course:.0f} mg → 30 min avant course")

