import streamlit as st
import pandas as pd
import plotly.express as px
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource

import matplotlib.pyplot as plt
import seaborn as sns

from helpers.CrimeData import *


@st.cache_data
def load_data():
    
    # Load the data from the Excel file (this assumes you have the file in the same directory)
    filename = 'data'
    file_path = 'assets'

    # Load 'Data' sheet
    crimes_df = getCrimeData(filename, file_path = file_path, sheet_name = 'Data')
    
    return crimes_df

st.title("Metro vs Regional Crime")

crimes_df = load_data()

crimes_df['District_Name'] = crimes_df['District'].apply(lambda x: x.title().removesuffix(' District'))
crimes_df['Region_Name'] = crimes_df['Region'].apply(lambda x: x.split()[0].title())


# Bar chart

fig = px.bar(
    crimes_df,
    x = 'Count_Per_100',
    y = 'Crime',
    color = 'Region_Name',
    width = 700,
    height = 600,
    barmode = 'group',
    title = 'Total Number of Crimes per Region (2007-2024)',
)

st.plotly_chart(fig, use_container_width = True)


# Scatter plot

fig = px.scatter(
    crimes_df,
    x = 'Count_Per_100',
    y = 'Crime',
    animation_frame = 'Year',
    animation_group = 'Crime',
    color = 'Region_Name',
    width = 700,
    height = 600,
    title = 'Total Number of Crimes per Region (2007-2024)',
)

st.plotly_chart(fig, use_container_width = True)