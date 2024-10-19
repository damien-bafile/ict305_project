### DataPreProcessing.py ###

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

from helpers.FileIO import *
from helpers.PopulationData import getPopulationData


# Function for loading crime dataset

def loadCrimeData(filename, file_path = '', sheet_name = None, get_csv = True):

    for ext in ['.csv', '.xlsx']:
        filename = filename.removesuffix(ext)
    
    filename = f'{path.join(file_path, filename)}.xlsx'

    #downloadDataset(filename)
    
    df = readData(filename, file_path = file_path, sheet_name = sheet_name, get_csv = get_csv)

    return df


# Function for getting processed crime data

def getCrimeData(filename, file_path = '', sheet_name = 'Data', include_sub_crimes = False, get_csv = True):

    # Load crime dataset
    crimes_df = loadCrimeData(filename, file_path = file_path, sheet_name = sheet_name, get_csv = get_csv)


    # Clean and transform data

    # Drop unnecessary columns
    crimes_df = crimes_df.drop(
        columns = [
            'WAPOL_Hierarchy_order_Lvl1',
            'WAPOL_Hierarchy_order_Lvl2',
            'Year',
            'Key',
            'MonthYear1',
            'prod_dte',
        ]
    )

    # Rename columns
    crimes_df = crimes_df.rename(
        columns = {
            'Website Region': 'District',
            'WAPOL_Hierarchy_Lvl2': 'Crime',
            'WAPOL_Hierarchy_Lvl1': 'Sub_Crime',
        }
    )
    
    # Drop Sub_Crime if passed
    if not include_sub_crimes:
        crimes_df = crimes_df.drop(columns = 'Sub_Crime')

    # Insert separate month and year columns
    crimes_df['Period'] = pd.to_datetime(crimes_df['Period'])
    crimes_df.insert(3, 'Month', crimes_df['Period'].dt.month_name())
    crimes_df.insert(3, 'Year', crimes_df['Period'].dt.year)

    # Fill Count NA values with 0 and convert dtype to int
    crimes_df['Count'] = crimes_df['Count'].fillna(0).astype('int')

    # Load population data to scale crime data

    # Get population data
    pop_df = getPopulationData(
        'RegionListing.csv',
        file_path = file_path,
        area_types = ['LGA', 'SA3', 'SAL'],
        get_csv = get_csv,
    )

    # Join crimes_df with pop_df
    crimes_df = crimes_df.join(pop_df.set_index('District'), on = 'District', how = 'left').dropna()

    # Scale Count according to population
    crimes_df['Count_Per_100'] = (crimes_df['Count'] / (crimes_df['Population'] / 100))


    # Write processed data to .csv files

    # Processed data
    writeToFile(crimes_df, f'{filename}_Processed.csv', file_path = file_path)
    
    # File path to write sorted .csv files
    csv_file_path = path.join(file_path, 'CSVs')
    if not path.isdir(csv_file_path):
        makedirs(csv_file_path)

    # 1 file sorted by date -> disrict -> crime
    crimes_df_sorted = crimes_df.sort_values(by = ['Period', 'District', 'Crime'], ignore_index = True)
    writeToFile(crimes_df_sorted, f'{filename}_All_Crimes.csv', file_path = csv_file_path)
    
    # 1 file grouped by crime
    crimes_df_sorted_totals = crimes_df_sorted.drop(columns = ['Period', 'Month', 'Year'])
    crimes_df_sorted_totals = crimes_df_sorted_totals.groupby(
        by = [x for x in crimes_df_sorted_totals.columns if not x.startswith('Count')],
        observed = False,
        as_index = False,
    ).sum().sort_values(
        by = 'Count_Per_100',
        ascending = False,
    )
    writeToFile(crimes_df_sorted_totals, f'{filename}_All_Crimes_Totals.csv', file_path = csv_file_path)

    # Separate files for each crime
    for crime in crimes_df['Crime'].unique():
        writeToFile(crimes_df_sorted[crimes_df_sorted['Crime'] == crime], f'{filename}_{crime}.csv', file_path = csv_file_path)


    return crimes_df


# Function for getting crime counts for a region

def getCrimeCounts(df, scale = 'District', area = None, ascending = False):

    if area:
        df = df[df[scale].str.contains(area.upper())]

    df = df[[scale, 'Crime', 'Count_Per_100']].groupby(
        by = [scale, 'Crime'],
        observed = False,
        as_index = False,
    ).sum().sort_values(
        by = 'Count_Per_100',
        ascending = ascending,
    )
    
    return df


# File to just run everything

def loadDataset():

    filename = 'WA Police Force Crime Timeseries'
    file_path = 'assets'
    sheet_name = 'Data'

    crimes_df = getCrimeData(filename, file_path = file_path, sheet_name = sheet_name)
    
    return crimes_df