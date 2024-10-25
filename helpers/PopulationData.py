### PopulationData.py ###

'''
ICT305: Data Visualisation and Simulation
Group Project
Group Name: Machine Masters
Eren Stannard - 34189185
'''


# Import libraries

import os
import numpy as np
import pandas as pd
import requests
from zipfile import ZipFile
from io import BytesIO

from helpers.FileIO import *


# Function for downloading ABS data

def downloadABSData(geographies, file_path = 'assets', abs_data_file_path = 'ABS_Data',
                    year = 2021, download_zips = False, check_first = True):
    
    print("downloadABSData()")
    
    file_path = filePath(abs_data_file_path, file_path = file_path)
    
    downloaded = False
    
    if not os.path.isdir(file_path):
        os.makedirs(file_path)
    url = "https://www.abs.gov.au"
    asgs_url = f"{url}/statistics/standards/australian-statistical-geography-standard-asgs-edition-3"

    # Allocation Files (for retrieving codes)
    af_filenames = [f'{g}_{year}_AUST.xlsx' for g in geographies]
    af_url = f"{asgs_url}/jul{year}-jun{year+5}/access-and-downloads/allocation-files"

    # Census DataPacks (for retrieving populations)
    dp_zip_filenames = [f'{year}_GCP_{g}_for_WA_short-header.zip' for g in geographies]
    dp_filenames = [f'{year}Census_G01_WA_{g}.csv' for g in geographies]
    dp_url = f"{url}/census/find-census-data/datapacks/download"

    session = requests.Session()

    # Download Allocation Files
    for filename in af_filenames:
        full_filename = filePath(filename, file_path = file_path)
        if not os.path.isfile(full_filename):
            print(f"Downloading {filename}...")
            response = session.get(f'{af_url}/{filename}')
            with open(full_filename, 'wb') as f:
                f.write(response.content)
                downloaded = True
        else:
            print(f"{filename} already downloaded.")

    # Download Census DataPacks
    for (filename, member_name) in zip(dp_zip_filenames, dp_filenames):
        
        full_filename = filePath(filename, file_path = file_path)
        member_filename = filePath(member_name, file_path = file_path)
        zip_exists = os.path.isfile(full_filename)
        member_exists = os.path.isfile(member_filename)

        if not ((zip_exists or not download_zips) and member_exists):
            print(f"Downloading {member_name} from {filename}...")
            response = session.get(f'{dp_url}/{filename}')

        if download_zips:
            if not zip_exists:
                print(f"Downloading {filename}...")
                with open(full_filename, 'wb') as f:
                    f.write(response.content)
                    downloaded = True
            else:
                print(f"{filename} already downloaded.")
                download_zips = False
        
        if download_zips or not member_exists:
            print(f"Downloading {member_name}...")
            with ZipFile(BytesIO(response.content)) as z:
                member_path = [x for x in z.namelist() if x.endswith(member_name)][0]
                member_filename = filePath(member_name, file_path = file_path)
                with open(member_filename, 'wb') as f:
                    f.write(z.read(member_path))
                    downloaded = True
        else:
            print(f"{member_name} already downloaded.")
    
    return downloaded


# Function for loading ABS data

def loadABSData(file_path = 'assets', abs_data_file_path = 'ABS_Data', geographies = [],
                year = 2021, get_csv = True, download = False):

    print("loadABSData()")
    
    file_path = filePath(abs_data_file_path, file_path = file_path)
    
    dfs = dict.fromkeys(geographies)

    # Allocation Files (for retrieving codes)
    af_filenames = [f'{g}_{year}_AUST.xlsx' for g in geographies]

    # Census DataPacks (for retrieving populations)
    dp_filenames = [f'{year}Census_G01_WA_{g}.csv' for g in geographies]

    for filename in af_filenames + dp_filenames:
        filename, _ = filePath(filename, file_path = file_path, split_ext = True)
        print(filename)
        if not os.path.isfile(f'{filename}.csv'):
            download = True
            break

    if download:
        downloadABSData(geographies, file_path = file_path, year = year)

    for (g, af_filename, dp_filename) in zip(geographies, af_filenames, dp_filenames):

        # Allocation Files
        dfs[g] = readData(
            af_filename,
            file_path = file_path,
            na_values = 'Z',
            usecols = [f'{g}_CODE_{year}', f'{g}_NAME_{year}', f'STATE_CODE_{year}'],
            dtype = {f'{g}_CODE_{year}': 'string'},
            get_csv = get_csv,
        )
        
        dfs[g].columns = [x.removeprefix(f'{g}_').removesuffix(f'_{year}') for x in dfs[g].columns]

        # Census DataPacks
        df = readData(
            dp_filename,
            file_path = file_path,
            na_values = 'Z',
            usecols = [f'{g}_CODE_{year}', 'Tot_P_P'],
            dtype = {f'{g}_CODE_{year}': 'string'},
            get_csv = get_csv,
        )
        
        df.columns = [x.removeprefix(f'{g}_').removesuffix(f'_{year}') for x in df.columns]

        # Remove code prefix to join DataFrames
        df['CODE'] = df['CODE'].apply(lambda x: x.removeprefix(g))

        # Join DataFrames
        dfs[g] = dfs[g].join(
            df.set_index('CODE'),
            on = 'CODE',
            how = 'left',
        ).dropna(how = 'any').drop_duplicates()
        
    return dfs


# Function for getting populations

def getPopulations(df, geography_df, geography):

    for i in df[df['Type'] == geography].index:

        # Get code
        df.loc[i, 'Code'] = geography_df[geography_df['NAME'] == df.loc[i, 'Name']]['CODE'].values[0]

        # Get population
        df.loc[i, 'Population'] = geography_df[geography_df['CODE'] == df.loc[i, 'Code']]['Tot_P_P'].values[0]

    return df


# Function for getting population data using ABS data

def getPopulationData(filename, file_path = 'assets', abs_data_file_path = 'ABS_Data',
                      geographies = [], year = 2021, get_csv = True, download = False):

    print("getPopulationData()")
    
    # Read data from files

    # Folder for data related to population
    abs_data_file_path = filePath(abs_data_file_path, file_path = file_path)
    if not os.path.isdir(abs_data_file_path):
        os.makedirs(abs_data_file_path)
        download = True

    ## Relevant areas
    filename = filePath(filename, file_path = file_path)
    df = readData(filename, get_csv = get_csv)
    
    if download:
        downloadABSData(geographies, file_path = abs_data_file_path, year = year)

    # ABS data
    dfs = loadABSData(
        file_path = abs_data_file_path,
        geographies = geographies,
        year = year,
        get_csv = get_csv,
        download = download,
    )


    # Clean data

    # Strip trailing whitespace from names
    df['Name'] = df['Name'].apply(lambda x: x.strip())

    for i in geographies:

        # Convert state codes to int
        dfs[i]['STATE_CODE'] = dfs[i]['STATE_CODE'].fillna(0).astype('int')

        # Limit records to WA
        dfs[i] = dfs[i][dfs[i]['STATE_CODE'] == 5].drop_duplicates().drop(columns = 'STATE_CODE')

        # Strip trailing whitespace from names
        dfs[i]['NAME'] = dfs[i]['NAME'].apply(lambda x: x.strip())

    # Add code and population columns
    df['Code'] = str()
    df['Population'] = int()


    # Extract population data

    # Get codes and populations
    for i in geographies:
        df = getPopulations(df, dfs[i], i)

    # Sum populations for each region
    name_cols = ['State', 'Region', 'District']
    pop_df = df[name_cols + ['Population']]
    pop_df = pop_df.groupby(by = name_cols, observed = False, as_index = False).sum()
    pop_df[name_cols] = pop_df[name_cols].apply(lambda x: x.str.upper())

    # Write population data to Excel file
    writeToFile(df, 'RegionMapping.csv', file_path = file_path)
    #writeToFile(pop_df, 'RegionPopulations.csv', file_path = abs_data_file_path, index = True)

    return(pop_df)