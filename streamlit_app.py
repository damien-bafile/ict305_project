import streamlit as st
from helpers.DataLoading import downloadData, loadData
from helpers.ZipDataset import zip_dataset
from helpers.CreatePage import create_page

# this is the main entry point for the streamlit app

# --- DATA SETUP ---
folder_path = "./assets/"
file_names = [
    "data.xlsx",
    "WAPoliceForceDistrictboundaries(WAPOL-002).geojson",
    "./ABS_Data/LGA_2021_AUST.xlsx" "./ABS_Data/SA3_2021_AUST.xlsx",
    "./ABS_Data/SAL_2021_AUST.xlsx",
    "2021Census_G01_WA_LGA.csv",
    "2021Census_G01_WA_SA3.csv",
    "2021Census_G01_WA_SAL.csv",
]

# Download the dataset
downloadData()
# Load the dataset
loadData()
# Create a zip file object containing the dataset ready for download
zip_file_object = zip_dataset(folder_path, file_names)

# --- PAGE SETUP ---
# Set the page title and layout to wide
st.set_page_config(page_title="ICT305 Machine Masters", layout="wide")

# Create a navigation sidebar with the following pages, using descriptive names
about_page = create_page(
    page_path="views/landing_page.py",
    title="About Project",
    icon="🐷",
    default=True,
)

# TODO: Using more descriptive names for the pages
homicide_by_population_page = create_page(
    page_path="views/crime_over_population.py",
    title="Homicide by Population",
    icon="🗺️",
)

crime_trends_page = create_page(
    page_path="views/crime_over_time.py",
    title="Crime Trends Over Time",
)

metro_vs_regional_crime_page = create_page(
    page_path="views/metro_vs_regional.py",
    title="Metro vs Regional Crime",
)

entertainment_zone_crime_page = create_page(
    page_path="views/entertainment_crime.py",
    title="Crime in Entertainment Zones",
)

# Load the pages into the navigation sidebar sorted by category
pg = st.navigation(
    {
        "Info": [about_page],
        "Visualizations": [
            homicide_by_population_page,
            crime_trends_page,
            metro_vs_regional_crime_page,
            entertainment_zone_crime_page,
        ],
    }
)

# Adds a footer to the sidebar
st.sidebar.text("Created by Machine Masters 🤖")
st.logo("assets/Police-logo-240-2021.png")
st.sidebar.download_button(
    label="Download Dataset",
    data=zip_file_object,
    file_name="data.zip",
    mime="application/zip",
    help="Download the dataset for you own use",
)

# Run the selected page
pg.run()