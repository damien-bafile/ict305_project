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
def load_data():
    
    # Load the data from the Excel file (this assumes you have the file in the same directory)
    #filename = 'data'
    #file_path = 'assets'

    # Load 'Data' sheet
    crimes_df = loadData()
    
    return crimes_df

st.title("Crime for all of WA")

area_scale = 'State'

crimes_df = load_data()
crimes_df_total = getCrimeCounts(crimes_df, area_scale = area_scale, ascending = True)
crimes_df_over_time = getCrimeCounts(crimes_df, group_by = ['Year'], sort = False, area_scale = area_scale)

crimes_df[f'{area_scale}_Name'] = crimes_df[area_scale].apply(lambda x: x.title())
crimes_df_total[f'{area_scale}_Name'] = crimes_df_total[area_scale].apply(lambda x: x.title())
crimes_df_over_time[f'{area_scale}_Name'] = crimes_df_over_time[area_scale].apply(lambda x: x.title())

crime_order = crimes_df_total['Crime'].unique()[::-1]

x_min = crimes_df_total['Count_Per_100'].min()
x_max = crimes_df_total['Count_Per_100'].max()
x_time_min = crimes_df_over_time['Count_Per_100'].min()
x_time_max = crimes_df_over_time['Count_Per_100'].max()


# Bar chart

fig = px.bar(
    crimes_df_total,
    x = 'Count_Per_100',
    y = 'Crime',
    #color = f'{area_scale}_Name',
    category_orders = {'Crime': crime_order},
    barmode = 'group',
    range_x = [x_min, x_max],
    title = 'Total Number of Crimes for all of WA (2007-2024)',
    width = 700,
    height = 600,
)

st.plotly_chart(fig, use_container_width = True)


# Bar chart over time

fig = px.bar(
    crimes_df_over_time,
    x = 'Count_Per_100',
    y = 'Crime',
    #color = f'{area_scale}_Name',
    animation_frame = 'Year',
    animation_group = 'Crime',
    category_orders = {'Crime': crime_order},
    barmode = 'group',
    range_x = [x_time_min, x_time_max],
    title = 'Total Number of Crimes for all of WA Over Time (2007-2024)',
    width = 700,
    height = 600,
)

st.plotly_chart(fig, use_container_width = True)


# Scatter plot

fig = px.scatter(
    crimes_df_total,
    x = 'Count_Per_100',
    y = 'Crime',
    #color = f'{area_scale}_Name',
    category_orders = {'Crime': crime_order},
    range_x = [x_min, x_max],
    title = 'Total Number of Crimes for all of WA (2007-2024)',
    width = 700,
    height = 600,
)

st.plotly_chart(fig, use_container_width = True)


# Scatter plot over time

fig = px.scatter(
    crimes_df_over_time,
    x = 'Count_Per_100',
    y = 'Crime',
    #color = f'{area_scale}_Name',
    animation_frame = 'Year',
    animation_group = 'Crime',
    category_orders = {'Crime': crime_order},
    range_x = [x_time_min, x_time_max],
    title = 'Total Number of Crimes for all of WA Over Time (2007-2024)',
    width = 700,
    height = 600,
)

st.plotly_chart(fig, use_container_width = True)