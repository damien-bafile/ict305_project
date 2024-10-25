import streamlit as st
import plotly.express as px
import json
import pandas as pd

from helpers.DataLoading import loadData


@st.cache_data
def load_data():
    
    # Load the data from the Excel file (this assumes you have the file in the same directory)
    #filename = 'data'
    #file_path = 'assets'

    # Load 'Data' sheet
    crimes_df = loadData()
    
    return crimes_df


# Title of the app
st.title("Choropleth Map of Crime in WA Police Districts")


crimes_df = load_data()


# Load the GeoJSON file for suburbs
geojson_file_path = "assets/WA Police Force District Boundaries (WAPOL-002).geojson"

with open(geojson_file_path) as f:
    geojson_data_suburbs = json.load(f)

# Load the crime data from the CSV
crime_data = pd.read_csv("assets/CSVs/data_All_Crimes_Totals_Sorted.csv")

# Extract unique crime types
crime_types = crime_data["Crime"].unique()


# Create a base figure (for the first crime type by default)
initial_crime_type = crime_types[0]
filtered_data = crime_data[crime_data["Crime"] == initial_crime_type].copy()

# Ensure 'District' column matches the 'DISTRICT' property in GeoJSON
filtered_data.loc[:, 'District'] = filtered_data['District'].str.upper()

# Create the choropleth map
fig = px.choropleth_mapbox(
    filtered_data,
    geojson=geojson_data_suburbs,
    locations="District",
    featureidkey="properties.DISTRICT",
    color="Count_Per_100",
    color_continuous_scale="Viridis",
    mapbox_style="carto-positron",
    zoom=8,
    center={"lat": -31.9505, "lon": 115.8605},  # Perth's coordinates
    opacity=0.6,
    hover_data={
        "District": True,
        "Region": True,
        "Count": True,
        "Population": True,
        "Count_Per_100": True
    },
    width = 700,
    height = 600,
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
    updatemenus=[
        {
            "buttons": dropdown_buttons,
            "direction": "down",
            "pad": {"r": 10, "t": 10},
            "showactive": True,
            "x": 0.1,
            "xanchor": "left",
            "y": 1.05,
            "yanchor": "top"
        }
    ],
    margin={"r": 0, "t": 50, "l": 0, "b": 0},
    title_x=0.5,
    title="Interactive Crime Map by Type",
)

# Show the figure
st.plotly_chart(fig)