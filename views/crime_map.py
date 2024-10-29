import streamlit as st
import plotly.express as px
import json
import pandas as pd

from helpers.DataLoading import loadData
from helpers.FileIO import readData, filePath


@st.cache_data
def load_data(filename, file_path='assets', sheet_name=None):
    if filename.endswith('.xlsx'):
        data = loadData(filename, file_path=file_path, sheet_name=sheet_name)
    else:
        data = readData(filename, file_path=file_path)
    return data


# Title of the page
st.title("Interactive Crime Map")

# Figure container margins
_, centre, _ = st.columns([0.05, 0.9, 0.05])


# Load the data from the Excel file (this assumes you have the file in the same directory)
filename = 'data.xlsx'
file_path = 'assets'
sheet_name = 'Data'
#crimes_df = load_data(filename, file_path, sheet_name)

# Load the GeoJSON file for districts
geojson_filename = 'WA Police Force District Boundaries (WAPOL-002).geojson'
geojson_data_suburbs = load_data(geojson_filename, file_path=file_path)

# Load the crime data from the CSV
totals_sorted_filename = 'data_All_Crimes_Totals_Sorted.csv'
csv_file_path = filePath('CSVs', file_path=file_path)
crime_data = load_data(totals_sorted_filename, file_path=csv_file_path)

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
    height=750,
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
    updatemenus = [
        {
            'buttons': dropdown_buttons,
            'direction': 'down',
            'showactive': True,
            'x': 1,
            'xanchor': 'right',
            'y': 1,
            'yanchor': 'bottom',
            'font': {'size': 12},
            'pad': {'b': 5, 'r': 1},
        },
    ],
    annotations = [
        {
            'text': 'Select Crime Category:',
            'x': 1,
            'xanchor': 'right',
            'xref': 'paper',
            'xshift': -270,
            'y': 1,
            'yanchor': 'bottom',
            'yref': 'paper',
            'yshift': 7,
            'showarrow': False,
            'font': {'size': 16},
            'borderpad': 5,
        },
    ],
)

# Show the figure
st.header("Interactive Map of WA Police Districts")
st.subheader("Total Number of Crimes in WA per District (2007-2024)")
st.plotly_chart(fig, use_container_width = True)