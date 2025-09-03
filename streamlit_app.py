import streamlit as st

##st.title("🎈 My new app")
##st.write(
##    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
##)

import streamlit as st
import pandas as pd
import numpy as np
import time


# Define the pages
main_page = st.Page("main.py", title="Accueil")
page_2 = st.Page("page_2.py", title="Calculatrice décibels")
page_3 = st.Page("page_3.py", title="Calcul Lden")
page_4 = st.Page("page4.py", title="Rose des vents")
page_5 = st.Page("page5.py", title="comparaison scipy.io.wavfile vs soudfile")

# Set up navigation
pg = st.navigation([main_page, page_2, page_3,page_4,page_5])

# Run the selected page
pg.run()
