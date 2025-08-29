# -*- coding: utf-8 -*-
"""
Created on Thu Aug 28 09:25:20 2025

@author: hotju02
"""

import streamlit as st
import pandas as pd
import numpy as np
import time


# Define the pages
main_page = st.Page("main.py", title="Main Page", icon="🎈")
page_2 = st.Page("page_2.py", title="Page 2", icon="❄️")
page_3 = st.Page("page_3.py", title="Page 3", icon="🎉")

# Set up navigation
pg = st.navigation([main_page, page_2, page_3])

# Run the selected page
pg.run()


# =============================================================================
# st.title("This is the title of our app")
# 
# 
# df = pd.DataFrame({
#   'first column': [1, 2, 3, 4],
#   'second column': [10, 20, 30, 40]
# })
# 
# df
# 
# st.write("Here's our first attempt at using data to create a table:")
# st.write(pd.DataFrame({
#     'first column': [1, 2, 3, 4],
#     'second column': [10, 20, 30, 40]
# }))
# 
# dataframe = np.random.randn(10, 20)
# st.dataframe(dataframe)
# =============================================================================


# =============================================================================
# dataframe = pd.DataFrame(
#     np.random.randn(10, 20),
#     columns=('col %d' % i for i in range(20)))
# 
# st.dataframe(dataframe.style.highlight_max(axis=0))
# =============================================================================

# =============================================================================
# dataframe = pd.DataFrame(
#     np.random.randn(10, 20),
#     columns=('col %d' % i for i in range(20)))
# st.table(dataframe)
# =============================================================================

# =============================================================================
# chart_data = pd.DataFrame(
#      np.random.randn(20, 3),
#      columns=['a', 'b', 'c'])
# 
# st.line_chart(chart_data)
# 
# =============================================================================

# =============================================================================
# map_data = pd.DataFrame(
#     np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
#     columns=['lat', 'lon'])
# 
# st.map(map_data)
# =============================================================================

# =============================================================================
# x = st.slider('x')  # 👈 this is a widget
# st.write(x, 'squared is', x * x)
# =============================================================================

# =============================================================================
# # Add a selectbox to the sidebar:
# add_selectbox = st.sidebar.selectbox(
#     'How would you like to be contacted?',
#     ('Email', 'Home phone', 'Mobile phone')
# )
# 
# # Add a slider to the sidebar:
# add_slider = st.sidebar.slider(
#     'Select a range of values',
#     0.0, 100.0, (25.0, 75.0)
# )
# 
# left_column, right_column = st.columns(2)
# # You can use a column just like st.sidebar:
# left_column.button('Press me!')
# 
# # Or even better, call Streamlit functions inside a "with" block:
# with right_column:
#     chosen = st.radio(
#         'Sorting hat',
#         ("Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin"))
#     st.write(f"You are in {chosen} house!")
# =============================================================================

# =============================================================================
# 'Starting a long computation...'
# 
# # Add a placeholder
# latest_iteration = st.empty()
# bar = st.progress(0)
# 
# for i in range(100):
#   # Update the progress bar with each iteration.
#   latest_iteration.text(f'Iteration {i+1}')
#   bar.progress(i + 1)
#   time.sleep(0.1)
# 
# '...and now we\'re done!'
# =============================================================================
