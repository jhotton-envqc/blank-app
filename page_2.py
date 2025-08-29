# -*- coding: utf-8 -*-
"""
Created on Thu Aug 28 09:56:25 2025

@author: hotju02
"""

import streamlit as st
import math

#st.title("This is the title page 2")

# =============================================================================
st.markdown("# Page 2 ❄️")
st.sidebar.markdown("# Page 2 ❄️")
# =============================================================================


# Titre de l'application
st.title("Additionneur / Soustracteur de Décibels")

# Explication
st.write("Cette application permet d'additionner ou de soustraire deux niveaux en décibels (dB) "
         "en les convertissant en intensité, puis en reconvertissant le résultat en dB.")

# Entrée des deux valeurs en dB
dB1 = st.number_input("Entrez la première valeur en dB :", format="%0.2f")
dB2 = st.number_input("Entrez la deuxième valeur en dB :", format="%.2f")

# Choix de l'opération
operation = st.radio("Choisissez l'opération :", ("Addition", "Soustraction"))

# Conversion des dB en intensité
I1 = 10 ** (dB1 / 10)
I2 = 10 ** (dB2 / 10)

# Calcul selon l'opération choisie
if operation == "Addition":
    I_result = I1 + I2
    dB_result = 10 * math.log10(I_result)
    st.success(f"Résultat de l'addition : {dB_result:.2f} dB")
else:
    if I1 > I2:
        I_result = I1 - I2
        dB_result = 10 * math.log10(I_result)
        st.success(f"Résultat de la soustraction : {dB_result:.2f} dB")
    else:
        st.error("Erreur : L'intensité correspondant à la première valeur doit être supérieure à celle de la deuxième pour effectuer une soustraction.")