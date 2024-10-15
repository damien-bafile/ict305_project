### FileIO.py ###

'''
ICT305: Data Visualisation and Simulation
Group Assignment
Group Name: Machine Masters
Dataset Analysis: Data Exploration and Discovery
Eren Stannard - 34189185
'''


from os import path
import pandas as pd
import json
#import geojson


# Function for reading data from a file

def readData(filename, file_path = None, sheet_name = 0, skiprows = None, na_values = None,
             index_col = None, usecols = None, dtype = None, header = 0):

    data = None
    
    if file_path:
        filename = path.join(file_path, filename)

    if path.isfile(filename):

        if filename.endswith('csv'):
            data = pd.read_csv(filename, skiprows = skiprows, na_values = na_values, index_col = index_col,
                               usecols = usecols, dtype = dtype, header = header, low_memory = False)

        elif filename.endswith('xlsx'):
            data = pd.read_excel(filename, sheet_name = sheet_name, skiprows = skiprows, na_values = na_values,
                                 index_col = index_col, usecols = usecols, dtype = dtype, header = header)
            
            '''elif filename.endswith('json'):
                with open(filename, 'r') as file:
                    data = geojson.load(file)'''
                               
        else:
            print("Error: Invalid file type.\n")

    else:
        print("Error: Could not open file.\n")

    return data


# Function for writing data to an Excel file

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