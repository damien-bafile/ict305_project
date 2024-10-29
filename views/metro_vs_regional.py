import streamlit as st
import pandas as pd
import plotly.express as px
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource

import matplotlib.pyplot as plt
import seaborn as sns

from helpers.DataLoading import loadData
from helpers.CrimeData import getCrimeCounts


@st.cache_data
def load_data(filename, file_path, sheet_name):
    crimes_df = loadData(filename, file_path, sheet_name)
    return crimes_df


area_scale = 'Region'


# Title of the app
st.title(f"Crime by {area_scale}")
st.divider()

# Figure container margins
_, centre, _ = st.columns([0.05, 0.9, 0.05])

# Load the data from the Excel file (this assumes you have the file in the same directory)
filename = 'data.xlsx'
file_path = 'assets'
sheet_name = 'Data'

crimes_df = load_data(filename, file_path, sheet_name)

crimes_df_total = getCrimeCounts(crimes_df, area_scale = area_scale, ascending = True)
crimes_df_over_time = getCrimeCounts(crimes_df, group_by = ['Year'], sort = False, area_scale = area_scale)

crimes_df[f'{area_scale}_Name'] = crimes_df[area_scale].apply(lambda x: x.split()[0].title())
crimes_df_total[f'{area_scale}_Name'] = crimes_df_total[area_scale].apply(lambda x: x.split()[0].title())
crimes_df_over_time[f'{area_scale}_Name'] = crimes_df_over_time[area_scale].apply(lambda x: x.split()[0].title())

crime_order = crimes_df_total[['Crime', 'Count_Per_100']].groupby(
    by = 'Crime',
    observed = False,
    as_index = False,
).mean().sort_values(
    by = 'Count_Per_100'
)['Crime'].unique()[::-1]

x_min = crimes_df_total['Count_Per_100'].min()
x_max = crimes_df_total['Count_Per_100'].max()
x_time_min = crimes_df_over_time['Count_Per_100'].min()
x_time_max = crimes_df_over_time['Count_Per_100'].max()



# Bar chart

fig = px.bar(
    crimes_df_total,
    x = 'Count_Per_100',
    y = 'Crime',
    color = f'{area_scale}_Name',
    category_orders = {'Crime': crime_order},
    barmode = 'group',
    range_x = [x_min, x_max],
    width = 700,
    height = 600,
)

st.subheader(f"Total Number of Crimes per {area_scale} (2007-2024)")
st.plotly_chart(fig, use_container_width = True)
st.divider()


# Bar chart over time

fig = px.bar(
    crimes_df_over_time,
    x = 'Count_Per_100',
    y = 'Crime',
    color = f'{area_scale}_Name',
    animation_frame = 'Year',
    animation_group = 'Crime',
    category_orders = {'Crime': crime_order},
    barmode = 'group',
    range_x = [x_time_min, x_time_max],
    width = 700,
    height = 600,
)

st.subheader(f"Total Number of Crimes per {area_scale} Over Time (2007-2024)")
st.plotly_chart(fig, use_container_width = True)
st.divider()


# Scatter plot

fig = px.scatter(
    crimes_df_total,
    x = 'Count_Per_100',
    y = 'Crime',
    color = f'{area_scale}_Name',
    category_orders = {'Crime': crime_order},
    range_x = [x_min, x_max],
    width = 700,
    height = 600,
)

st.subheader(f"Total Number of Crimes per {area_scale} (2007-2024)")
st.plotly_chart(fig, use_container_width = True)
st.divider()


# Scatter plot over time

fig = px.scatter(
    crimes_df_over_time,
    x = 'Count_Per_100',
    y = 'Crime',
    color = f'{area_scale}_Name',
    animation_frame = 'Year',
    animation_group = 'Crime',
    category_orders = {'Crime': crime_order},
    range_x = [x_time_min, x_time_max],
    width = 700,
    height = 600,
)

st.subheader(f"Total Number of Crimes per {area_scale} Over Time (2007-2024)")
st.plotly_chart(fig, use_container_width = True)