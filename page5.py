
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from io import BytesIO
from datetime import datetime

st.set_page_config(page_title="Multi-Trace", layout="wide")

# --- Fonctions ------------------------------------------------------

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

# --- Interface utilisateur ------------------------------------------

st.title("📈 Multi-Trace")

uploaded_file = st.file_uploader("Sélectionner un fichier Excel", type=["xlsx"])

# Options interactives
wind = st.checkbox("Vent vitesse", value=True)
kmh = st.checkbox("km/h ?", value=True)
direction = st.checkbox("Vent direction", value=True)
dirlabel = st.checkbox("Afficher étiquettes direction", value=False)
celcius = st.checkbox("Température (°C)", value=True)
HR = st.checkbox("Humidité relative", value=True)
download_graph = st.checkbox("Télécharger le graphique")

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    df["Start Time"] = pd.to_datetime(df["Start Time"])

    results_df = compute_wind_vectors(df)

    # --- Création du graphique --------------------------------------

    fig, ax1 = plt.subplots(figsize=(18, 10))
    ax1.grid(True)

    # LAeq
    ax1.plot(df["Start Time"], df["LAeq"], color='C0')
    ax1.set_ylabel("LAeq", color='C0')
    ax1.tick_params(axis="x", rotation=55)
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
    ax1.set_ylim(df["LAeq"].min() - 5, df["LAeq"].max() + 10)
    ax1.set_title("Données mesurées")

    # Vent vitesse
    if wind:
        ax2 = ax1.twinx()
        if kmh:
            ax2.plot(df['Start Time'], df['Wind Speed avg'] * 3.6, color='C1')
            ax2.set_ylabel("Vent vitesse (km/h)", color='C1')
            ax2.set_ylim(0, 90)
        else:
            ax2.plot(df['Start Time'], df['Wind Speed avg'], color='C1')
            ax2.set_ylabel("Vent vitesse (m/s)", color='C1')
            ax2.set_ylim(0, 3)

        ax2.tick_params(axis='y', labelcolor='C1')

    # Humidité relative
    if HR:
        ax3 = ax1.twinx()
        ax3.spines['right'].set_position(('outward', 40))
        ax3.plot(df["Start Time"], df["Amb. Humidity"], color='C2')
        ax3.set_ylabel("%HR", color='C2')
        ax3.set_ylim(0, 100)

    # Température
    if celcius:
        ax4 = ax1.twinx()
        ax4.spines['right'].set_position(('outward', 100))
        ax4.plot(df["Start Time"], df["Amb. Temperature"], color='C4')
        ax4.set_ylabel("Température (°C)", color='C4')

    # Direction du vent (flèches)
    if direction:
        results_df["row"] = results_df.index
        ax_top = ax1.twiny()

        wind_rad = np.radians(results_df["MeanWindDirection"])
        ax_top.quiver(
            results_df["row"],
            df["LAeq"].max() + 5,
            np.cos(wind_rad),
            np.sin(-wind_rad),
            scale_units="xy",
            scale=1,
            width=0.003
        )

        if dirlabel:
            for idx, row in results_df.iterrows():
                ax_top.text(
                    row["row"],
                    df["LAeq"].max() + 4,
                    f'{row["MeanWindDirection"]+270:.1f}\n({row["SigmaTheta"]:.1f})',
                    color='red',
                    ha='center',
                    fontsize=8
                )

    st.pyplot(fig)

    # --- Téléchargement -----------------------------------------

    if download_graph:
        buffer = BytesIO()
        fig.savefig(buffer, format="png")
        st.download_button(
            label="Télécharger le graphique (.png)",
            data=buffer.getvalue(),
            file_name=f"traces_{datetime.now().strftime('%Y-%m-%d_%Hh%Mm%Ss')}.png",
            mime="image/png"
        )
