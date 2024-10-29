import streamlit as st
import plotly.express as px
import json
import pandas as pd

from helpers.DataLoading import loadData
from helpers.FileIO import *


@st.cache_data
def load_data(filename, file_path, sheet_name):
    crimes_df = loadData(filename, file_path, sheet_name)
    return crimes_df


# Title of the app
st.title("Interactive Crime Map")
st.divider()

# Figure container margins
_, centre, _ = st.columns([0.05, 0.9, 0.05])

# Load the data from the Excel file (this assumes you have the file in the same directory)
filename = 'data.xlsx'
file_path = 'assets'
sheet_name = 'Data'

#crimes_df = load_data(filename, file_path, sheet_name)

# Load the GeoJSON file for suburbs
geojson_filename = filePath(
    'WA Police Force District Boundaries (WAPOL-002).geojson',
    file_path = file_path,
)

with open(geojson_filename, 'r') as f:
    geojson_data_suburbs = json.load(f)

# Load the crime data from the CSV
totals_sorted_filename = 'data_All_Crimes_Totals_Sorted.csv'
csv_file_path = filePath('CSVs', file_path)
crime_data = readData(totals_sorted_filename, csv_file_path)

# Extract unique crime types
crime_types = crime_data['Crime'].unique()

# Create a base figure (for the first crime type by default)
initial_crime_type = crime_types[0]
filtered_data = crime_data[crime_data['Crime'] == initial_crime_type].copy()

# Ensure 'District' column matches the 'DISTRICT' property in GeoJSON
filtered_data.loc[:, 'District'] = filtered_data['District'].str.upper()


# Create the choropleth map
fig = px.choropleth_mapbox(
    filtered_data,
    geojson=geojson_data_suburbs,
    locations='District',
    featureidkey='properties.DISTRICT',
    color='Count_Per_100',
    color_continuous_scale='Viridis',
    mapbox_style='carto-positron',
    zoom=8,
    center={'lat': -31.9505, 'lon': 115.8605},  # Perth's coordinates
    opacity=0.6,
    hover_data={
        'District': True,
        'Region': True,
        'Count': True,
        'Population': True,
        'Count_Per_100': True
    },
    width=700,
    height=600,
)

# Create the dropdown menu for crime types
dropdown_buttons = [
    {
        'args': [{'z': [crime_data[crime_data['Crime'] == crime_type]['Count_Per_100']]}],
        'label': crime_type,
        'method': 'update',
    }
    for crime_type in crime_types
]

# Add dropdown to the layout
fig.update_layout(
    updatemenus=[
        {
            'buttons': dropdown_buttons,
            'direction': 'down',
            'showactive': True,
            'pad': {'t': 5},
            'x': 1,
            'xanchor': 'right',
            'y': 1.1,
            'yanchor': 'top',
            'font': {'size': 16},
        },
    ],
    annotations=[
        {
            'text': 'Select Crime Category:',
            'x': 1,
            'xanchor': 'right',
            'xref': 'paper',
            'y': 1.15,
            'yanchor': 'top',
            'yref': 'paper',
            'showarrow': False,
            'font': {'size': 16},
        },
    ],
    margin={'t': 75},
)

# Show the figure
st.header("Interactive Map of Crime Across WA Police Districts")
st.plotly_chart(fig, use_container_width = True)