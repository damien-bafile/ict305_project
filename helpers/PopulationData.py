### PopulationData.py ###

'''
ICT305: Data Visualisation and Simulation
Group Assignment
Group Name: Machine Masters
Dataset Analysis: Data Exploration and Discovery
Eren Stannard - 34189185
'''


# Import libraries

import numpy as np
import pandas as pd

from helpers.FileIO import *


# Function for getting populations

def getPopulations(df, area_type_df, area_type):

    for i in df[df['Type'] == area_type].index:

        # Get code
        df.loc[i, 'Code'] = area_type_df[area_type_df['NAME'] == df.loc[i, 'Name']]['CODE'].values[0]

        # Get population
        df.loc[i, 'Population'] = area_type_df[area_type_df['CODE'] == df.loc[i, 'Code']]['Tot_P_P'].values[0]

    return df


# Function for loading ABS data

def loadABSData(file_path = None, area_types = [], year = 2021, na_values = 'Z', usecols = None):

    dfs = dict.fromkeys(area_types)

    for i in area_types:

        # Allocation Files
        dfs[i] = readData(
            f'{i}_{year}_AUST.csv',
            file_path = f'{file_path}/ABS_Allocation_Files',
            na_values = 'Z',
            usecols = [f'{i}_CODE_{year}', f'{i}_NAME_{year}', f'STATE_CODE_{year}'],
            dtype = {f'{i}_CODE_{year}': 'string'},
        )
        
        dfs[i].columns = [j.removeprefix(f'{i}_').removesuffix(f'_{year}') for j in dfs[i].columns]

        # Census DataPacks
        df = readData(
            f'{year}Census_G01_WA_{i}.csv',
            file_path = f'{file_path}/ABS_Census_DataPacks',
            na_values = 'Z',
            usecols = [f'{i}_CODE_{year}', 'Tot_P_P'],
            dtype = {f'{i}_CODE_{year}': 'string'},
        )
        
        df.columns = [j.removeprefix(f'{i}_').removesuffix(f'_{year}') for j in df.columns]

        # Remove code prefix to join DataFrames
        df['CODE'] = df['CODE'].apply(lambda x: x.removeprefix(i))

        # Join DataFrames
        dfs[i] = dfs[i].join(df.set_index('CODE'), on = 'CODE', how = 'left').dropna(how = 'any')
        
    return dfs


def getPopulationData(filename, file_path = None):

    # Read data from files

    pop_data_file_path = f'{file_path}/Region_Population_Data'
    area_types = ['LGA', 'SA3', 'SAL']
    year = 2021

    ## Relevant areas
    df = readData(filename, file_path = pop_data_file_path)

    # ABS data
    dfs = loadABSData(file_path = file_path, area_types = area_types, year = year)


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


    # Get codes and populations

    for i in area_types:
        df = getPopulations(df, dfs[i], i)


    # Sum populations for each region

    pops = df[['District', 'Region', 'State', 'Population']]
    pops = pops.groupby(by = ['State', 'Region', 'District'], observed = False, as_index = False).sum()
    pops[['State', 'Region', 'District']] = pops[['State', 'Region', 'District']].apply(lambda x: x.str.upper())
    pop_df = pops[['District', 'Region', 'State', 'Population']]


    # Write population data to Excel file

    writeToFile(df, 'RegionMapping.csv', file_path = pop_data_file_path)
    #writeToFile(pop_df, 'RegionPopulations.csv', file_path = pop_data_file_path, index = True)

    return(pop_df)