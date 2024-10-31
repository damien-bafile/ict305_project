import os
from http.client import responses

import pandas as pd
import streamlit as st
from helpers.DataLoading import downloadData, loadData
from helpers.ZipDataset import zip_dataset
from helpers.CreatePage import create_page

# this is the main entry point for the streamlit app
from helpers.DataLoading import downloadData


# Load the data from the Excel file (this assumes you have the file in the same directory)
filename = 'data.xlsx'
file_path = 'assets'
sheet_name = 'Data'

# --- DATA SETUP ---
file_names = [
    "data.xlsx",
    "WAPoliceForceDistrictboundaries(WAPOL-002).geojson",
    "./ABS_Data/LGA_2021_AUST.xlsx" "./ABS_Data/SA3_2021_AUST.xlsx",
    "./ABS_Data/SAL_2021_AUST.xlsx",
    "2021Census_G01_WA_LGA.csv",
    "2021Census_G01_WA_SA3.csv",
    "2021Census_G01_WA_SAL.csv",
]

# Geographies and year for ABS data to download
abs_file_path = 'ABS_Data'
geographies = ['LGA', 'SA3', 'SAL']
year = 2021

# Create a zip file object containing the dataset ready for download
zip_file_object = zip_dataset(file_path, file_names)

# --- PAGE SETUP ---
# Set the page title and layout to wide
st.set_page_config(page_title="ICT305 Machine Masters", layout="wide")

# Create a navigation sidebar with the following pages, using descriptive names
landing_page = create_page(
    page_path="views/landing_page.py",
    title="About Project",
    icon="👮",
    default=True,
)

# TODO: Using more descriptive names for the pages
crime_by_district = create_page(
    page_path="views/crime_by_district.py",
    title="Crime by District",
    icon="🏢",
)

crime_map = create_page(
    page_path="views/crime_map.py",
    title="Crime Map",
    icon="🗺️",
)

crime_over_time = create_page(
    page_path="views/crime_over_time.py",
    title="Crime Over Time",
)

metro_vs_regional = create_page(
    page_path="views/metro_vs_regional.py",
    title="Metro vs Regional Crime",
    icon="👨‍🌾",
)

crime_total_wa = create_page(
    page_path="views/crime_total_wa.py",
    title="Total Crime in WA",
    icon="📊",
)

about_us_page = create_page(
    page_path="views/about_us.py",
    title="About Us",
    icon="👨‍💻",
)

references_page = create_page(
    page_path="views/references.py",
    title="References",
    icon="📚",
)

# Load the pages into the navigation sidebar sorted by category
pg = st.navigation(
    {
        "Info": [landing_page],
        "Visualizations": [
            crime_by_district,
            crime_map,
            crime_over_time,
            metro_vs_regional,
            crime_total_wa,
        ],
        "Additional": [references_page, about_us_page],
    }
)

# Adds a footer to the sidebar
st.sidebar.text("Created by Machine Masters 🤖")
st.logo("assets/images/Police-logo-240-2021.png")
st.sidebar.download_button(
    label="Download Dataset",
    data=zip_file_object,
    file_name="data.zip",
    mime="application/zip",
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
