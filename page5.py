import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import soundfile as sf
from scipy.signal import spectrogram

st.title("Comparaison de lecture de fichier audio WAV")

uploaded_file = st.file_uploader("Sélectionnez un fichier WAV", type=["wav"])

if uploaded_file is not None:
    st.audio(uploaded_file, format='audio/wav')

    # Analyse 1 : Lecture avec scipy.io.wavfile
    st.header("Analyse avec scipy.io.wavfile")
    try:
        rate_scipy, data_scipy = wavfile.read(uploaded_file)
        st.write(f"Taux d'échantillonnage : {rate_scipy} Hz")
        st.write(f"Forme des données : {data_scipy.shape}")

        fig1, ax1 = plt.subplots()
        ax1.specgram(data_scipy[:, 0] if data_scipy.ndim > 1 else data_scipy, Fs=rate_scipy)
        ax1.set_title("Sonogramme avec matplotlib.specgram (scipy)")
        st.pyplot(fig1)

        f, t, Sxx = spectrogram(data_scipy[:, 0] if data_scipy.ndim > 1 else data_scipy, rate_scipy)
        fig2, ax2 = plt.subplots()
        pcm = ax2.pcolormesh(t, f, 10 * np.log10(Sxx), shading='gouraud')
        ax2.set_title("Spectrogramme avec scipy.signal.spectrogram (scipy)")
        fig2.colorbar(pcm, ax=ax2)
        st.pyplot(fig2)
    except Exception as e:
        st.error(f"Erreur lors de la lecture avec scipy: {e}")

    # Analyse 2 : Lecture avec soundfile
    st.header("Analyse avec soundfile")
    try:
        data_sf, rate_sf = sf.read(uploaded_file)
        st.write(f"Taux d'échantillonnage : {rate_sf} Hz")
        st.write(f"Forme des données : {data_sf.shape}")

        fig3, ax3 = plt.subplots()
        ax3.specgram(data_sf[:, 0] if data_sf.ndim > 1 else data_sf, Fs=rate_sf)
        ax3.set_title("Sonogramme avec matplotlib.specgram (soundfile)")
        st.pyplot(fig3)

        f2, t2, Sxx2 = spectrogram(data_sf[:, 0] if data_sf.ndim > 1 else data_sf, rate_sf)
        fig4, ax4 = plt.subplots()
        pcm2 = ax4.pcolormesh(t2, f2, 10 * np.log10(Sxx2), shading='gouraud')
        ax4.set_title("Spectrogramme avec scipy.signal.spectrogram (soundfile)")
        fig4.colorbar(pcm2, ax=ax4)
        st.pyplot(fig4)
    except Exception as e:
        st.error(f"Erreur lors de la lecture avec soundfile: {e}")