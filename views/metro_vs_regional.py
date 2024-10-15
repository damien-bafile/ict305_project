import streamlit as st
import pandas as pd
import plotly.express as px
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource

import matplotlib.pyplot as plt
import seaborn as sns

import sys

from helpers.CrimeData import getCrimeData


@st.cache_data
def load_data():
    # Load the data from the Excel file (this assumes you have the file in the same directory)
    filename = 'data'
    file_path = 'assets'

    # Load the "Western Australia" sheet, skipping metadata rows
    #wa_data = pd.read_excel(file_path, sheet_name="Western Australia", skiprows=6)

    crimes_df = getCrimeData(filename, file_path = file_path, sheet_name = 'Data')
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

crimes_df = load_data()

crimes_df['District_Name'] = crimes_df['District'].apply(lambda x: x.title().removesuffix(' District'))

# Create scatter plot

fig = px.scatter(
    crimes_df,
    x = 'Count_Per_100',
    y = 'Crime',
    animation_frame = 'Year',
    animation_group = 'Crime',
    color = 'District_Name',
    width = 700,
    height = 600,
)

st.plotly_chart(fig, use_container_width = True)