import streamlit as st
import pandas as pd
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource

import matplotlib.pyplot as plt
import seaborn as sns

from ..helpers import CrimeData


@st.cache_data
def load_data():
    # Load the data from the Excel file (this assumes you have the file in the same directory)
    file_path = "assets/data.xlsx"

    # Load the "Western Australia" sheet, skipping metadata rows
    #wa_data = pd.read_excel(file_path, sheet_name="Western Australia", skiprows=6)

    crimes_df = CrimeData.getCrimeData(file_path, sheet_name = 'Data')
    #wa_data = getCrimeData(file_path, sheet_name = 'Western Australia')
    
    return crimes_df

st.title("Metro vs Regional Crime")
st.write("Hello from metro_vs_region.py")
st.write("hi")

# Function for getting crime counts for a region

def getCrimeCounts(df, scale = 'District', area = None):

    if area:
        df = df[df[scale].str.contains(area.upper())]

    df = df[[scale, 'Crime', 'Count_Per_100']]
    df = df.groupby(
        by = [scale, 'Crime'],
        observed = False,
        as_index = False,
    ).sum().sort_values(
        by = 'Count_Per_100',
        ascending = False,
    )
    
    return df

crime_counts_by_region = getCrimeCounts(crimes_df, 'Region')

plt.figure(figsize = (10, 6), layout = 'constrained')
ax = sns.barplot(data = crime_counts_by_region, x = 'Count_Per_100', y = 'Crime', hue = 'Region', errorbar = None)
ax.set_title('Total Number of Crimes in Western Australia per Region by Crime (2007-2024)');

st.bar_chart(data = crime_counts_by_region, x = 'Count_Per_100', y = 'Crime')