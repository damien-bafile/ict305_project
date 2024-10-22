### DataLoading.py ###

import os

from helpers.CrimeData import downloadDataset, getCrimeData
from helpers.PopulationData import downloadABSData


# Function to download data

def downloadData(filename = 'data.xlsx', file_path = 'assets', abs_file_path = 'ABS_Data',
                 geographies = ['LGA', 'SA3', 'SAL'], year = 2021, check_first = True):
    
    if os.path.dirname(filename) == file_path:
        filename = os.path.basename(filename)
    
    if os.path.dirname(abs_file_path) != file_path:
        abs_file_path = os.path.join(file_path, abs_file_path)
    
    downloadDataset(filename, file_path = file_path, check_first = check_first)
    downloadABSData(geographies, file_path = abs_file_path, year = year, check_first = check_first)


# Function to load and process data

def loadData(filename = 'data', file_path = 'assets', sheet_name = 'Data'):

    if os.path.dirname(filename) == file_path:
        filename = os.path.basename(filename)

    crimes_df = getCrimeData(
        filename,
        file_path = file_path,
        sheet_name = sheet_name,
        get_csv = True,
        download = True,
        write_new_csvs = True,
    )
    
    return crimes_df