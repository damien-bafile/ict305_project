from http.client import responses

import streamlit as st
import pandas as pd
import os
import requests

# Load the data from the Excel file (this assumes you have the file in the same directory)
file_path = "assets/data.xlsx"


def download_dataset(file):
    url = "https://www.police.wa.gov.au/Crime/~/media/5BBD428073EC4651B0C4693CD21E532C.ashx"
    response = requests.get(url)
    with open(file, "wb") as f:
        f.write(response.content)


# --- PAGE SETUP ---
about_page = st.Page(
    page="views/landing_page.py",
    title="About Project",
    icon="🐷",
    default=True,
)

bokem_homicide_test_page = st.Page(
    page="views/bokem_homicide_test.py", title="Test Homicide Bokem Graph", icon="📈"
)

metro_vs_regional_page = st.Page(
    page="views/metro_vs_regional.py",
    title="Metro vs Regional Crime",
)
# --- NAVIGATION SETUP ---
pg = st.navigation(
    {
        "Info": [about_page],
        "Visualizations": [bokem_homicide_test_page, metro_vs_regional_page],
    }
)

# -- COMMON ASSETS ---
st.sidebar.text("Created by Machine Masters 🤖")
st.logo("assets/Police-logo-240-2021.png")
st.sidebar.download_button(
    label="Download Dataset",
    data="./assets/data.xlsx",
    file_name="WA Police Force Crime Timeseries.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    help="Download the dataset for you own use",
)
# -- DOWNLOAD DATASET ---
download_dataset(file_path)

# -- RUN NAVIGATION ---
pg.run()
