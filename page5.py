
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from io import BytesIO
from datetime import datetime

st.set_page_config(page_title="Multi-Trace", layout="wide")

# ------------------------------------------------------------
# FONCTIONS
# ------------------------------------------------------------

def calculate_mean_direction_and_sigma_theta(wind_directions):
    wind_directions_rad = np.radians(wind_directions - 270)
    mean_sin = np.mean(np.sin(wind_directions_rad))
    mean_cos = np.mean(np.cos(wind_directions_rad))
    mean_direction = np.degrees(np.arctan2(mean_sin, mean_cos))
    sigma_theta = np.degrees(np.sqrt(-2 * np.log(np.sqrt(mean_sin**2 + mean_cos**2))))
    return mean_direction, sigma_theta


def compute_wind_vectors(df):
    results = []
    for minute, group in df.groupby(pd.Grouper(key='Start Time', freq='5Min')):
        mean_speed = group['Wind Speed avg'].mean()
        mean_dir, sigma = calculate_mean_direction_and_sigma_theta(group['Wind Dir. avg'])
        results.append([minute, mean_speed, mean_dir, sigma])
    return pd.DataFrame(results, columns=['Start Time', 'MeanWindSpeed', 'MeanWindDirection', 'SigmaTheta'])



# ------------------------------------------------------------
# INTERFACE PRINCIPALE
# ------------------------------------------------------------

st.title("📈 Multi-Trace")

uploaded_file = st.file_uploader("Sélectionner un fichier Excel", type=["xlsx"])


# ------------------------------------------------------------
# SIDEBAR – OPTIONS D’AFFICHAGE
# ------------------------------------------------------------

with st.sidebar.expander("⚙️ Options d’affichage"):
    wind = st.checkbox("Afficher vent (vitesse)", value=True)
    kmh = st.checkbox("Afficher vent en km/h ?", value=True)
    direction = st.checkbox("Afficher direction du vent", value=True)
    dirlabel = st.checkbox("Afficher étiquettes direction", value=False)
    celcius = st.checkbox("Afficher Température (°C)", value=True)
    HR = st.checkbox("Afficher Humidité relative", value=True)
    download_graph = st.checkbox("Activer téléchargement du graphique")


# ---------------------------------------------------------------------------------
# LECTURE ET TRAITEMENT DU FICHIER
# ---------------------------------------------------------------------------------

if uploaded_file:

    df = pd.read_excel(uploaded_file)
    df["Start Time"] = pd.to_datetime(df["Start Time"])
    results_df = compute_wind_vectors(df)

    # ------------------------------------------------------------
    # ÉCHELLES AUTOMATIQUES
    # ------------------------------------------------------------
    laeq_min_auto = float(df["LAeq"].min())
    laeq_max_auto = float(df["LAeq"].max())

    if kmh:
        wind_series = df["Wind Speed avg"] * 3.6
    else:
        wind_series = df["Wind Speed avg"]

    wind_min_auto = float(wind_series.min())
    wind_max_auto = float(wind_series.max())

    hr_min_auto = float(df["Amb. Humidity"].min())
    hr_max_auto = float(df["Amb. Humidity"].max())

    temp_min_auto = float(df["Amb. Temperature"].min())
    temp_max_auto = float(df["Amb. Temperature"].max())


    # ------------------------------------------------------------
    # SIDEBAR – CONTROLE DES ECHELLES
    # ------------------------------------------------------------

    with st.sidebar.expander("📏 Contrôle manuel des échelles"):
        
        st.markdown("Les valeurs entre parenthèses proviennent des données.")

        reset = st.button("🔄 Réinitialiser aux valeurs auto")

        # Valeurs par défaut
        laeq_min_val, laeq_max_val = laeq_min_auto, laeq_max_auto
        wind_min_val, wind_max_val = wind_min_auto, wind_max_auto
        hr_min_val, hr_max_val = hr_min_auto, hr_max_auto
        temp_min_val, temp_max_val = temp_min_auto, temp_max_auto

        if reset:
            st.info("✔️ Échelles réinitialisées.")

        # --- LAeq ---
        st.markdown(f"### LAeq (auto : {laeq_min_auto:.1f} → {laeq_max_auto:.1f})")
        c1, c2 = st.columns(2)
        laeq_min = c1.number_input("LAeq Min", value=laeq_min_val)
        laeq_max = c2.number_input("LAeq Max", value=laeq_max_val)

        # --- Vent ---
        st.markdown(f"### Vent ({'km/h' if kmh else 'm/s'}) – auto : {wind_min_auto:.1f} → {wind_max_auto:.1f}")
        c3, c4 = st.columns(2)
        wind_min = c3.number_input("Vent Min", value=wind_min_val)
        wind_max = c4.number_input("Vent Max", value=wind_max_val)

        # --- HR ---
        st.markdown(f"### Humidité relative (%HR) – auto : {hr_min_auto:.1f} → {hr_max_auto:.1f}")
        c5, c6 = st.columns(2)
        hr_min = c5.number_input("HR Min", value=hr_min_val)
        hr_max = c6.number_input("HR Max", value=hr_max_val)

        # --- Température ---
        st.markdown(f"### Température (°C) – auto : {temp_min_auto:.1f} → {temp_max_auto:.1f}")
        c7, c8 = st.columns(2)
        temp_min = c7.number_input("Temp. Min", value=temp_min_val)
        temp_max = c8.number_input("Temp. Max", value=temp_max_val)

        # --- VALIDATION ---
        def validate(name, vmin, vmax, auto_min, auto_max):
            if vmin >= vmax:
                st.warning(f"⚠️ {name} : min ≥ max → réinitialisé")
                return auto_min, auto_max
            return vmin, vmax

        laeq_min, laeq_max = validate("LAeq", laeq_min, laeq_max, laeq_min_auto, laeq_max_auto)
        wind_min, wind_max = validate("Vent", wind_min, wind_max, wind_min_auto, wind_max_auto)
        hr_min, hr_max = validate("HR", hr_min, hr_max, hr_min_auto, hr_max_auto)
        temp_min, temp_max = validate("Température", temp_min, temp_max, temp_min_auto, temp_max_auto)


    # ------------------------------------------------------------
    # GRAPHIQUE
    # ------------------------------------------------------------

    fig, ax1 = plt.subplots(figsize=(18, 10))
    ax1.grid(True)

    # LAeq
    ax1.plot(df["Start Time"], df["LAeq"], color='C0')
    ax1.set_ylabel("LAeq", color='C0')
    ax1.tick_params(axis="x", rotation=55)
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
    ax1.set_ylim(laeq_min, laeq_max)
    ax1.set_title("Données mesurées")

    # Vent vitesse
    if wind:
        ax2 = ax1.twinx()
        if kmh:
            ax2.plot(df["Start Time"], df["Wind Speed avg"] * 3.6, color='C1')
            ax2.set_ylabel("Vent vitesse (km/h)", color='C1')
        else:
            ax2.plot(df["Start Time"], df["Wind Speed avg"], color='C1')
            ax2.set_ylabel("Vent vitesse (m/s)", color='C1')
        ax2.set_ylim(wind_min, wind_max)
        ax2.tick_params(axis='y', labelcolor='C1')

    # Humidité relative
    if HR:
        ax3 = ax1.twinx()
        ax3.spines['right'].set_position(('outward', 40))
        ax3.plot(df["Start Time"], df["Amb. Humidity"], color='C2')
        ax3.set_ylabel("%HR", color='C2')
        ax3.set_ylim(hr_min, hr_max)

    # Température
    if celcius:
        ax4 = ax1.twinx()
        ax4.spines['right'].set_position(('outward', 100))
        ax4.plot(df["Start Time"], df["Amb. Temperature"], color='C4')
        ax4.set_ylabel("Température (°C)", color='C4')
        ax4.set_ylim(temp_min, temp_max)

    # Direction du vent
    if direction:
        results_df["row"] = results_df.index
        ax_top = ax1.twiny()

        wind_rad = np.radians(results_df["MeanWindDirection"])

        # position dynamique des flèches (5% sous le max)
        y_arrow = laeq_max - (laeq_max - laeq_min) * 0.05

        ax_top.quiver(
            results_df["row"],
            y_arrow,
            np.cos(wind_rad),
            np.sin(-wind_rad),
            scale_units="xy",
            scale=1,
            width=0.003
        )

        # étiquettes
        if dirlabel:
            y_label = y_arrow - (laeq_max - laeq_min) * 0.03
            for idx, row in results_df.iterrows():
                ax_top.text(
                    row["row"],
                    y_label,
                    f'{row["MeanWindDirection"]+270:.1f}\n({row["SigmaTheta"]:.1f})',
                    color='red',
                    ha='center',
                    fontsize=8
                )

    st.pyplot(fig)

    # Téléchargement
    if download_graph:
        buffer = BytesIO()
        fig.savefig(buffer, format="png")
        st.download_button(
            label="Télécharger le graphique (.png)",
            data=buffer.getvalue(),
            file_name=f"traces_{datetime.now().strftime('%Y-%m-%d_%Hh%Mm%Ss')}.png",
            mime="image/png"
        )
``
