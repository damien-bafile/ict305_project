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
crimes_df_district_total = getCrimeCounts(
    crimes_df.drop(columns='Crime'),
    area_scale=area_scale,
    group_by=['Population'],
    sort_by=['Count_Per_100', 'Count'],
    ascending=True,
)
crimes_df_over_time = getCrimeCounts(crimes_df, group_by=['Year'], sort=False, area_scale=area_scale)

areas = crimes_df_district_total[area_scale].unique()[::-1]
crimes = crimes_df_total['Crime'].unique()[::-1]

# Colour palette
colours = [colour.hex for colour in PALETTE.latte.colors]
crime_colours = colours[:len(crimes)]
#crime_colours = sorted(crime_colours)
area_colours = colours[:len(areas)]
#area_colours = sorted(area_colours)
crime_colour_map = dict(zip(crimes, crime_colours))
area_colour_map = dict(zip(areas, area_colours))

x_min = crimes_df_total['Count_Per_100'].min()
x_max = crimes_df_total['Count_Per_100'].max()
x_time_min = crimes_df_over_time['Count_Per_100'].min()
x_time_max = crimes_df_over_time['Count_Per_100'].max()


# Crime count over opulation
st.header("Crime Count Over District Population")
st.write(
    "The scatter plot illustrates the relationship between the amount of crime in a district "
    "and the district's population."
)

# Figure container margins
left, right = st.columns([0.5, 0.5])

# Scatter plot
fig = px.scatter(
    crimes_df_district_total,
    x='Count',
    y='Population',
    color=area_scale,
    size='Count',
    color_discrete_map=area_colour_map,
    height=500,
)
left.subheader(f"Raw Crime Count")
left.plotly_chart(fig, use_container_width=True)

# Scatter plot
fig = px.scatter(
    crimes_df_district_total,
    x='Count_Per_100',
    y='Population',
    color=area_scale,
    size='Count_Per_100',
    color_discrete_map=area_colour_map,
    height=500,
)
right.subheader(f"Crime Count Scaled per 100 Residents")
right.plotly_chart(fig, use_container_width=True)
st.divider()


# By crime
st.header("Crime Statistics Displayed by Crime Category")
st.write("This section shows the total number of crimes for each crime category per district.")

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
    category_orders={area_scale: areas, 'Crime': crimes},
    color_discrete_sequence=area_colours,
    height=600,
)
fig.update_layout(updatemenus=[{'pad': {'b': 5, 'r': 1}}])
left.subheader(f"Crime Counts per Category Proportional to the Total for All {area_scale}s")
left.plotly_chart(fig, use_container_width=True)

# Bar chart with dropdown menu
fig = px.bar(
    crimes_df_total[crimes_df_total[area_scale] == areas[0]],
    x='Count_Per_100',
    y='Crime',
    color=area_scale,
    color_discrete_map=area_colour_map,
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
    showlegend=False,
)
right.subheader(f"Crime Categories Ranked per {area_scale}")
right.plotly_chart(fig, use_container_width=True)

# Scatter plot
fig = px.scatter(
    crimes_df_total,
    x='Count_Per_100',
    y='Crime',
    color=area_scale,
    category_orders={area_scale: areas, 'Crime': crimes},
    color_discrete_map=area_colour_map,
    range_x=[x_min, x_max],
    height=500,
)
st.subheader(f"Total Number of Crimes per Category per {area_scale}")
st.plotly_chart(fig, use_container_width=True)
st.divider()


# By district
st.header(f"Crime Statistics Displayed by {area_scale}")
st.write("This section shows the total number of crimes in each district per crime category.")

# Bar chart
fig = px.bar(
    crimes_df_district_total,
    x='Count_Per_100',
    y=area_scale,
    color=area_scale,
    category_orders={area_scale: areas, 'Crime': crimes},
    color_discrete_map=area_colour_map,
    text_auto='.2f',
    height=500,
)
fig.update_layout(showlegend=False)
st.subheader(f"{area_scale}s Ranked by Total Number of Crimes Across All Categories")
st.plotly_chart(fig, use_container_width=True)

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
    category_orders={area_scale: areas, 'Crime': crimes},
    color_discrete_sequence=crime_colours,
    height=550,
)
fig.update_layout(updatemenus=[{'pad': {'b': 5, 'r': 1}}])
left.subheader(f"Crime Counts per {area_scale} Proportional to the Total for All Categories")
left.plotly_chart(fig, use_container_width=True)

# Bar chart with dropdown menu
fig = px.bar(
    crimes_df_total[crimes_df_total['Crime'] == crimes[0]],
    x='Count_Per_100',
    y=area_scale,
    color='Crime',
    color_discrete_map=crime_colour_map,
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
    for crime, colour in crime_colour_map.items()
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
    showlegend=False,
)
right.subheader(f"{area_scale}s Ranked by Number of Crimes for Each Category")
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
    category_orders={area_scale: areas, 'Crime': crimes},
    color_discrete_map=area_colour_map,
    height=600,
)
st.subheader(f"Crime Counts for Each Category Proportional to the Total for All {area_scale}s Over Time (per Year)")
st.plotly_chart(fig, use_container_width=True)

# Scatter plot over time
fig=px.scatter(
    crimes_df_over_time,
    x='Count_Per_100',
    y='Crime',
    color=area_scale,
    animation_frame='Year',
    animation_group='Crime',
    category_orders={area_scale: areas, 'Crime': crimes},
    color_discrete_map=area_colour_map,
    range_x=[x_time_min, x_time_max],
    height=600,
)
st.subheader(f"Total Number of Crimes of Each Category per {area_scale} Over Time (per Year)")
st.plotly_chart(fig, use_container_width=True)