# -*- coding: utf-8 -*-
"""
Created on Thu Aug 28 09:59:43 2025

@author: hotju02
"""

import streamlit as st

#t.title("This is the title page 3")

st.markdown("# Page 3 🎉")
st.sidebar.markdown("# Page 3 🎉")

# Titre de l'application
st.title("Calculateur de l'indice acoustique Lden")

# Description de l'application
st.write("""
Cette application calcule l'indice acoustique Lden à partir d'un fichier Excel. 
Veuillez vous assurer que votre fichier contient les colonnes "LAeq_jour", "LAeq_soir" et "LAeq_nuit" avec les valeurs en dB(A).
""")

# Section de chargement du fichier
uploaded_file = st.file_uploader("Choisissez un fichier Excel", type=["xlsx", "xls"])

if uploaded_file is not None:
    # Lecture du fichier Excel
    try:
        df = pd.read_excel(uploaded_file)
        st.write("Aperçu des données chargées :")
        st.dataframe(df.head())

        # Vérification des colonnes requises
        required_cols = ["LAeq_jour", "LAeq_soir", "LAeq_nuit"]
        if all(col in df.columns for col in required_cols):

            # Calcul du Lden
            # Formule: Lden = 10 * log10 [ (12/24) * 10^(Ljour/10) + (4/24) * 10^((Lsoir+5)/10) + (8/24) * 10^((Lnuit+10)/10) ]
            
            # Les valeurs sont en dB, donc on les convertit en pression acoustique (10^(L/10))
            P_jour = 10**(df["LAeq_jour"] / 10)
            P_soir_pondere = 10**((df["LAeq_soir"] + 5) / 10)
            P_nuit_pondere = 10**((df["LAeq_nuit"] + 10) / 10)
            
            # Calcul de la moyenne énergétique
            P_den = (12/24) * P_jour + (4/24) * P_soir_pondere + (8/24) * P_nuit_pondere

            # Conversion du résultat en dB
            lden = 10 * np.log10(P_den)

            st.subheader("Résultats du calcul Lden")
            st.dataframe(pd.DataFrame(lden, columns=["Lden (dB)"]))

            # Option de téléchargement des résultats
            csv_data = pd.DataFrame(lden, columns=["Lden (dB)"]).to_csv(index=False)
            st.download_button(
                label="Télécharger les résultats en CSV",
                data=csv_data,
                file_name='resultats_lden.csv',
                mime='text/csv',
            )

        else:
            st.error("Erreur : Le fichier ne contient pas toutes les colonnes requises (LAeq_jour, LAeq_soir, LAeq_nuit).")

    except Exception as e:
        st.error(f"Une erreur s'est produite lors du traitement du fichier : {e}")



