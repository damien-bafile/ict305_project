import streamlit as st
import pandas as pd
import plotly.express as px
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
st.title("Crime for All of WA")

# Figure container margins
_, centre, _ = st.columns([0.05, 0.9, 0.05])

# Colour palette
colours = [colour.hex for colour in PALETTE.latte.colors]

# Load the data from the Excel file (this assumes you have the file in the same directory)
filename = 'data_Processed.csv'
file_path = 'assets'
area_scale = 'State'

crimes_df = load_data(filename, file_path=file_path)

crimes_df['State'] = crimes_df['State'].apply(lambda x: x.title())
crimes_df['Region'] = crimes_df['Region'].apply(lambda x: x.rsplit(maxsplit=1)[0].title())
crimes_df['District'] = crimes_df['District'].apply(lambda x: x.rsplit(maxsplit=1)[0].title())

# Time ranges
year_range = [crimes_df['Year'].min(), crimes_df['Year'].max() - 1]
period_range = [crimes_df['Period'].min(), crimes_df['Period'].max()]
st.caption(f"From {period_range[0]} to {period_range[1]}.")

crimes_df_total = getCrimeCounts(crimes_df, area_scale=area_scale, ascending=True)
crimes_df_over_time = getCrimeCounts(crimes_df, group_by=['Year'], area_scale=area_scale, sort=False)
crimes_df_over_time_rank = crimes_df_over_time.sort_values(by=['Year', 'Count_Per_100'], ascending=[True, True])

crimes = crimes_df_total['Crime'].unique()[::-1]


# All time
st.header("All Time")

# Bar chart
fig = px.bar(
    crimes_df_total,
    x='Count_Per_100',
    y='Crime',
    category_orders={'Crime': crimes},
    color_discrete_sequence=colours,
    barmode='group',
    text_auto='.2f',
    height=600,
)
st.subheader("Crime Categories Ranked By Frequency for All of WA")
st.plotly_chart(fig, use_container_width=True)
st.divider()


# Over ime
st.header("Over Time")

# Bar chart over time (continuous ranking)
fig = px.bar(
    crimes_df_over_time_rank,
    x='Count_Per_100',
    y='Crime',
    animation_frame='Year',
    animation_group='Crime',
    color_discrete_sequence=colours,
    barmode='group',
    height=600,
)
buttons = [
    {
        'args': [
            None,
            {
                'frame': {'duration': 900},
                'fromcurrent': True,
                'transition': {'duration': 300, 'easing': 'quadratic-in-out'},
            },
        ],
        'method': 'animate',
    },
    {
        'args': [
            None,
            {
                'frame': {'duration': 0},
                'mode': 'immediate',
                'transition': {'duration': 0},
            },
        ],
        'method': 'animate',
    },
]
fig.update_layout(updatemenus=[{'buttons': buttons}])
st.subheader("Crime Categories Continuously Ranked Over Time By Frequency for All of WA")
st.plotly_chart(fig, use_container_width=True)