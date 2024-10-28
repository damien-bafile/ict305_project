import streamlit as st
import pandas as pd
import plotly.express as px
from catppuccin import PALETTE

from helpers.DataLoading import loadData
from helpers.CrimeData import getCrimeCounts


@st.cache_data
def load_data(filename, file_path, sheet_name):
    crimes_df = loadData(filename, file_path, sheet_name)
    return crimes_df


area_scale = 'District'


# Title of the app
st.title(f"Crime by {area_scale}")

# Figure container margins
_, centre, _ = st.columns([0.05, 0.9, 0.05])

# Colour palette
colours = [colour.hex for colour in PALETTE.latte.colors]

# Load the data from the Excel file (this assumes you have the file in the same directory)
filename = 'data.xlsx'
file_path = 'assets'
sheet_name = 'Data'

crimes_df = load_data(filename, file_path, sheet_name)

crimes_df[f'{area_scale}_Name'] = crimes_df[area_scale].apply(lambda x: ''.join(x.split()[:-1]).title())
crimes_df_total = getCrimeCounts(crimes_df, area_scale = area_scale, ascending = True)
crimes_df_over_time = getCrimeCounts(crimes_df, group_by = ['Year'], sort = False, area_scale = area_scale)

areas = crimes_df_total[f'{area_scale}_Name'].unique()
crimes = crimes_df_total['Crime'].unique()
crime_order = crimes[::-1]
colour_map = dict(zip(crimes, colours[:len(crimes)]))
area_colour_map = dict(zip(areas, colours[:len(areas)]))

x_min = crimes_df_total['Count_Per_100'].min()
x_max = crimes_df_total['Count_Per_100'].max()
x_time_min = crimes_df_over_time['Count_Per_100'].min()
x_time_max = crimes_df_over_time['Count_Per_100'].max()


with centre:

    # Bar chart with dropdown menu

    # Bar chart figure
    fig = px.bar(
        crimes_df_total[crimes_df_total['Crime'] == crimes[0]],
        x = 'Count_Per_100',
        y = f'{area_scale}_Name',
        color_discrete_sequence = [colour_map[crimes[0]]],
        text_auto = '.2f',
        width = 700,
        height = 600,
    )

    # Dropdown menu
    dropdown = [
        {
            'args': [
                {
                    'x': [crimes_df_total[crimes_df_total['Crime'] == crime]['Count_Per_100']],
                    'y': [crimes_df_total[crimes_df_total['Crime'] == crime][f'{area_scale}_Name']],
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
                'pad': {'t': 5},
                'x': 1,
                'xanchor': 'right',
                'y': 1.1,
                'yanchor': 'top',
                'font': {'size': 16},
            },
        ],
        annotations = [
            {
                'text': 'Select Crime Category:',
                'x': 1,
                'xanchor': 'right',
                'xref': 'paper',
                'y': 1.15,
                'yanchor': 'top',
                'yref': 'paper',
                'showarrow': False,
                'font': {'size': 16},
            },
        ],
        margin = {'t': 75, 'r': 10, 'b': 20, 'l': 10},
    )
    
    st.subheader(f"Total Number of Crimes per {area_scale} (2007-2024)")

    st.plotly_chart(fig, use_container_width = True)
    
    
    # Bar chart with dropdown menu

    # Bar chart figure
    fig = px.bar(
        crimes_df_total[crimes_df_total[f'{area_scale}_Name'] == areas[0]],
        x = 'Count_Per_100',
        y = 'Crime',
        color_discrete_sequence = [area_colour_map[areas[0]]],
        text_auto = '.2f',
        width = 700,
        height = 600,
    )

    # Dropdown menu
    dropdown = [
        {
            'args': [
                {
                    'x': [crimes_df_total[crimes_df_total[f'{area_scale}_Name'] == area]['Count_Per_100']],
                    'y': [crimes_df_total[crimes_df_total[f'{area_scale}_Name'] == area]['Crime']],
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
                'pad': {'t': 5},
                'x': 1,
                'xanchor': 'right',
                'y': 1.1,
                'yanchor': 'top',
                'font': {'size': 16},
            },
        ],
        annotations = [
            {
                'text': f'Select {area_scale}:',
                'x': 1,
                'xanchor': 'right',
                'xref': 'paper',
                'y': 1.15,
                'yanchor': 'top',
                'yref': 'paper',
                'showarrow': False,
                'font': {'size': 16},
            },
        ],
        margin = {'t': 75, 'r': 10, 'b': 20, 'l': 10},
    )
    
    st.subheader(f"Total Number of Crimes per {area_scale} (2007-2024)")

    st.plotly_chart(fig, use_container_width = True)


    # Bar chart

    fig = px.bar(
        crimes_df_total,
        x = 'Count_Per_100',
        y = f'{area_scale}_Name',
        color = 'Crime',
        #category_orders = {'Crime': crime_order},
        color_discrete_sequence = colours[::-1],
        barmode = 'relative',
        #range_x = [x_min, x_max],
        title = f'Total Number of Crimes per {area_scale} (2007-2024)',
        width = 700,
        height = 800,
    )

    st.plotly_chart(fig, use_container_width = True)


    # Bar chart over time

    fig = px.bar(
        crimes_df_over_time,
        x = 'Count_Per_100',
        y = 'Crime',
        color = f'{area_scale}_Name',
        animation_frame = 'Year',
        animation_group = 'Crime',
        category_orders = {'Crime': crime_order},
        color_discrete_sequence = colours,
        barmode = 'relative',
        range_x = [x_time_min, x_time_max],
        title = f'Total Number of Crimes per {area_scale} Over Time (2007-2024)',
        width = 700,
        height = 800,
    )

    st.plotly_chart(fig, use_container_width = True)


    # Scatter plot

    fig = px.scatter(
        crimes_df_total,
        x = 'Count_Per_100',
        y = 'Crime',
        color = f'{area_scale}_Name',
        category_orders = {'Crime': crime_order},
        color_discrete_sequence = colours,
        range_x = [x_min, x_max],
        title = f'Total Number of Crimes per {area_scale} (2007-2024)',
        width = 700,
        height = 600,
    )

    st.plotly_chart(fig, use_container_width = True)


    # Scatter plot over time

    fig = px.scatter(
        crimes_df_over_time,
        x = 'Count_Per_100',
        y = 'Crime',
        color = f'{area_scale}_Name',
        animation_frame = 'Year',
        animation_group = 'Crime',
        category_orders = {'Crime': crime_order},
        color_discrete_sequence = colours,
        range_x = [x_time_min, x_time_max],
        title = f'Total Number of Crimes per {area_scale} Over Time (2007-2024)',
        width = 700,
        height = 600,
    )

    st.plotly_chart(fig, use_container_width = True)