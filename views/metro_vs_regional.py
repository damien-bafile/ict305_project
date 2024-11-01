import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
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
st.title("Metro vs Regional Crime")

# Figure container margins
_, centre, _ = st.columns([0.05, 0.9, 0.05])

# Load the data from the Excel file (this assumes you have the file in the same directory)
filename = 'data_Processed.csv'
file_path = 'assets'
area_scale = 'Region'

crimes_df = load_data(filename, file_path=file_path)

crimes_df['State'] = crimes_df['State'].apply(lambda x: x.title())
crimes_df['Region'] = crimes_df['Region'].apply(lambda x: x.split()[0].title())
crimes_df['District'] = crimes_df['District'].apply(lambda x: x.rsplit(maxsplit=1)[0].title())

# Time ranges
year_range = [crimes_df['Year'].min(), crimes_df['Year'].max() - 1]
period_range = [crimes_df['Period'].min(), crimes_df['Period'].max()]
st.caption(f"From {period_range[0]} to {period_range[1]}.")

crimes_df_total = getCrimeCounts(crimes_df, area_scale=area_scale, ascending=True)
crimes_df_region_total = getCrimeCounts(crimes_df.drop(columns='Crime'), area_scale=area_scale, ascending=True)
crimes_df_over_time = getCrimeCounts(crimes_df, group_by=['Year'], area_scale=area_scale, sort=False)
crimes_df_over_time_rank = crimes_df_over_time.sort_values(by=['Year', 'Count_Per_100'], ascending=[True, True])

areas = crimes_df[area_scale].unique()
crimes = crimes_df_total[['Crime', 'Count_Per_100']].groupby(
    by='Crime',
    observed=False,
    as_index=False,
).mean().sort_values(by='Count_Per_100')['Crime'].unique()[::-1]

x_min = crimes_df_total['Count_Per_100'].min()
x_max = crimes_df_total['Count_Per_100'].max()

x_min_time = crimes_df_over_time['Count_Per_100'].min()
x_max_time = crimes_df_over_time['Count_Per_100'].max()

# Colour palette
colours = [colour.hex for colour in PALETTE.latte.colors][:14]
colours = sorted(colours)
area_colours = [colours[0], colours[-1]]
area_colour_map = dict(zip(areas, area_colours))


# All time
st.header("All Time")

# Bar chart
fig = px.bar(
    crimes_df_region_total,
    x='Count_Per_100',
    y=area_scale,
    color=area_scale,
    category_orders={area_scale: areas},
    color_discrete_map=area_colour_map,
    barmode='relative',
    text_auto='.2f',
    height=200,
)
fig.update_layout(showlegend=False)
st.subheader(f"Total Number of Crimes per {area_scale} for All Crime")
st.plotly_chart(fig, use_container_width=True)

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
    color=area_scale,
    color_discrete_sequence=area_colours,
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
            'xshift': -110,
            'y': 1,
            'yanchor': 'bottom',
            'yref': 'paper',
            'yshift': 7,
            'showarrow': False,
            'font': {'size': 16},
            'borderpad': 5,
        },
    ],
    showlegend=False,
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
    x='Count_Per_100',
    y='Crime',
    color=area_scale,
    facet_col=area_scale,
    category_orders={'Crime': crimes},
    animation_frame='Year',
    animation_group='Crime',
    color_discrete_map=area_colour_map,
    height=600,
)
st.subheader(f"Total Number of Crimes in WA per {area_scale} Over Time (per Year)")
st.plotly_chart(fig, use_container_width=True)

# Bar chart over time
fig = px.bar(
    crimes_df_over_time,
    x='Count_Per_100_Norm',
    y='Crime',
    color=area_scale,
    category_orders={'Crime': crimes},
    animation_frame='Year',
    animation_group='Crime',
    color_discrete_map=area_colour_map,
    height=600,
)
st.subheader(f"Relative Total Number of Crimes in WA per {area_scale} Over Time (per Year)")
st.plotly_chart(fig, use_container_width=True)