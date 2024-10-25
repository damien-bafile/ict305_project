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


area_scale = 'State'

crimes_df = load_data()
crimes_df[f'{area_scale}_Name'] = crimes_df[area_scale].apply(lambda x: x.title())

crimes_df_total = getCrimeCounts(crimes_df, area_scale = area_scale, ascending = True)
crimes_df_over_time = getCrimeCounts(crimes_df, group_by = ['Year'], sort = False, area_scale = area_scale, ascending = True)
crimes_df_over_time_rank = crimes_df_over_time.sort_values(by = ['Year', 'Count_Per_100'], ascending = [True, True])

crime_order = crimes_df_total['Crime'].unique()[::-1]

x_min = crimes_df_total['Count_Per_100'].min()
x_max = crimes_df_total['Count_Per_100'].max()
x_time_min = crimes_df_over_time['Count_Per_100'].min()
x_time_max = crimes_df_over_time['Count_Per_100'].max()


st.title("Crime for All of WA")

l_margin, centre, r_margin = st.columns([0.1, 0.8, 0.1])

with centre:    

    # Bar chart

    fig = px.bar(
        crimes_df_total,
        x = 'Count_Per_100',
        y = 'Crime',
        category_orders = {'Crime': crime_order},
        barmode = 'group',
        range_x = [x_min, x_max],
        text_auto = '.2f',
        title = 'Total Number of Crimes for All of WA (2007-2024)',
        width = 1000,
        height = 600,
    )

    st.plotly_chart(fig, use_container_width = False)


    # Bar chart over time (continuous ranking)

    fig = px.bar(
        crimes_df_over_time_rank,
        x = 'Count_Per_100',
        y = 'Crime',
        animation_frame = 'Year',
        animation_group = 'Crime',
        #category_orders = {'Crime': crime_order},
        barmode = 'group',
        range_x = [x_time_min, x_time_max],
        title = 'Total Number of Crimes for All of WA Over Time (2007-2024)',
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
                                'transition': {
                                    'duration': 200,
                                    'easing': 'quadratic-in-out',
                                },
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

    st.plotly_chart(fig, use_container_width = True)


    # Bar chart over time

    fig = px.bar(
        crimes_df_over_time,
        x = 'Count_Per_100',
        y = 'Crime',
        animation_frame = 'Year',
        animation_group = 'Crime',
        category_orders = {'Crime': crime_order},
        barmode = 'group',
        range_x = [x_time_min, x_time_max],
        title = 'Total Number of Crimes for All of WA Over Time (2007-2024)',
        width = 700,
        height = 600,
    )

    st.plotly_chart(fig, use_container_width = True)