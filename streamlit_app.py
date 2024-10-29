import os
from http.client import responses

import pandas as pd
import streamlit as st

from helpers.DataLoading import downloadData


# Load the data from the Excel file (this assumes you have the file in the same directory)
filename = 'data.xlsx'
file_path = 'assets'
sheet_name = 'Data'

# Geographies and year for ABS data to download
abs_file_path = 'ABS_Data'
geographies = ['LGA', 'SA3', 'SAL']
year = 2021


# --- PAGE SETUP ---
about_page = st.Page(
    page="views/landing_page.py",
    title="About Project",
    icon="🐷",
    default=True,
)
crime_map_page = st.Page(
    page="views/crime_map.py",
    title="Crime Map",
    icon="📈",
)
crime_over_time_page = st.Page(
    page="views/crime_over_time.py",
    title="Crime Over Time",
    icon="📈",
)
crime_total_wa_page = st.Page(
    page="views/crime_total_wa.py",
    title="Crime for All of WA",
    icon="📈",
)
metro_vs_regional_page = st.Page(
    page="views/metro_vs_regional.py",
    title="Metro vs Regional Crime",
    icon="📈",
)
crime_by_district_page = st.Page(
    page="views/crime_by_district.py",
    title="Crime per District",
    icon="📈",
)

# --- NAVIGATION SETUP ---
pg = st.navigation(
    {
        "Info": [about_page],
        "Visualizations": [
            crime_map_page,
            crime_over_time_page,
            crime_total_wa_page,
            metro_vs_regional_page,
            crime_by_district_page,
        ],
    }
)

# --- PAGE LAYOUT SETUP ---
st.set_page_config(layout='wide')

# --- COMMON ASSETS ---
st.sidebar.text("Created by Machine Masters 🤖")
st.logo("assets/Police-logo-240-2021.png")
st.sidebar.download_button(
    label="Download Dataset",
    data="./assets/data.xlsx",
    file_name="WA Police Force Crime Timeseries.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    help="Download the dataset for you own use",
)

# --- DOWNLOAD DATASET ---
downloadData(
    filename,
    file_path=file_path,
    abs_file_path=abs_file_path,
    geographies=geographies,
    year=year,
)

# --- RUN NAVIGATION ---
pg.run()