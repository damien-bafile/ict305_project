import streamlit as st
import plotly.express as px
import pandas as pd
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from catppuccin import PALETTE

from helpers.DataLoading import loadData
from helpers.CrimeData import getCrimeCounts


@st.cache_data
def load_data(filename, file_path, sheet_name):
    crimes_df = loadData(filename, file_path, sheet_name)
    return crimes_df


# Title of the app
st.title("Crime Over Time")
st.divider()

# Figure container margins
_, centre, _ = st.columns([0.05, 0.9, 0.05])

# Colour palette
colours = [colour.hex for colour in PALETTE.latte.colors]

# Load the data from the Excel file (this assumes you have the file in the same directory)
filename = 'data.xlsx'
file_path = 'assets'
sheet_name = 'Data'
area_scale = 'State'

crimes_df = load_data(filename, file_path, sheet_name)

crimes_df['State_Name'] = crimes_df['State'].apply(lambda x: ''.join(x.split()[:-1]).title())
crimes_df['District_Name'] = crimes_df['District'].apply(lambda x: ''.join(x.split()[:-1]).title())

# For all WA
crimes_df_total = getCrimeCounts(crimes_df, area_scale = 'State', ascending = True)
crimes_df_over_time_year = getCrimeCounts(crimes_df, group_by = ['Year'], sort = False, area_scale = 'State')
crimes_df_over_time_period = getCrimeCounts(crimes_df, group_by = ['Period'], sort = False, area_scale = 'State')


# For districts
crimes_df_districts_total = getCrimeCounts(crimes_df.drop(columns = 'Crime'), area_scale = 'District', ascending = True)
crimes_df_districts_ranked = getCrimeCounts(crimes_df.drop(columns = 'Crime'), area_scale = 'District', ascending = True)
crimes_df_districts_over_time_year = getCrimeCounts(crimes_df, group_by = ['Year'], sort = False, area_scale = 'District')
crimes_df_districts_total_over_time_year = getCrimeCounts(crimes_df.drop(columns = 'Crime'), group_by = ['Year'], sort = False, area_scale = 'District')
crimes_df_districts_over_time_period = getCrimeCounts(crimes_df, group_by = ['Period'], sort = False, area_scale = 'District')
crimes_df_districts_total_over_time_period = getCrimeCounts(crimes_df.drop(columns = 'Crime'), group_by = ['Period'], sort = False, area_scale = 'District')

districts = crimes_df_districts_ranked['District_Name'].unique()
district_colour_map = dict(zip(districts, colours[:len(districts)]))
district_order = districts[::-1]

crimes = crimes_df_total['Crime'].unique()
crime_colour_map = dict(zip(crimes, colours[:len(crimes)]))
crime_order = crimes[::-1]

x_min = crimes_df_total['Count_Per_100'].min()
x_max = crimes_df_total['Count_Per_100'].max()
x_time_min = crimes_df_over_time_year['Count_Per_100'].min()
x_time_max = crimes_df_over_time_year['Count_Per_100'].max()


# Line plot (year)
fig = px.line(
    crimes_df_over_time_year,
    x = 'Year',
    y = 'Count_Per_100',
    line_group = 'Crime',
    color = 'Crime',
    color_discrete_sequence = colours,
    width = 700,
    height = 550,
)

st.subheader("Total Number of Crimes in WA Over Time (Per Year) (2007-2024)")
st.write("Select or deselect crime categories in legend to restrict display.")
st.plotly_chart(fig, use_container_width = True)
st.divider()


# Line plot (period)
fig = px.line(
    crimes_df_over_time_period,
    x = 'Period',
    y = 'Count_Per_100',
    line_group = 'Crime',
    color = 'Crime',
    color_discrete_sequence = colours,
    width = 700,
    height = 550,
)

st.subheader("Total Number of Crimes in WA Over Time (Per Period) (2007-2024)")
st.write("Select or deselect crime categories in legend to restrict display.")
st.plotly_chart(fig, use_container_width = True)
st.divider()


# Line plot (year)
fig = px.line(
    crimes_df_districts_total_over_time_year,
    x = 'Year',
    y = 'Count_Per_100',
    line_group = 'District',
    color = 'District',
    color_discrete_sequence = colours,
    width = 700,
    height = 550,
)

st.subheader("Total Number of Crimes in WA Per District Over Time (Per Year) (2007-2024)")
st.write("Select or deselect crime categories in legend to restrict display.")
st.plotly_chart(fig, use_container_width = True)
st.divider()


# Line plot (period)
fig = px.line(
    crimes_df_districts_total_over_time_period,
    x = 'Period',
    y = 'Count_Per_100',
    line_group = 'District',
    color = 'District',
    color_discrete_sequence = colours,
    width = 700,
    height = 550,
)

st.subheader("Total Number of Crimes in WA Per District Over Time (Per Period) (2007-2024)")
st.write("Select or deselect crime categories in legend to restrict display.")
st.plotly_chart(fig, use_container_width = True)
st.divider()


# Line plot (year)
fig = px.line(
    crimes_df_districts_over_time_year[crimes_df_districts_over_time_year['District_Name'] == district_order[0]],
    x = 'Year',
    y = 'Count_Per_100',
    line_group = 'Crime',
    color = 'Crime',
    color_discrete_sequence = colours,
    width = 700,
    height = 550,
)

st.subheader(f"Total Number of Crimes in the {district_order[0]} District Over Time (Per Year) (2007-2024)")
st.write("Select or deselect crime categories in legend to restrict display.")
st.plotly_chart(fig, use_container_width = True)