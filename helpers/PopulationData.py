### PopulationData.py ###

'''
ICT305: Data Visualisation and Simulation
Group Assignment
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

def downloadABSData(geographies, file_path = '', year = 2021, check_first = True):
    
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
        if not os.path.isfile(os.path.join(file_path, filename)):
            print(f"Downloading {filename}...")
            response = session.get(f'{af_url}/{filename}')
            with open(os.path.join(file_path, filename), 'wb') as f:
                f.write(response.content)
        else:
            print(f"{filename} already downloaded.")

    # Download Census DataPacks
    for (filename, member_name) in zip(dp_zip_filenames, dp_filenames):
        if not os.path.isfile(os.path.join(file_path, member_name)):
            print(f"Downloading {filename}...")
            response = session.get(f'{dp_url}/{filename}')
            with ZipFile(BytesIO(response.content)) as z:
                member_path = [x for x in z.namelist() if x.endswith(member_name)][0]
                with open(os.path.join(file_path, member_name), 'wb') as f:
                    f.write(z.read(member_path))
        else:
            print(f"{member_name} already downloaded.")


# Function for loading ABS data

def loadABSData(file_path = '', area_types = [], year = 2021, get_csv = True, download = False):

    dfs = dict.fromkeys(area_types)

    if download:
        downloadABSData(area_types, file_path = file_path, year = year)

    for i in area_types:

        # Allocation Files
        dfs[i] = readData(
            f'{i}_{year}_AUST.csv',
            file_path = file_path,
            na_values = 'Z',
            usecols = [f'{i}_CODE_{year}', f'{i}_NAME_{year}', f'STATE_CODE_{year}'],
            dtype = {f'{i}_CODE_{year}': 'string'},
            get_csv = get_csv,
        )
        
        dfs[i].columns = [j.removeprefix(f'{i}_').removesuffix(f'_{year}') for j in dfs[i].columns]

        # Census DataPacks
        df = readData(
            f'{year}Census_G01_WA_{i}.csv',
            file_path = file_path,
            na_values = 'Z',
            usecols = [f'{i}_CODE_{year}', 'Tot_P_P'],
            dtype = {f'{i}_CODE_{year}': 'string'},
            get_csv = get_csv,
        )
        
        df.columns = [j.removeprefix(f'{i}_').removesuffix(f'_{year}') for j in df.columns]

        # Remove code prefix to join DataFrames
        df['CODE'] = df['CODE'].apply(lambda x: x.removeprefix(i))

        # Join DataFrames
        dfs[i] = dfs[i].join(
            df.set_index('CODE'),
            on = 'CODE',
            how = 'left',
        ).dropna(how = 'any').drop_duplicates()
        
    return dfs


# Function for getting populations

def getPopulations(df, area_type_df, area_type):

    for i in df[df['Type'] == area_type].index:

        # Get code
        df.loc[i, 'Code'] = area_type_df[area_type_df['NAME'] == df.loc[i, 'Name']]['CODE'].values[0]

        # Get population
        df.loc[i, 'Population'] = area_type_df[area_type_df['CODE'] == df.loc[i, 'Code']]['Tot_P_P'].values[0]

    return df


# Function for getting population data using ABS data

def getPopulationData(filename, file_path = '', area_types = [], year = 2021, get_csv = True, download = False):

    # Read data from files

    # Folder for data related to population
    abs_data_file_path = os.path.join(file_path, 'ABS_Data')
    if not os.path.isdir(abs_data_file_path):
        os.makedirs(abs_data_file_path)
        download = True

    ## Relevant areas
    df = readData(filename, file_path = file_path, get_csv = get_csv)
    
    if download:
        downloadABSData(area_types, file_path = file_path, year = year)

    # ABS data
    dfs = loadABSData(
        file_path = abs_data_file_path,
        area_types = area_types,
        year = year,
        get_csv = get_csv,
        download = download,
    )


    # Clean data

    # Strip trailing whitespace from names
    df['Name'] = df['Name'].apply(lambda x: x.strip())

    for i in area_types:

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
    for i in area_types:
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