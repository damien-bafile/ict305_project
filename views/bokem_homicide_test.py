import streamlit as st
import pandas as pd
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource


@st.cache_data
def load_data():
    # Load the data from the Excel file (this assumes you have the file in the same directory)
    file_path = "assets/data.xlsx"

    # Load the "Western Australia" sheet, skipping metadata rows
    wa_data = pd.read_excel(file_path, sheet_name="Western Australia", skiprows=6)
    return wa_data


homicide_data = load_data()
# Extract relevant homicide columns
homicide_data = homicide_data[
    ["Unnamed: 0", "Homicide", "Unnamed: 2", "Unnamed: 3", "Unnamed: 4", "Unnamed: 5"]
]
homicide_data.columns = [
    "Month and Year",
    "Homicide Total",
    "Murder",
    "Attempted / Conspiracy to Murder",
    "Manslaughter",
    "Driving Causing Death",
]

# Convert 'Month and Year' to datetime
homicide_data.loc[:, "Month and Year"] = pd.to_datetime(
    homicide_data["Month and Year"], format="%Y-%m=%d", errors="coerce"
)

# Remove rows where 'Month and Year' is NaT (invalid dates)
homicide_data = homicide_data.dropna()

# Set up data for Bokeh
source = ColumnDataSource(homicide_data)

# Output in Jupyter Notebook
# output_notebook()

# Create a figure
p = figure(
    x_axis_type="datetime",
    title="Homicide Data in Western Australia",
    width=800,
    height=400,
    x_axis_label="Month and Year",
    y_axis_label="Number of Cases",
)

# Add multiple lines for different types of homicide data
p.line(
    "Month and Year",
    "Homicide Total",
    source=source,
    legend_label="Homicide Total",
    color="blue",
    line_width=2,
)
p.line(
    "Month and Year",
    "Murder",
    source=source,
    legend_label="Murder",
    color="red",
    line_width=2,
)
p.line(
    "Month and Year",
    "Attempted / Conspiracy to Murder",
    source=source,
    legend_label="Attempted / Conspiracy to Murder",
    color="green",
    line_width=2,
)
p.line(
    "Month and Year",
    "Manslaughter",
    source=source,
    legend_label="Manslaughter",
    color="orange",
    line_width=2,
)
p.line(
    "Month and Year",
    "Driving Causing Death",
    source=source,
    legend_label="Driving Causing Death",
    color="purple",
    line_width=2,
)

# Customize the legend
p.legend.location = "top_left"
p.legend.click_policy = "hide"

st.write("# WA Homicide Data")

st.bokeh_chart(p, use_container_width=False)
