1. Add 'helpers' folder and __init__.py to project directory.


2. Add RegionListing.csv from 'assets' folder to the same folder in project directory.


3. Download data by adding the following to streamlit_app.py (downloads unprocessed files):

from helpers.DataLoading import downloadData
downloadData()


4. Load data by adding the following to file where data is to be loaded (processes files and writes new .csvs):

from helpers.DataLoading import loadData
df = loadData()