### FileIO.py ###

'''
ICT305: Data Visualisation and Simulation
Group Project
Group Name: Machine Masters
Eren Stannard - 34189185
'''


import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
import geojson


# Function for getting file path

def filePath(filename, file_path = '', ext = False, split = False, split_ext = False):
    
    split_ext = split_ext and not ext

    if ((os.path.dirname(filename) != file_path) and
        ((filename != file_path) and
         (filename != os.path.basename(file_path)))):
        filename = os.path.join(file_path, filename)
    else:
        if filename == os.path.basename(file_path):
            filename = file_path

    if split_ext and split:
        head, tail = os.path.split(filename)
        root, ext = os.path.splitext(tail)
        filename = (head, root, ext)

    else:
        if split_ext:
            filename = os.path.splitext(filename)
        if split:
            filename = os.path.split(filename)

    return filename


# Function for getting HTML data

def getHTMLData(url, href = None, session = None, features = 'lxml', parse_only = None):

    print("getHTMLData()")

    if href:
        url += href

    if session:
        html_data = session.get(url).text
    else:
        html_data = requests.get(url).text
    
    soup = BeautifulSoup(
        markup = html_data,
        features = features,
        parse_only = parse_only,
    )

    return soup


# Function for checking for dataset updates

def checkFileUpdate(filename, processed_filename = None):

    print("checkFileUpdate()")

    filename = filePath(filename)
    
    if not processed_filename:
        root, _ = os.path.splitext(filename)
        processed_filename = f'{root}_Processed.csv'
        
    processing_update = not os.path.isfile(processed_filename)

    if not processing_update:
        file_mtime = os.path.getmtime(filename)
        processed_file_mtime = os.path.getmtime(processed_filename)
        processing_update = file_mtime > processed_file_mtime
        
    if processing_update:
        print(f"Data file {filename} updated.")

    return processing_update


# Function for trying to get a .csv file

def getCSV(filename, sheet_name = 0, skiprows = None, na_values = None, usecols = None,
           dtype = None, header = 0):
    
    print("getCSV()")
    
    filename = filePath(filename)
    root, _ = os.path.splitext(filename)

    csv_filename = f'{root}.csv'
    xlsx_filename = f'{root}.xlsx'
    
    csv = os.path.isfile(csv_filename)
    xlsx = os.path.isfile(xlsx_filename)

    processing_update = xlsx and checkFileUpdate(xlsx_filename, processed_filename = csv_filename)

    if processing_update:
        df = readData(
            xlsx_filename,
            sheet_name = sheet_name,
            skiprows = skiprows,
            na_values = na_values,
            usecols = usecols, 
            dtype = dtype,
            header = header,
        )
        writeToFile(df, csv_filename)
    
    if xlsx or csv:
        filename = csv_filename

    return filename


# Function for reading data from a file

def readData(filename, file_path = '', sheet_name = 0, skiprows = None, na_values = None,
             usecols = None, dtype = None, header = 0, get_csv = False):
    
    print("readData()")

    data = None
    filename = filePath(filename, file_path = file_path)

    params = dict(
        skiprows = skiprows,
        na_values = na_values,
        usecols = usecols,
        dtype = dtype,
        header = header,
    )

    if os.path.isfile(filename):

        if get_csv:
            filename = getCSV(
                filename, sheet_name = sheet_name, skiprows = skiprows, na_values = na_values,
                usecols = usecols, dtype = dtype, header = header,
            )

        _, ext = os.path.splitext(filename)

        match ext:

            case '.csv':
                data = pd.read_csv(filename, **params, low_memory = False)

            case '.xlsx':
                data = pd.read_excel(filename, **params, sheet_name = sheet_name)

            case '.json':
                with open(filename, 'r') as file:
                    data = json.load(file)

            case '.geojson':
                with open(filename, 'r') as file:
                    data = geojson.load(file)

            case _:
                print(f"Error: Invalid file type '{ext}'.\n")

    else:
        print(f"Error: Could not open file '{filename}'.\n")

    return data


# Function for writing data to a file

def writeToFile(data, filename, file_path = '', index = False, columns = None):

    print("writeToFile()")

    filename, ext = filePath(filename, file_path = file_path, split_ext = True)

    match ext:
        case '.csv':
            data.to_csv(f'{filename}.csv', index = index, columns = columns)
            print(f"{filename}.csv file written.")
        case '.xlsx':
            data.to_excel(f'{filename}.xlsx', index = index, columns = columns)
            print(f"{filename}.xlsx file written.")
        case _:
            print(f"Error: Invalid file type '{ext}'.\n")

    return