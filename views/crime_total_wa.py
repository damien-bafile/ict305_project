import streamlit as st
import pandas as pd
import plotly.express as px
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource

from helpers.DataLoading import loadData
from helpers.CrimeData import getCrimeCounts


@st.cache_data
def load_data(filename, file_path, sheet_name):
    crimes_df = loadData(filename, file_path, sheet_name)
    return crimes_df


area_scale = 'State'


# Title of the app
st.title("Crime for All of WA")
st.divider()

# Figure container margins
_, centre, _ = st.columns([0.05, 0.9, 0.05])

# Load the data from the Excel file (this assumes you have the file in the same directory)
filename = 'data.xlsx'
file_path = 'assets'
sheet_name = 'Data'

crimes_df = load_data(filename, file_path, sheet_name)

crimes_df[f'{area_scale}_Name'] = crimes_df[area_scale].apply(lambda x: x.title())

crimes_df_total = getCrimeCounts(crimes_df, area_scale = area_scale, ascending = True)
crimes_df_over_time = getCrimeCounts(crimes_df, group_by = ['Year'], sort = False, area_scale = area_scale, ascending = True)
crimes_df_over_time_rank = crimes_df_over_time.sort_values(by = ['Year', 'Count_Per_100'], ascending = [True, True])

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
    category_orders = {'Crime': crime_order},
    barmode = 'group',
    #range_x = [x_min, x_max],
    text_auto = '.2f',
    width = 700,
    height = 600,
)

st.subheader("Total Number of Crimes for All of WA Over Time (2007-2024)")
st.plotly_chart(fig, use_container_width = True)
st.divider()


# Bar chart over time (continuous ranking)

fig = px.bar(
    crimes_df_over_time_rank,
    x = 'Count_Per_100',
    y = 'Crime',
    animation_frame = 'Year',
    animation_group = 'Crime',
    #category_orders = {'Crime': crime_order},
    barmode = 'group',
    #range_x = [x_time_min, x_time_max],
    width = 700,
    height = 600,
)

fig.update_layout(
    updatemenus = [
        {
            'buttons': [
                {
                    'args': [
                        None,
                        {
                            'frame': {'duration': 900},
                            'fromcurrent': True,
                            'transition': {'duration': 200, 'easing': 'quadratic-in-out'},
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
            ],
        },
    ],
)

st.subheader("Total Number of Crimes for All of WA Over Time (2007-2024) with Continuous Ranking")
st.plotly_chart(fig, use_container_width = True)
st.divider()


# Bar chart over time

fig = px.bar(
    crimes_df_over_time,
    x = 'Count_Per_100',
    y = 'Crime',
    animation_frame = 'Year',
    animation_group = 'Crime',
    category_orders = {'Crime': crime_order},
    barmode = 'group',
    width = 700,
    height = 600,
)

st.subheader("Total Number of Crimes for All of WA Over Time (2007-2024)")
st.plotly_chart(fig, use_container_width = True)