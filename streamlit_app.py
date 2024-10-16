import os
from http.client import responses

import pandas as pd
import requests
from zipfile import ZipFile
import streamlit as st

# Load the data from the Excel file (this assumes you have the file in the same directory)
file_path = "assets/data.xlsx"


def download_dataset(file):
    url = "https://www.wa.gov.au/media/48429/download?inline?inline="
    # url = "https://www.police.wa.gov.au/Crime/~/media/5BBD428073EC4651B0C4693CD21E532C.ashx"
    
    response = requests.get(url)
    with open(file, 'wb') as f:
        f.write(response.content)

  
def download_abs_data():
    abs_file_paths = ['ABS_Allocation_Files', 'ABS_Census_DataPacks']
    abs_filenames = [
        ['LGA_2021_AUST.xlsx', 'SA3_2021_AUST.xlsx', 'SAL_2021_AUST.xlsx'],
        ['2021_GCP_LGA_for_WA_short-header.zip', '2021_GCP_SA3_for_WA_short-header.zip', '2021_GCP_SAL_for_WA_short-header.zip'],
    ]
    abs_urls = [
        "https://www.abs.gov.au/statistics/standards/australian-statistical-geography-standard-asgs-edition-3/jul2021-jun2026/access-and-downloads/allocation-files",
        "https://www.abs.gov.au/census/find-census-data/datapacks/download",
    ]
    
    for i in range(2):
        for j in range(3):
            response = requests.get(f'{abs_urls[i]}/{abs_filenames[i][j]}')
            with open(f'assets/{abs_file_paths[i]}/{abs_filenames[i][j]}', 'wb') as f:
                f.write(response.content)


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
download_dataset(file_path)
download_abs_data()

# -- RUN NAVIGATION ---
pg.run()
