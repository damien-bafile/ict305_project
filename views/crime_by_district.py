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
st.title("Crime per District")

# Figure container margins
_, centre, _ = st.columns([0.05, 0.9, 0.05])

# Colour palette
colours = [colour.hex for colour in PALETTE.latte.colors]

# Load the data from the Excel file (this assumes you have the file in the same directory)
filename = 'data_Processed.csv'
file_path = 'assets'
area_scale = 'District'

crimes_df = load_data(filename, file_path=file_path)

crimes_df['District'] = crimes_df['District'].apply(lambda x: x.rsplit(maxsplit=1)[0].title())

# Time ranges
year_range = [crimes_df['Year'].min(), crimes_df['Year'].max() - 1]
period_range = [crimes_df['Period'].min(), crimes_df['Period'].max()]
st.caption(f"From {period_range[0]} to {period_range[1]}.")

crimes_df_total = getCrimeCounts(crimes_df, area_scale=area_scale, ascending=True)
crimes_df_over_time = getCrimeCounts(crimes_df, group_by=['Year'], sort=False, area_scale=area_scale)

areas = crimes_df_total[area_scale].unique()
crimes = crimes_df_total['Crime'].unique()[::-1]
colour_map = dict(zip(crimes, colours[:len(crimes)]))
area_colour_map = dict(zip(areas, colours[:len(areas)]))

x_min = crimes_df_total['Count_Per_100'].min()
x_max = crimes_df_total['Count_Per_100'].max()
x_time_min = crimes_df_over_time['Count_Per_100'].min()
x_time_max = crimes_df_over_time['Count_Per_100'].max()


# By crime
st.header("By Crime")

# Figure container margins
left, right = st.columns([0.55, 0.45])

crimes_df_total['Count_Per_100_Norm'] = crimes_df_total[['Crime', 'Count_Per_100', area_scale]].groupby(
    'Crime',
    observed=False,
)['Count_Per_100'].transform(lambda x: x / x.sum())

# Bar chart (normalised relative)
fig = px.bar(
    crimes_df_total,
    x='Count_Per_100_Norm',
    y='Crime',
    color=area_scale,
    category_orders={'Crime': crimes},
    color_discrete_map=area_colour_map,
    barmode='relative',
    height=600,
)
fig.update_layout(updatemenus=[{'pad': {'b': 5, 'r': 1}}])
left.subheader(f"Relative Total Number of Crimes per {area_scale}")
left.plotly_chart(fig, use_container_width=True)

# Bar chart with dropdown menu
fig = px.bar(
    crimes_df_total[crimes_df_total[area_scale] == areas[0]],
    x='Count_Per_100',
    y='Crime',
    color_discrete_sequence=[area_colour_map[areas[0]]],
    text_auto='.2f',
    height=600,
)
# Dropdown menu
dropdown = [
    {
        'args': [
            {
                'x': [crimes_df_total[crimes_df_total[area_scale] == area]['Count_Per_100']],
                'y': [crimes_df_total[crimes_df_total[area_scale] == area]['Crime']],
                'marker.color': colour,
            },
        ],
        'label': area,
        'method': 'update',
    }
    for area, colour in area_colour_map.items()
]
# Add dropdown menu to figure
fig.update_layout(
    updatemenus = [
        {
            'buttons': dropdown,
            'direction': 'down',
            'showactive': True,
            'x': 1,
            'xanchor': 'right',
            'y': 1,
            'yanchor': 'bottom',
            'font': {'size': 12},
            'pad': {'b': 5, 'r': 1},
        },
    ],
    annotations = [
        {
            'text': f'Select {area_scale}:',
            'x': 1,
            'xanchor': 'right',
            'xref': 'paper',
            'xshift': -155,
            'y': 1,
            'yanchor': 'bottom',
            'yref': 'paper',
            'yshift': 7,
            'showarrow': False,
            'font': {'size': 16},
            'borderpad': 5,
        },
    ],
)
right.subheader(f"Total Number of Crimes per {area_scale}")
right.plotly_chart(fig, use_container_width=True)

# Scatter plot
fig = px.scatter(
    crimes_df_total,
    x='Count_Per_100',
    y='Crime',
    color=area_scale,
    category_orders={'Crime': crimes},
    color_discrete_sequence=colours,
    range_x=[x_min, x_max],
    height=500,
)
st.subheader(f"Total Number of Crimes per {area_scale}")
st.plotly_chart(fig, use_container_width=True)
st.divider()


# By district
st.header(f"By {area_scale}")

# Figure container margins
left, right = st.columns([0.55, 0.45])

crimes_df_total['Count_Per_100_Norm'] = crimes_df_total[['Crime', 'Count_Per_100', area_scale]].groupby(
    area_scale,
    observed=False,
)['Count_Per_100'].transform(lambda x: x / x.sum())

# Bar chart
fig = px.bar(
    crimes_df_total,
    x='Count_Per_100_Norm',
    y=area_scale,
    color='Crime',
    category_orders={area_scale: areas},
    color_discrete_map=colour_map,
    barmode='relative',
    height=550,
)
fig.update_layout(updatemenus=[{'pad': {'b': 5, 'r': 1}}])
left.subheader(f"Relative Total Number of Crimes per {area_scale}")
left.plotly_chart(fig, use_container_width=True)

# Bar chart with dropdown menu
fig = px.bar(
    crimes_df_total[crimes_df_total['Crime'] == crimes[0]],
    x='Count_Per_100',
    y=area_scale,
    color_discrete_sequence=[colour_map[crimes[0]]],
    text_auto='.2f',
    height=550,
)
# Dropdown menu
dropdown = [
    {
        'args': [
            {
                'x': [crimes_df_total[crimes_df_total['Crime'] == crime]['Count_Per_100']],
                'y': [crimes_df_total[crimes_df_total['Crime'] == crime][area_scale]],
                'marker.color': colour,
            },
        ],
        'label': crime,
        'method': 'update',
    }
    for crime, colour in colour_map.items()
]
# Add dropdown menu to figure
fig.update_layout(
    updatemenus = [
        {
            'buttons': dropdown,
            'direction': 'down',
            'showactive': True,
            'x': 1,
            'xanchor': 'right',
            'y': 1,
            'yanchor': 'bottom',
            'font': {'size': 12},
            'pad': {'b': 5, 'r': 1},
        },
    ],
    annotations = [
        {
            'text': 'Select Crime Category:',
            'x': 1,
            'xanchor': 'right',
            'xref': 'paper',
            'xshift': -270,
            'y': 1,
            'yanchor': 'bottom',
            'yref': 'paper',
            'yshift': 7,
            'showarrow': False,
            'font': {'size': 16},
            'borderpad': 5,
        },
    ],
)
right.subheader(f"Total Number of Crimes per {area_scale}")
right.plotly_chart(fig, use_container_width=True)
st.divider()


# Over time
st.header("Over Time")

crimes_df_over_time['Count_Per_100_Norm'] = crimes_df_over_time[['Year', 'Crime', 'Count_Per_100', area_scale]].groupby(
    ['Year', 'Crime'],
    observed=False,
)['Count_Per_100'].transform(lambda x: x / x.sum())

# Bar chart over time
fig = px.bar(
    crimes_df_over_time,
    x='Count_Per_100_Norm',
    y='Crime',
    color=area_scale,
    animation_frame='Year',
    animation_group='Crime',
    category_orders={'Crime': crimes},
    color_discrete_sequence=colours,
    barmode='relative',
    height=600,
)
st.subheader(f"Relative Total Number of Crimes per {area_scale} Over Time (per Year)")
st.plotly_chart(fig, use_container_width=True)

# Scatter plot over time
fig=px.scatter(
    crimes_df_over_time,
    x='Count_Per_100',
    y='Crime',
    color=area_scale,
    animation_frame='Year',
    animation_group='Crime',
    category_orders={'Crime': crimes},
    color_discrete_sequence=colours,
    range_x=[x_time_min, x_time_max],
    height=600,
)
st.subheader(f"Total Number of Crimes per {area_scale} Over Time (per Year)")
st.plotly_chart(fig, use_container_width=True)