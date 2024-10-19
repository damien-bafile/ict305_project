import os
from os import path, makedirs
from http.client import responses

import pandas as pd
import requests
from zipfile import ZipFile
import streamlit as st

from helpers.FileIO import getHTMLData
from calendar import timegm
from datetime import datetime

# Load the data from the Excel file (this assumes you have the file in the same directory)
file_path = 'assets'
filename = 'data.xlsx'

# Geographies and year for ABS data to download
geographies = ['LGA', 'SA3', 'SAL']
year = 2021


# Function for downloading ABS data

def downloadABSData(geographies, file_path = '', year = 2021):
    
    if not path.isdir(file_path):
        makedirs(file_path)

    # Allocation Files (for retrieving codes)
    af_filenames = [f'{g}_{year}_AUST.xlsx' for g in geographies]
    af_url = f"https://www.abs.gov.au/statistics/standards/australian-statistical-geography-standard-asgs-edition-3/jul{year}-jun{year + 5}/access-and-downloads/allocation-files"

    # Census DataPacks (for retrieving populations)
    dp_filenames = [f'{year}_GCP_{g}_for_WA_short-header.zip' for g in geographies]
    dp_url = "https://www.abs.gov.au/census/find-census-data/datapacks/download"

    session = requests.Session()

    # Download ABS Data
    for (url, files) in zip([af_url, dp_url], [af_filenames, dp_filenames]):
        for filename in files:
            if not path.isfile(path.join(file_path, filename)):
                response = session.get(f'{url}/{filename}')
                with open(path.join(file_path, filename), 'wb') as f:
                    f.write(response.content)
    
    # Extract from .zip files
    for (filename, g) in zip(dp_filenames, geographies):
        with ZipFile(path.join(file_path, filename)) as z:
            name_list = z.namelist()
            member_name = [x for x in name_list if x.endswith(f'{year}Census_G01_WA_{g}.csv')][0]
            if not path.isfile(path.join(file_path, path.basename(member_name))):
                with z.open(member_name) as m:
                    with open(path.join(file_path, path.basename(member_name)), 'wb') as f:
                        f.write(m.read())


# Function for checking for dataset updates

def checkDatasetUpdate(filename, url):
    
    file_mtime = path.getmtime(filename)
    soup = getHTMLData(url)
    last_update_time = soup.find(class_ = 'page-reviewed').time['datetime']
    last_update_time = timegm(datetime.timetuple(datetime.fromisoformat(last_update_time)))

    # Return True if webpage has been updated since last dataset download
    return last_update_time > file_mtime


# Function for downloading crime dataset

def downloadDataset(filename, file_path = '', check_exists_first = False):
    
    download = True

    for ext in ['.csv', '.xlsx']:
        filename = filename.removesuffix(ext)
    
    filename = f'{path.join(file_path, filename)}.xlsx'
    
    if check_exists_first:
        url = "https://www.wa.gov.au/organisation/western-australia-police-force/crime-statistics#/start"
        if path.isfile(filename) and not checkDatasetUpdate(filename, url):
            download = False

    if download:
        url = "https://www.wa.gov.au/media/48429/download?inline?inline="
        response = requests.get(url)
        with open(filename, 'wb') as f:
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
downloadDataset(filename, file_path = file_path, check_exists_first = True)
downloadABSData(geographies, file_path = path.join(file_path, 'ABS_Data'), year = year)

# -- RUN NAVIGATION ---
pg.run()
