import streamlit as st
import plotly.express as px
import json
import pandas as pd

# Title of the app
st.title("Choropleth Map of Perth Area")


@st.cache_data
def load_data():
    # Load the data from the Excel file (this assumes you have the file in the same directory)
    file_path = "assets/WA Police Force Crime Timeseries.csv"

    # Load the "Western Australia" sheet, skipping metadata rows
    wa_data = pd.read_csv(file_path)
    return wa_data


def preprocess(data):
    # get all the Murder from the WAPOL_Hierarchy_Lvl1 column
    fmt_data = data[data["WAPOL_Hierarchy_Lvl1"] == "Murder"]
    # get all the dates for
    fmt_data = fmt_data[fmt_data["Period"] == "2007"]
    return fmt_data


data = load_data()
st.write(preprocess(data=data))

# Load the GeoJSON file
geojson_file_path = "./assets/WA Police Force District Boundaries (WAPOL-002).geojson"

with open(geojson_file_path) as f:
    geojson_data = json.load(f)


# Example data (replace this with actual data relevant to the map)
data = pd.DataFrame(
    {
        "region_name": [
            "Perth",
            "Region B",
            "Region C",
            "Region D",
        ],  # Replace with actual region names
        "value": [10, 20, 30, 40],  # Replace with actual values
    }
)

# Create the Choroplethmapbox
fig = px.choropleth_mapbox(
    data,
    geojson=geojson_data,
    locations="region_name",
    featureidkey="properties.NAME",  # Change this key to match the actual GeoJSON field
    color="value",
    color_continuous_scale="Viridis",
    mapbox_style="carto-positron",
    zoom=8,  # Adjust for Perth area
    center={"lat": -31.9505, "lon": 115.8605},  # Perth's coordinates
    opacity=0.6,
)
# Update layout of the map
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

# Display the map in Streamlit
st.plotly_chart(fig)
