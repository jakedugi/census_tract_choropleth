import pandas as pd
import json
import plotly.express as px

def generate_choropleth(csv_file, json_file, token_file, output_html):
    df = pd.read_csv(csv_file, dtype={'GEOID': object, 'GEO_ID': object, 'Total_Population': int})
    df = df[['GEOID', 'GEO_ID', 'Total_Population']]
    df = df[df['Total_Population'] > 0]
    print("Data Types:\n", df.dtypes)
    print("\nMissing Values:\n", df.isnull().sum())

    with open(token_file, "r") as f:
        px.set_mapbox_access_token(f.read().strip())

    with open(json_file, 'r') as f:
        geojson_data = json.load(f)

    fig = px.choropleth_mapbox(
        df,
        geojson=geojson_data,
        locations='GEOID',
        color='Total_Population',
        color_continuous_scale="Reds",
        range_color=(0, 8600),
        featureidkey="properties.GEOID",
        mapbox_style="light",
        zoom=3.5,
        opacity=1.0,
        center={"lat": 37.0902, "lon": -95.7129},
        hover_data={'Total_Population': True, 'GEO_ID': True},
        labels={
            'Total_Population': "Total Population",
            'GEO_ID': "Geographic ID"
        }
    )

    fig.update_traces(marker_line_width=0.000000001, marker_line_color='#D3D3D3')

    fig.update_layout(
        margin={"r": 0, "t": 25, "l": 0, "b": 0},
        title={'xanchor': 'center', 'x': 0.5},
        coloraxis_colorbar={
            'title': 'Estimated Total Population',
            'title_side': 'bottom',
            'orientation': 'h',
            'tickformat': '.1f',
            'tickvals': [0, 1931, 2493, 2943, 3355, 3754, 4170, 4648, 5244, 6114, 8600],
            'ticktext': ['0%:0', '10%:1931', '20%:2493', '30%:2943', '40%:3355', '50%:3754', '60%:4170', '70%:4648', '80%:5244', '90%:6114', '99%:8600'],
            'x': 0.5,
            'xanchor': 'center',
            'y': -0.00000001,
            'yanchor': 'top',
            'len': 0.9
        },
        annotations=[{
            'text': 'Source: U.S. Census Bureau, American Community Survey 2021',
            'xref': 'paper', 'yref': 'paper', 'x': 0.01, 'y': 0.01,
            'showarrow': False, 'font': {'size': 10}, 'align': 'left'
        }]
    )

    fig.write_html(output_html)
    fig.show()