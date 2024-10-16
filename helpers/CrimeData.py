### DataPreProcessing.py ###

'''
ICT305: Data Visualisation and Simulation
Group Assignment
Group Name: Machine Masters
Dataset Analysis: Data Exploration and Discovery
Eren Stannard - 34189185
'''


# Import libraries

from os import path
import numpy as np
import pandas as pd

from helpers.FileIO import *
from helpers.PopulationData import getPopulationData


def loadCrimeData(filename, file_path = None, sheet_name = None):

    if file_path:
        filename = path.join(file_path, filename)
        
    for ext in ['.csv', '.xlsx']:
        if filename.endswith(ext):
            filename = filename.removesuffix(ext)
            break

    if path.isfile(f'{filename}.csv') and path.getmtime(f'{filename}.csv') >= path.getmtime(f'{filename}.xlsx'):
        df = readData(f'{filename}.csv')
    else:
        df = readData(f'{filename}.xlsx', sheet_name = sheet_name)
        writeToFile(df, f'{filename}.csv')
        df = readData(f'{filename}.csv')

    return df


def getCrimeData(filename, file_path = None, sheet_name = 'Data'):

    # Load crime data

    crimes_df = loadCrimeData(filename, file_path = file_path, sheet_name = sheet_name)


    # Transform data

    # Drop unnecessary columns

    crimes_df = crimes_df.drop(columns = [
        'WAPOL_Hierarchy_order_Lvl1', 'WAPOL_Hierarchy_order_Lvl2',
        'Year', 'Key', 'MonthYear1', 'prod_dte',
    ])


    # Rename columns

    crimes_df = crimes_df.rename(columns = {
        'Website Region': 'District',
        'WAPOL_Hierarchy_Lvl2': 'Crime',
        'WAPOL_Hierarchy_Lvl1': 'Sub_Crime',
    })


    # Insert separate month and year columns

    crimes_df['Period'] = pd.to_datetime(crimes_df['Period'])
    crimes_df.insert(3, 'Month', crimes_df['Period'].dt.month_name())
    crimes_df.insert(3, 'Year', crimes_df['Period'].dt.year)


    # Fill Count NA values with 0 and convert dtype to int

    crimes_df['Count'] = crimes_df['Count'].fillna(0).astype('int')


    # Load population data to scale crime data

    pop_df = getPopulationData('RegionListing.csv', file_path = file_path)


    # Join crimes_df with pop_df

    crimes_df = crimes_df.join(pop_df.set_index('District'), on = 'District', how = 'left').dropna()

    '''for col in ['State', 'Region', 'District']:
        crimes_df[col] = crimes_df[col].apply(lambda x: x.removesuffix(x.split()[-1]).strip().title())
    
    crimes_df['Region'] = crimes_df['Region'].apply(lambda x: ' '.join([x.split()[0], x.split()[-1].upper()]) if x.split()[-1] == 'Wa' else x)'''


    # Scale Count according to population

    crimes_df['Count_Per_100'] = (crimes_df['Count'] / (crimes_df['Population'] / 100))


    # Write .csv files

    # Processed data
    writeToFile(crimes_df, f'{filename} (Processed).csv', file_path = f'{file_path}')

    '''# 1 file sorted by date -> disrict -> crime
    crimes_df_sorted = crimes_df.sort_values(by = ['Period', 'District', 'Crime'], ignore_index = True)
    writeToFile(crimes_df_sorted, f'{filename} (All Crimes).csv', file_path = f'{file_path}/csvs')

    # Separate files for each crime
    crimes_df_sorted = dict.fromkeys(crimes_df['Crime'].unique())
    for crime in crimes_df_sorted:
        crimes_df_sorted[crime] = crimes_df[crimes_df['Crime'] == crime].sort_values(by = ['Period', 'District'], ignore_index = True)
        writeToFile(crimes_df_sorted[crime], f'{filename} ({crime}).csv', file_path = f'{file_path}/csvs')'''


    return crimes_df