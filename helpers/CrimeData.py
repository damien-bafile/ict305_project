### CrimeData.py ###

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
from bs4 import SoupStrainer

from calendar import timegm
from datetime import datetime

from helpers.FileIO import *
from helpers.PopulationData import getPopulationData


# Function for checking for dataset updates

def checkDatasetUpdate(filename, processed_filename = None):

    print("checkDatasetUpdate()")
    
    url = "https://www.wa.gov.au/organisation/western-australia-police-force/crime-statistics#/start"

    filename = filePath(filename)

    download_update = not os.path.isfile(filename)

    if not download_update:
        file_mtime = os.path.getmtime(filename)
        soup = getHTMLData(url, parse_only = SoupStrainer(class_ = 'page-reviewed'))
        last_update = timegm(datetime.timetuple(datetime.fromisoformat(soup.time['datetime'])))

        # True if webpage has been updated since last dataset download
        download_update = last_update > file_mtime
    
    processing_update = download_update or checkFileUpdate(filename, processed_filename = processed_filename)
    
    if processing_update:
        print(f"Data file {filename} updated on website.")

    return processing_update, download_update


# Function for downloading crime dataset

def downloadDataset(filename, file_path = 'assets', check_first = True):

    print("downloadDataset()")
    
    download, downloaded = True, False
    url = "https://www.wa.gov.au/media/48429/download?inline?inline="
    filename, _ = filePath(filename, file_path = file_path, split_ext = True)
    filename = f'{filename}.xlsx'

    if check_first:
        _, download_update = checkDatasetUpdate(filename)
        download = download_update

    if download:
        print(f"Downloading {filename} dataset...")
        response = requests.get(url)
        with open(filename, 'wb') as f:
            f.write(response.content)
            downloaded = True
    else:
        print("Dataset already downloaded.")
        
    return downloaded


# Function for loading crime dataset

def loadCrimeData(filename, file_path = 'assets', sheet_name = 'Data', get_csv = True, download = False):

    print("loadCrimeData()")

    filename, _ = filePath(filename, file_path = file_path, split_ext = True)
    filename = f'{filename}.xlsx'
    exists = os.path.isfile(filename)

    if download or not exists:
        downloadDataset(filename, check_first = exists)
    
    df = readData(
        filename,
        sheet_name = sheet_name,
        get_csv = get_csv,
    )

    return df


# Function for processing crime data

def processCrimeData(filename, file_path = 'assets', sheet_name = 'Data', include_sub_crimes = False,
                     get_csv = True, write_new_csvs = True):
    
    print("processCrimeData()")
    
    file_path, filename = filePath(filename, file_path = file_path, split = True)

    # Load crime dataset
    crimes_df = loadCrimeData(
        filename,
        file_path = file_path,
        sheet_name = sheet_name,
        get_csv = get_csv,
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
    
    filename, _ = os.path.splitext(filename)

    # Processed data
    writeToFile(crimes_df, f'{filename}_Processed.csv', file_path = file_path)

    # File path to write sorted .csv files
    csv_file_path = filePath('CSVs', file_path = file_path)
    if not os.path.isdir(csv_file_path):
        os.makedirs(csv_file_path)
        write_new_csvs = True

    if not (os.path.isfile(f'{filename}_All_Crimes_Sorted.csv') and
            os.path.isfile(f'{filename}_All_Crimes_Totals_Sorted.csv')):
        write_new_csvs = True
    
    if write_new_csvs:

        print("Writing new .csv files...")
    
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

        '''# Separate files for each crime
        for crime in crimes_df['Crime'].unique():
            writeToFile(
                crimes_df_sorted[crimes_df_sorted['Crime'] == crime],
                f'{filename}_{crime}_Sorted.csv',
                file_path = csv_file_path,
            )'''

    return crimes_df


# Function for getting processed crime data

def getCrimeData(filename, file_path = 'assets', sheet_name = 'Data', include_sub_crimes = False,
                 get_csv = True, download = False, check_first = True, write_new_csvs = False):
    
    print("getCrimeData()")
    
    write_new_csvs = download

    filename = filePath(filename, file_path = file_path)
    root, _ = os.path.splitext(filename)
    processed_filename = f'{root}_Processed.csv'

    processing_update, download_update = write_new_csvs, download

    if check_first:
        processing_update, download_update = checkDatasetUpdate(filename, processed_filename = processed_filename)

    if not (processing_update or download_update):
        crimes_df = readData(processed_filename)
        print(f"Data file {processed_filename} loaded.")
    
    else:
        if download_update:
            downloadDataset(filename, check_first = False)
        
        # Load crime dataset
        crimes_df = processCrimeData(
            filename,
            sheet_name = sheet_name,
            get_csv = get_csv,
        )
        print(f"Data file {filename} loaded and pre-processed.")

    return crimes_df


# Function for getting crime counts for a region

def getCrimeCounts(df, group_by = [], sort = True, sort_by = [], area_scale = 'District',
                   area = None, ascending = False):

    if area:
        df = df[df[area_scale].str.contains(area.upper())]
    
    for i in [area_scale, f'{area_scale}_Name', 'Crime']:
        if i in df.columns and i not in group_by:
            group_by = group_by + [i]
    
    if 'Count_Per_100' not in sort_by:
        sort_by = sort_by + ['Count_Per_100']

    df = df[group_by + sort_by].groupby(
        by = group_by,
        observed = False,
        as_index = False,
    ).sum()
    
    if sort:
        df = df.sort_values(
            by = sort_by,
            ascending = ascending,
        )
    
    return df