import pandas as pd
import json
import plotly.express as px


def generate_choropleth(csv_file, json_file, token_file, output_html):
    """
    Generate an interactive choropleth map using Census tract data.

    Args:
        csv_file: Path to processed CSV with tract data
        json_file: Path to GeoJSON with tract boundaries
        token_file: Path to Mapbox access token file
        output_html: Path to save the output HTML map
    """
    try:
        # Read and prepare data
        df = pd.read_csv(csv_file, dtype={"GEOID": str})

        # Ensure GEOID is properly formatted
        if "GEOID" not in df.columns:
            raise ValueError("CSV file must contain a 'GEOID' column")

        # Load GeoJSON
        with open(json_file, "r") as f:
            geojson_data = json.load(f)

        # Verify GeoJSON structure
        if "features" not in geojson_data:
            raise ValueError("Invalid GeoJSON structure: 'features' not found")

        # Get available GEOIDs from GeoJSON for validation
        geojson_geoids = {
            feature["properties"]["GEOID"]
            for feature in geojson_data["features"]
            if "properties" in feature and "GEOID" in feature["properties"]
        }

        # Check for GEOID matches
        matching_geoids = set(df["GEOID"].astype(str)) & geojson_geoids
        if not matching_geoids:
            raise ValueError("No matching GEOIDs found between CSV and GeoJSON")

        print(f"Found {len(matching_geoids)} matching GEOIDs")

        # Load Mapbox token
        with open(token_file, "r") as f:
            px.set_mapbox_access_token(f.read().strip())

        # Create choropleth
        fig = px.choropleth_mapbox(
            df,
            geojson=geojson_data,
            locations="GEOID",
            color="Total_Population",
            color_continuous_scale="Reds",
            range_color=(0, df["Total_Population"].quantile(0.99)),
            featureidkey="properties.GEOID",
            mapbox_style="light",
            zoom=3.5,
            opacity=1.0,
            center={"lat": 37.0902, "lon": -95.7129},
            hover_data={"Total_Population": True},
            labels={"Total_Population": "Total Population"},
        )

        fig.update_traces(marker_line_width=0.000000001, marker_line_color="#D3D3D3")

        fig.update_layout(
            margin={"r": 0, "t": 25, "l": 0, "b": 0},
            title={
                "text": "Census Tract Population Distribution",
                "xanchor": "center",
                "x": 0.5,
            },
            coloraxis_colorbar={
                "title": "Total Population",
                "title_side": "bottom",
                "orientation": "h",
                "x": 0.5,
                "xanchor": "center",
                "y": -0.00000001,
                "yanchor": "top",
                "len": 0.9,
            },
            annotations=[
                {
                    "text": "Source: U.S. Census Bureau, American Community Survey",
                    "xref": "paper",
                    "yref": "paper",
                    "x": 0.01,
                    "y": 0.01,
                    "showarrow": False,
                    "font": {"size": 10},
                    "align": "left",
                }
            ],
        )

        # Save the map
        fig.write_html(output_html)
        print(f"Choropleth map saved to: {output_html}")

        return fig

    except Exception as e:
        print(f"Error generating choropleth: {str(e)}")
        raise
