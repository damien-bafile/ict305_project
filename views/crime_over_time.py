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

crimes_df[f'{area_scale}_Name'] = crimes_df[area_scale].apply(lambda x: ''.join(x.split()[:-1]).title())
crimes_df_total = getCrimeCounts(crimes_df, area_scale = area_scale, ascending = True)
crimes_df_over_time_year = getCrimeCounts(crimes_df, group_by = ['Year'], sort = False, area_scale = area_scale)
crimes_df_over_time_period = getCrimeCounts(crimes_df, group_by = ['Period'], sort = False, area_scale = area_scale)

areas = crimes_df_total[area_scale].unique()
crimes = crimes_df_total['Crime'].unique()
crime_order = crimes[::-1]

x_min = crimes_df_total['Count_Per_100'].min()
x_max = crimes_df_total['Count_Per_100'].max()
x_time_min = crimes_df_over_time_year['Count_Per_100'].min()
x_time_max = crimes_df_over_time_year['Count_Per_100'].max()


with centre:

    # Line plot with dropdown menu
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

    st.write("Select or deselect crime categories in legend to restrict display.")
    st.plotly_chart(fig, use_container_width = True, theme = 'streamlit')
    st.divider()
    
    
    # Line plot with dropdown menu
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

    st.write("Select or deselect crime categories in legend to restrict display.")
    st.plotly_chart(fig, use_container_width = True, theme = 'streamlit')
    st.divider()