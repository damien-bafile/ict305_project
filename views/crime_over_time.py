import streamlit as st
import plotly.express as px
import pandas as pd
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from catppuccin import PALETTE

from helpers.DataLoading import loadData
from helpers.FileIO import readData
from helpers.CrimeData import getCrimeCounts


@st.cache_data
def load_data(filename, file_path='assets', sheet_name=None):
    if filename.endswith('.xlsx'):
        data = loadData(filename, file_path=file_path, sheet_name=sheet_name)
    else:
        data = readData(filename, file_path=file_path)
    return data


# Title of the page
st.title("Crime Over Time")

# Figure container margins
_, centre, _ = st.columns([0.05, 0.9, 0.05])

# Colour palette
colours = [colour.hex for colour in PALETTE.latte.colors]

# Load the data from the Excel file (this assumes you have the file in the same directory)
filename = 'data_Processed.csv'
file_path = 'assets'

crimes_df = load_data(filename, file_path=file_path)

crimes_df['State'] = crimes_df['State'].apply(lambda x: x.title())
crimes_df['Region'] = crimes_df['Region'].apply(lambda x: x.rsplit(maxsplit=1)[0].title())
crimes_df['District'] = crimes_df['District'].apply(lambda x: x.rsplit(maxsplit=1)[0].title())

# Time ranges
year_range = [crimes_df['Year'].min(), crimes_df['Year'].max() - 1]
period_range = [crimes_df['Period'].min(), crimes_df['Period'].max()]
st.caption(f"From {period_range[0]} to {period_range[1]}.")


# For all WA
st.header("For All of WA")

# WA all crimes
crimes_df_wa = getCrimeCounts(crimes_df, area_scale='State', ascending=True)
# WA total
crimes_df_wa_total = getCrimeCounts(crimes_df.drop(columns='Crime'), group_by=['Year'], area_scale='State', sort=False)
# WA per year
crimes_df_wa_per_year = getCrimeCounts(crimes_df, group_by=['Year'], area_scale='State', sort=False)
# WA per period
crimes_df_wa_per_period = getCrimeCounts(crimes_df, group_by=['Period'], area_scale='State', sort=False)

crimes = crimes_df_wa['Crime'].unique()[::-1]
crime_colour_map = dict(zip(crimes, colours[:len(crimes)]))

# Line plot (year)
fig = px.line(
    crimes_df_wa_total,
    x='Year',
    y='Count_Per_100',
    color_discrete_sequence=colours,
    range_x=year_range,
    hover_data={
        'State': True,
        'Year': True,
        'Count_Per_100': True,
    },
)
st.subheader("Total Number of Crimes in WA Over Time (per Year) for All Crime")
st.plotly_chart(fig, use_container_width=True)

# Line plot (year)
fig = px.line(
    crimes_df_wa_per_year,
    x='Year',
    y='Count_Per_100',
    color='Crime',
    color_discrete_sequence=colours,
    range_x=year_range,
    hover_data={
        'State': True,
        'Crime': True,
        'Year': True,
        'Count_Per_100': True,
    },
    height=550,
)
st.subheader("Total Number of Crimes in WA Over Time (per Year)")
st.write("Select or deselect crime categories in legend to restrict display. Double click to isolate a single option.")
st.plotly_chart(fig, use_container_width=True)

# Line plot (period)
fig = px.line(
    crimes_df_wa_per_period,
    x='Period',
    y='Count_Per_100',
    color='Crime',
    color_discrete_sequence=colours,
    range_x=period_range,
    hover_data={
        'State': True,
        'Crime': True,
        'Period': True,
        'Count_Per_100': True,
    },
    height=550,
)
st.subheader(f"Total Number of Crimes in WA Over Time (per Period)")
st.write("Select or deselect crime categories in legend to restrict display. Double click to isolate a single option.")
st.plotly_chart(fig, use_container_width=True)
st.divider()


# Per district
st.header("Per District")

# Per district all crimes
crimes_df_districts = getCrimeCounts(crimes_df, area_scale='District', ascending=True)
# Per district totals
crimes_df_districts_total = getCrimeCounts(crimes_df.drop(columns='Crime'), area_scale='District', ascending=True)
# Per district per year
crimes_df_districts_per_year = getCrimeCounts(crimes_df, group_by=['Year'], area_scale='District', sort=False)
# Per district totals per year
crimes_df_districts_total_per_year = getCrimeCounts(crimes_df.drop(columns='Crime'), group_by=['Year'], area_scale='District', sort=False)
# Per district per period
crimes_df_districts_per_period = getCrimeCounts(crimes_df, group_by=['Period'], area_scale='District', sort=False)
# Per district total per period
crimes_df_districts_total_per_period = getCrimeCounts(crimes_df.drop(columns='Crime'), group_by=['Period'], area_scale='District', sort=False)

districts = crimes_df_districts_total['District'].unique()[::-1]
district_colour_map = dict(zip(districts, colours[:len(districts)]))

# Line plot (year)
fig = px.line(
    crimes_df_districts_total_per_year,
    x='Year',
    y='Count_Per_100',
    color='District',
    color_discrete_sequence=colours,
    range_x=year_range,
    hover_data={
        'District': True,
        'Year': True,
        'Count_Per_100': True,
    },
)
st.subheader(f"Total Number of Crimes in WA per District Over Time (per Year)")
st.write("Select or deselect district names in legend to restrict display. Double click to isolate a single option.")
st.plotly_chart(fig, use_container_width=True)

# Line plot (period)
fig = px.line(
    crimes_df_districts_total_per_period,
    x='Period',
    y='Count_Per_100',
    color='District',
    color_discrete_sequence=colours,
    range_x=period_range,
    hover_data={
        'District': True,
        'Period': True,
        'Count_Per_100': True,
    },
)
st.subheader(f"Total Number of Crimes in WA per District Over Time (per Period)")
st.write("Select or deselect district names in legend to restrict display. Double click to isolate a single option.")
st.plotly_chart(fig, use_container_width=True)
st.divider()


# District with highest crime rate
st.header("District With the Highest Crime Rate")

# Line plot (year)
fig = px.line(
    crimes_df_districts_per_year[crimes_df_districts_per_year['District'] == districts[0]],
    x='Year',
    y='Count_Per_100',
    color='Crime',
    color_discrete_sequence=colours,
    range_x=year_range,
    hover_data={
        'District': True,
        'Crime': True,
        'Year': True,
        'Count_Per_100': True,
    },
    height=550,
)
st.subheader(f"Total Number of Crimes in the {districts[0]} District Over Time (per Year)")
st.write("Select or deselect crime categories in legend to restrict display. Double click to isolate a single option.")
st.plotly_chart(fig, use_container_width=True)

# Line plot (period)
fig = px.line(
    crimes_df_districts_per_period[crimes_df_districts_per_period['District'] == districts[0]],
    x='Period',
    y='Count_Per_100',
    color='Crime',
    color_discrete_sequence=colours,
    range_x=period_range,
    hover_data={
        'District': True,
        'Crime': True,
        'Period': True,
        'Count_Per_100': True,
    },
    height=550,
)
st.subheader(f"Total Number of Crimes in the {districts[0]} District Over Time (per Period)")
st.write("Select or deselect crime categories in legend to restrict display. Double click to isolate a single option.")
st.plotly_chart(fig, use_container_width=True)