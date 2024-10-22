### DataPreProcessing.py ###

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

from calendar import timegm
from datetime import datetime

from helpers.FileIO import *
from helpers.PopulationData import getPopulationData


# Function for checking for dataset updates

def checkDatasetUpdate(filename, url):
    
    file_mtime = os.path.getmtime(filename)
    soup = getHTMLData(url)
    last_update_time = soup.find(class_ = 'page-reviewed').time['datetime']
    last_update_time = timegm(datetime.timetuple(datetime.fromisoformat(last_update_time)))

    # Return True if webpage has been updated since last dataset download
    return last_update_time > file_mtime


# Function for downloading crime dataset

def downloadDataset(filename, file_path = '', check_first = True):
    
    download = True

    for ext in ['.csv', '.xlsx']:
        filename = filename.removesuffix(ext)
    filename = f'{os.path.join(file_path, filename)}.xlsx'

    url = "https://www.wa.gov.au"
    
    if check_first:
        cs_url = f"{url}/organisation/western-australia-police-force/crime-statistics#/start"
        if os.path.isfile(filename) and not checkDatasetUpdate(filename, cs_url):
            download = False

    if download:
        print("Downloading dataset...")
        dl_url = f"{url}/media/48429/download?inline?inline="
        response = requests.get(dl_url)
        with open(filename, 'wb') as f:
            f.write(response.content)
    else:
        print("Dataset already downloaded.")


# Function for loading crime dataset

def loadCrimeData(filename, file_path = '', sheet_name = None, get_csv = True, download = False):

    for ext in ['.csv', '.xlsx']:
        filename = filename.removesuffix(ext)
    
    filename = f'{os.path.join(file_path, filename)}.xlsx'

    if not not os.path.isfile(filename):
        download = True

    if download:
        downloadDataset(filename)
    
    df = readData(
        filename,
        file_path = file_path,
        sheet_name = sheet_name,
        get_csv = get_csv,
    )

    return df


# Function for getting processed crime data

def getCrimeData(filename, file_path = '', sheet_name = 'Data', include_sub_crimes = False,
                 get_csv = True, download = False, write_new_csvs = False):
    
    if download:
        write_new_csvs = True

    for ext in ['.csv', '.xlsx']:
        filename = filename.removesuffix(ext)

    # Load crime dataset
    crimes_df = loadCrimeData(
        filename,
        file_path = file_path,
        sheet_name = sheet_name,
        get_csv = get_csv,
        download = download,
    )


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
        geographies = ['LGA', 'SA3', 'SAL'],
        get_csv = get_csv,
        download = download,
    )

    # Join crimes_df with pop_df
    crimes_df = crimes_df.join(
        pop_df.set_index('District'),
        on = 'District',
        how = 'left',
    ).dropna()

    # Scale Count according to population
    crimes_df['Count_Per_100'] = (crimes_df['Count'] / (crimes_df['Population'] / 100))


    # Write processed data to .csv files

    # Processed data
    writeToFile(crimes_df, f'{filename}_Processed.csv', file_path = file_path)

    # File path to write sorted .csv files
    csv_file_path = os.path.join(file_path, 'CSVs')
    if not os.path.isdir(csv_file_path):
        os.makedirs(csv_file_path)
        write_new_csvs = True
    
    if write_new_csvs:
    
        # 1 file sorted by date -> disrict -> crime
        crimes_df_sorted = crimes_df.sort_values(
            by = ['Period', 'District', 'Crime'],
            ignore_index = True,
        )
        writeToFile(
            crimes_df_sorted,
            f'{filename}_All_Crimes_Sorted.csv',
            file_path = csv_file_path,
        )
        
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
        writeToFile(
            crimes_df_sorted_totals,
            f'{filename}_All_Crimes_Totals_Sorted.csv',
            file_path = csv_file_path,
        )

        # Separate files for each crime
        for crime in crimes_df['Crime'].unique():
            writeToFile(
                crimes_df_sorted[crimes_df_sorted['Crime'] == crime],
                f'{filename}_{crime}_Sorted.csv',
                file_path = csv_file_path,
            )


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