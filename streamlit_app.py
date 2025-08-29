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
main_page = st.Page("main.py", title="Accueil", icon="🎈")
page_2 = st.Page("page_2.py", title="Calculatrice de décibels", icon="❄️")
page_3 = st.Page("page_3.py", title="Calculateur de Lden", icon="🎉")

# Set up navigation
pg = st.navigation([main_page, page_2, page_3])

# Run the selected page
pg.run()
