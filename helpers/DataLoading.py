### DataLoading.py ###

'''
ICT305: Data Visualisation and Simulation
Group Project
Group Name: Machine Masters
Eren Stannard - 34189185
'''


import os
from time import time

from helpers.CrimeData import downloadDataset, getCrimeData
from helpers.PopulationData import downloadABSData
from helpers.FileIO import filePath


# Function to download data

def downloadData(filename = 'data.xlsx', file_path = 'assets', abs_file_path = 'ABS_Data',
                 geographies = ['LGA', 'SA3', 'SAL'], year = 2021, check_first = True):
    
    t0 = time()
    
    filename = filePath(filename, file_path = file_path)
    abs_file_path = filePath(abs_file_path, file_path = file_path)
    
    dataset_downloaded = downloadDataset(filename, check_first = check_first)
    abs_data_downloaded = downloadABSData(geographies, file_path = abs_file_path, year = year)
    
    if dataset_downloaded or abs_data_downloaded:
        loadData(filename = filename, geographies = geographies, year = year)
    
    t1 = time()
    print("downloadData(): %.3fs" % (t1 - t0))


# Function to load and process data

def loadData(filename = 'data.xlsx', file_path = 'assets', sheet_name = 'Data', get_csv = True,
             geographies = ['LGA', 'SA3', 'SAL'], year = 2021):
    
    t0 = time()

    filename = filePath(filename, file_path = file_path)
    
    if not os.path.isfile(filename):
        downloadDataset(filename)

    crimes_df = getCrimeData(
        filename,
        sheet_name = sheet_name,
        get_csv = get_csv,
        geographies = geographies,
        year = year,
    )

    t1 = time()
    print("loadData(): %.3fs" % (t1 - t0))
    
    return crimes_df