### FileIO.py ###

'''
ICT305: Data Visualisation and Simulation
Group Project
Group Name: Machine Masters
Eren Stannard - 34189185
'''


from os import path
import pandas as pd
import requests
from bs4 import BeautifulSoup
from zipfile import ZipFile
import json
import geojson

from datetime import datetime
from calendar import timegm


# Function for getting HTML data

def getHTMLData(url, href = None, session = None):

    if href:
        url += href

    if session:
        html_data = session.get(url).text
    else:
        html_data = requests.get(url).text
    
    soup = BeautifulSoup(html_data, 'lxml')

    return soup


# Function for trying to get a .csv file

def getCSV(filename, sheet_name = 0, skiprows = None, na_values = None, index_col = None,
           usecols = None, dtype = None, header = 0):
    
    fn = filename

    for ext in ['.csv', '.xlsx']:
        fn = fn.removesuffix(ext)
    
    csv = path.isfile(f'{fn}.csv')
    xlsx = path.isfile(f'{fn}.xlsx')

    if ((xlsx and not csv) or
        ((csv and xlsx) and (path.getmtime(f'{fn}.csv') < path.getmtime(f'{fn}.xlsx')))):
        df = readData(
            f'{fn}.xlsx', sheet_name = sheet_name, skiprows = skiprows, na_values = na_values,
            index_col = index_col, usecols = usecols, dtype = dtype, header = header,
        )
        writeToFile(df, f'{path.basename(fn)}.csv', file_path = path.dirname(filename))
    
    if xlsx or csv:
        filename = f'{fn}.csv'

    return filename


# Function for reading data from a file

def readData(filename, file_path = None, sheet_name = 0, skiprows = None, na_values = None,
             index_col = None, usecols = None, dtype = None, header = 0, get_csv = False):

    data = None

    if file_path and (file_path != path.dirname(filename)):
        filename = path.join(file_path, filename)

    if get_csv:
        filename = getCSV(
            filename, sheet_name = sheet_name, skiprows = skiprows, na_values = na_values,
            index_col = index_col, usecols = usecols, dtype = dtype, header = header,
        )

    if path.isfile(filename):

        if filename.endswith('.csv'):
            data = pd.read_csv(
                filename, skiprows = skiprows, na_values = na_values, index_col = index_col,
                usecols = usecols, dtype = dtype, header = header, low_memory = False,
            )

        elif filename.endswith('.xlsx'):
            data = pd.read_excel(
                filename, sheet_name = sheet_name, skiprows = skiprows, na_values = na_values,
                index_col = index_col, usecols = usecols, dtype = dtype, header = header,
            )
            
        elif filename.endswith('.json'):
            with open(filename, 'r') as file:
                data = json.load(file)

        elif filename.endswith('.geojson'):
            with open(filename, 'r') as file:
                data = geojson.load(file)
    
        else:
            print("Error: Invalid file type.\n")

    else:
        print(f"Error: Could not open file {filename}.\n")

    return data


# Function for reading data from a .zip file

def readZIPData(filename, file_path = None, sheet_name = 0, skiprows = None, na_values = None,
                index_col = None, usecols = None, dtype = None, header = 0):

    data = None

    if path.isfile(file_path):

        if file_path.endswith('.zip') and filename.endswith('.csv'):
            with ZipFile(file_path) as z:
                with z.open(filename) as f:
                    data = pd.read_csv(
                        f, skiprows = skiprows, na_values = na_values, index_col = index_col,
                        usecols = usecols, dtype = dtype, header = header, low_memory = False,
                    )
                    
        else:
            print("Error: Invalid file type.\n")

    else:
        print("Error: Could not open file.\n")

    return data


# Function for writing data to a file

def writeToFile(data, filename, file_path = None, index = False, columns = None):

    if file_path:
        filename = path.join(file_path, filename)

    if filename.endswith('.csv'):
        data.to_csv(filename, index = index, columns = columns)

    elif filename.endswith('.xlsx'):
        data.to_excel(filename, index = index, columns = columns)

    else:
        print("Error: Invalid file type.\n")

    return