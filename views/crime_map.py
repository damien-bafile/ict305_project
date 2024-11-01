import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import json
import os
import pandas as pd
from catppuccin import PALETTE

from helpers.CrimeData import downloadGeoJSON
from helpers.FileIO import *

# Load the GeoJSON file for suburbs
file_path = 'assets'
district_file_path = filePath('WAPOL_Districts', file_path=file_path)
geojson_file_path = filePath('Police_Districts.geojson', file_path=district_file_path)

if not os.path.isfile(geojson_file_path):
    downloadGeoJSON(district_file_path)

geojson_data_suburbs = readData(geojson_file_path)

# Load the crime data from the CSV
csv_file_path = filePath('CSVs', file_path=file_path)
crime_file_path = filePath('data_All_Crimes_Totals_Sorted.csv', file_path=csv_file_path)
crime_data = readData(crime_file_path)

# Extract unique crime types
crime_types = crime_data["Crime"].unique()

# Create a base figure (for the first crime type by default)
initial_crime_type = crime_types[0]
filtered_data = crime_data[crime_data["Crime"] == initial_crime_type].copy()

# Ensure 'District' column matches the 'DISTRICT' property in GeoJSON
filtered_data.loc[:, 'District'] = filtered_data['District'].str.upper()

catppuccin_color_scale = [
    [0, PALETTE.latte.colors.blue.hex],
    [0.25, PALETTE.latte.colors.green.hex],
    [0.5, PALETTE.latte.colors.yellow.hex],
    [0.75, PALETTE.latte.colors.maroon.hex],
    [1, PALETTE.latte.colors.red.hex],
]

# Create the choropleth map
fig = px.choropleth_mapbox(
    filtered_data,
    geojson=geojson_data_suburbs,
    locations="District",
    featureidkey="properties.DISTRICT",
    color="Count_Per_100",
    color_continuous_scale=catppuccin_color_scale,
    mapbox_style="carto-positron",
    zoom=8,
    center={"lat": -31.9505, "lon": 115.8605},  # Perth's coordinates
    opacity=0.6,
    height=800,
    hover_data={
        "District": True,
        "Region": True,
        "Count": True,
        "Population": True,
        "Count_Per_100": True
    }
)

# Create the dropdown menu for crime types
dropdown_buttons = [
    {
        "args": [{"z": [crime_data[crime_data["Crime"] == crime_type]["Count_Per_100"]]}],
        "label": crime_type,
        "method": "update",
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
            'x': 0,
            'xanchor': 'left',
            'y': 1,
            'yanchor': 'bottom',
            'font': {'size': 12},
            'pad': {'b': 5, 'l': 180},
        },
    ],
    annotations = [
        {
            'text': 'Select Crime Category:',
            'x': 0,
            'xanchor': 'left',
            'xref': 'paper',
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