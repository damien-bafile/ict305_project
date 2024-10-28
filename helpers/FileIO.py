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
import json
import geojson
from bs4 import BeautifulSoup
from time import time


# Function for getting file path

def filePath(filename, file_path = '', split = False, split_ext = False):

    #t0 = time()
    #print("filePath()")

    if len(file_path) != 0:
        name_in_path = filename == os.path.basename(file_path)
        if name_in_path:
            filename = file_path
        else:
            common_path = os.path.commonpath([file_path, filename])
            if len(common_path) == 0:
                filename = os.path.join(file_path, filename)
            else:
                path_in_name = file_path == os.path.dirname(filename)
                same_path = filename == file_path
                if not (path_in_name or same_path):
                    filename = os.path.join(file_path, filename)

    if split_ext or split:
        if split_ext and split:
            head, tail = os.path.split(filename)
            root, ext = os.path.splitext(tail)
            filename = (head, root, ext)
        else:
            if split_ext:
                filename = os.path.splitext(filename)
            else:
                filename = os.path.split(filename)
    
    #t1 = time()
    #print("filePath(): %.3fs" % (t1 - t0))

    return filename


# Function for getting HTML data

def getHTMLData(url, href = None, session = None, features = 'lxml', parse_only = None):

    t0 = time()

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

    t1 = time()
    print("getHTMLData(): %.3fs" % (t1 - t0))

    return soup


# Function for checking for dataset updates

def checkFileUpdate(filename, processed_filename = None):

    t0 = time()
    
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
    
    t1 = time()
    print("checkFileUpdate(): %.3fs" % (t1 - t0))

    return processing_update


# Function for trying to get a .csv file

def getCSV(filename, sheet_name = 0, skiprows = None, na_values = None, usecols = None,
           dtype = None, header = 0):
    
    t0 = time()

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

    t1 = time()
    print("getCSV(): %.3fs" % (t1 - t0))

    return filename


# Function for reading data from a file

def readData(filename, file_path = '', sheet_name = 0, skiprows = None, na_values = None,
             usecols = None, dtype = None, engine = 'calamine', header = 0, get_csv = False):
    
    t0 = time()

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

        print(f"Reading data from {filename}...")

        _, ext = os.path.splitext(filename)

        match ext:
            case '.csv':
                data = pd.read_csv(filename, **params, low_memory = False)
            case '.xlsx':
                data = pd.read_excel(filename, **params, sheet_name = sheet_name, engine = engine)
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
    
    t1 = time()
    print("readData(): %.3fs" % (t1 - t0))

    return data


# Function for writing data to a file

def writeToFile(data, filename, file_path = '', index = False, columns = None):

    t0 = time()

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
    
    t1 = time()
    print("writeToFile(): %.3fs" % (t1 - t0))

    return