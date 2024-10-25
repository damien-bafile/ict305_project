### DataLoading.py ###

'''
ICT305: Data Visualisation and Simulation
Group Project
Group Name: Machine Masters
Eren Stannard - 34189185
'''


import os

from helpers.CrimeData import downloadDataset, getCrimeData
from helpers.PopulationData import downloadABSData
from helpers.FileIO import *


# Function to download data

def downloadData(filename = 'data.xlsx', file_path = 'assets', abs_file_path = 'ABS_Data',
                 geographies = ['LGA', 'SA3', 'SAL'], year = 2021, check_first = True):
    
    print("downloadData()")
    
    filename = filePath(filename, file_path = file_path)
    abs_file_path = filePath(abs_file_path, file_path = file_path)
    
    dataset_downloaded = downloadDataset(filename, check_first = check_first)
    abs_data_downloaded = downloadABSData(geographies, file_path = abs_file_path, year = year, check_first = check_first)
    
    if dataset_downloaded or abs_data_downloaded:
        loadData(filename = filename)


# Function to load and process data

def loadData(filename = 'data.xlsx', file_path = 'assets', sheet_name = 'Data', get_csv = True,
             download = False, write_new_csvs = True):
    
    print("loadData()")

    filename = filePath(filename, file_path = file_path)

    crimes_df = getCrimeData(
        filename,
        sheet_name = sheet_name,
        get_csv = get_csv,
        download = download,
        write_new_csvs = write_new_csvs,
    )
    
    return crimes_df