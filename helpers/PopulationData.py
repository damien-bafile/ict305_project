### PopulationData.py ###

'''
ICT305: Data Visualisation and Simulation
Group Assignment
Group Name: Machine Masters
Eren Stannard - 34189185
'''


# Import libraries

from os import path, makedirs
import numpy as np
import pandas as pd
import requests
from zipfile import ZipFile

from helpers.FileIO import *


# Function for loading ABS data

def loadABSData(file_path = '', area_types = [], year = 2021, na_values = 'Z', usecols = None, get_csv = True):

    dfs = dict.fromkeys(area_types)

    #downloadABSData(area_types, file_path = file_path, year = year)

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

def getPopulationData(filename, file_path = '', area_types = [], year = 2021, get_csv = True):

    # Read data from files

    # Folder for data related to population
    abs_data_file_path = path.join(file_path, 'ABS_Data')
    if not path.isdir(abs_data_file_path):
        makedirs(abs_data_file_path)

    ## Relevant areas
    df = readData(filename, file_path = file_path, get_csv = get_csv)

    # ABS data
    dfs = loadABSData(file_path = abs_data_file_path, area_types = area_types, year = year, get_csv = get_csv)


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
    pops = df[['District', 'Region', 'State', 'Population']]
    pops = pops.groupby(by = ['State', 'Region', 'District'], observed = False, as_index = False).sum()
    pops[['State', 'Region', 'District']] = pops[['State', 'Region', 'District']].apply(lambda x: x.str.upper())
    pop_df = pops[['District', 'Region', 'State', 'Population']]

    # Write population data to Excel file
    writeToFile(df, 'RegionMapping.csv', file_path = file_path)
    #writeToFile(pop_df, 'RegionPopulations.csv', file_path = abs_data_file_path, index = True)

    return(pop_df)