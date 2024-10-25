import os
from http.client import responses

import pandas as pd
import requests
import streamlit as st
from helpers.DataLoading import downloadData, loadData

# Load the data from the Excel file (this assumes you have the file in the same directory)
file_path = "assets/data.xlsx"


def download_dataset(file):
    url = "https://www.wa.gov.au/media/48429/download?inline?inline="
    response = requests.get(url)
    with open(file, "wb") as f:
        f.write(response.content)


# -- PAGE CONFIG --
st.set_page_config(page_title="ICT305 Machine Masters", layout="wide")


# --- PAGE SETUP ---
about_page = st.Page(
    page="views/landing_page.py",
    title="About Project",
    icon="🐷",
    default=True,
)

crime_over_population = st.Page(
    page="views/crime_over_population.py",
    title="Test Homicide Bokem Graph",
    icon="📈",
)

crime_over_time = st.Page(
    page="views/crime_over_time.py", title="Crime Over Time", icon="📈"
)

metro_vs_regional_page = st.Page(
    page="views/metro_vs_regional.py",
    title="Metro vs Regional Crime",
    icon="📈",
)

entertainment_page = st.Page(
    page="views/entertainment_crime.py",
    title="Crime in Entertainment areas",
    icon="📈",
)

# --- NAVIGATION SETUP ---
pg = st.navigation(
    {
        "Info": [about_page],
        "Visualizations": [
            crime_over_population,
            crime_over_time,
            metro_vs_regional_page,
            entertainment_page,
        ],
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
downloadData()
loadData()

# -- RUN NAVIGATION ---
pg.run()
