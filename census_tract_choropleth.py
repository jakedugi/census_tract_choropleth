import os
import geopandas as gpd
import pandas as pd


def convert_to_geojson(directory, output_path):
    shp_files = [file for file in os.listdir(directory) if file.endswith(".shp")]
    if len(shp_files) > 0:
        gdf_list = []
        for shp_file in shp_files:
            shp_path = os.path.join(directory, shp_file)
            try:
                gdf = gpd.read_file(shp_path)
                # Check if there are invalid geometries and repair them
                gdf["geometry"] = gdf["geometry"].apply(
                    lambda geom: geom.buffer(0) if not geom.is_valid else geom
                )
                gdf_list.append(gdf)
            except Exception as e:
                print(f"Error reading {shp_path}: {e}")
        combined_gdf = gpd.GeoDataFrame(pd.concat(gdf_list, ignore_index=True))
        # Save the GeoDataFrame as GeoJSON with ".geojson" extension
        combined_gdf.to_file(output_path, driver="GeoJSON")
        return output_path
    else:
        return None


# Directory path
directory_path = "Your_Directory_Path"
# Specify the output file path with ".geojson" extension
output_file_path = "Your_Path\\tracts1.geojson"
# Convert to GeoJSON and save the output file
output_file_path = convert_to_geojson(directory_path, output_file_path)
# Print the output file path
print("Output GeoJSON file:", output_file_path)


import pandas as pd


def process_csv(input_file, output_file, columns_to_keep):
    try:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(input_file)

        # Remove the second row
        df = df.drop(0)  # Assuming rows are 0-indexed

        # Keep only the specified columns
        df = df[columns_to_keep]

        # Save the processed DataFrame to a new CSV file
        df.to_csv(output_file, index=False)

        print(f"Processed CSV saved to {output_file}")

    except Exception as e:
        print(f"Error: {str(e)}")


input_file = r"Your_Path\\ACSST5Y2021.S2701-Data.csv"
output_file = r"Your_Path\\censustractdata\Blog_Data.csv"
columns_to_keep = ["GEO_ID", "S2701_C01_001E"]

process_csv(input_file, output_file, columns_to_keep)

import pandas as pd


# Function to convert and save CSV
def convert_and_save_csv(
    input_csv_file, output_csv_file, selected_columns, column_rename_mapping
):
    # Load the CSV file without specifying data types
    df = pd.read_csv(input_csv_file)

    # Rename columns using the provided mapping
    df.rename(columns=column_rename_mapping, inplace=True)

    # Select the specified columns
    df = df[selected_columns]

    # Convert 'S2701_C03_001E' column to float with NaN for non-float values
    df["Total_Population"] = pd.to_numeric(df["Total_Population"], errors="coerce")

    # Fill missing values with 0
    df["Total_Population"].fillna(0, inplace=True)

    df["GEOID"] = df["GEOID"].str[9:]

    # Save the modified DataFrame to a new CSV file
    df.to_csv(output_csv_file, index=False)

    # Check data types of columns
    data_types = df.dtypes

    # Check for missing values
    missing_values = df.isnull().sum()

    return data_types, missing_values


# Load the CSV file into a DataFrame
csv_file_path = "Your_Path/censustractdata/Blog_Data.csv"
df = pd.read_csv(csv_file_path)

# Rename the 'S2701_C03_001E' column to a new name
new_column_name = "Total_Population"
df.rename(columns={"S2701_C03_001E": new_column_name}, inplace=True)

# Extract the 'New_Column_Name' column
column_to_analyze = new_column_name

# Convert the column to numeric (assuming it contains numeric data)
df[column_to_analyze] = pd.to_numeric(df[column_to_analyze], errors="coerce")

# Calculate custom percentiles
custom_percentiles = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 99, 100]

# Calculate the values for custom percentiles
percentile_values = [
    df[column_to_analyze].quantile(p / 100) for p in custom_percentiles
]

# Get the min and max values
min_value = df[column_to_analyze].min()
max_value = df[column_to_analyze].max()

# Display the summary statistics
print("Summary Statistics:")
print(f"min: {min_value}")
for p, value in zip(custom_percentiles, percentile_values):
    print(f"{p}%ile: {value}")
print(f"max: {max_value}")

# Save the DataFrame to a new CSV file
new_csv_file_path = "Your_Path\\censustractdata/New_Blog_Data.csv"
df.to_csv(new_csv_file_path, index=False)

# Example usage:
input_csv_file = r"Your_Path\\Blog_Data.csv"
output_csv_file = r"Your_Path\\Blog_Data_Processed.csv"
selected_columns = ["GEOID", "Total_Population"]

# Define the column rename mapping
column_rename_mapping = {"GEO_ID": "GEOID", "S2701_C03_001E": "Total_Population"}

# Call the function to convert and save the CSV file with missing values filled with 0
data_types, missing_values = convert_and_save_csv(
    input_csv_file, output_csv_file, selected_columns, column_rename_mapping
)

# Print data types and missing values
print("Data Types:")
print(data_types)

print("\nMissing Values:")
print(missing_values)


import pandas as pd
import json
import plotly.express as px


def catestvisual():
    # Read the CSV file as df
    csv_file = "Your_Path\\Blog_Data_Processed.csv"
    df = pd.read_csv(
        csv_file, dtype={"GEOID": object, "GEO_ID": object, "Total_Population": int}
    )

    # Select the specified columns
    df = df[["GEOID", "GEO_ID", "Total_Population"]]

    df = df[df["Total_Population"] > 0]

    # Check data types of columns
    print("Data Types:")
    print(df.dtypes)

    # Check for missing values
    print("\nMissing Values:")
    print(df.isnull().sum())

    with open("Your_Path\\accesstoken.txt", "r") as token_file:
        token = token_file.read().strip()

    # Load the JSON data for California tracts
    with open("Your_Path\\blog_tracts_zip.json", "r") as json_file:
        json_data = json.load(json_file)

    # Can use a diffrent access token
    mapbox_access_token = "<pk.YOUR ACCESS TOKEN HERE>"
    px.set_mapbox_access_token(mapbox_access_token)

    # Create the choropleth map
    fig = px.choropleth_mapbox(
        df,
        geojson=json_data,
        locations="GEOID",
        color="Total_Population",
        color_continuous_scale="Reds",
        range_color=(0, 8600),
        featureidkey="properties.GEOID",
        mapbox_style="light",
        zoom=3.5,
        opacity=1.0,
        center={"lat": 37.0902, "lon": -95.7129},
        title="Health Insurance Coverage by Tract",
        hover_data={"Total_Population": True, "GEO_ID": True},
        labels={
            "Total_Population": "Total Population",
            "GEO_ID": "3-digit summary level+2-digit geographic variant+2-digit geographic component+'US'+STATE+COUNTY+TRACT",
        },
    )

    fig = fig.update_traces(
        marker_line_width=0.000000001,
        marker_line_color="#D3D3D3",
    )

    fig.update_layout(
        margin={"r": 0, "t": 25, "l": 0, "b": 0},
        title={"xanchor": "center", "x": 0.5},
        coloraxis_colorbar={
            "title": "Estimated Total Population",
            "title_side": "bottom",
            "tickformat": ".1f",
            "tickvals": [0, 1931, 2493, 2943, 3355, 3754, 4170, 4648, 5244, 6114, 8600],
            "ticktext": [
                "0%:0",
                "10%:1931",
                "20%:2493",
                "30%:2943",
                "40%:3355",
                "50%:3754",
                "60%:4170",
                "70%:4648",
                "80%:5244",
                "90%:6114",
                "99%:8600",
            ],
            "orientation": "h",
            "x": 0.5,
            "xanchor": "center",
            "y": -0.00000001,
            "yanchor": "top",
            "len": 0.9,
        },
        annotations=[
            dict(
                text="Source: U.S. Census Bureau 2023 Shapefiles,<br>American Community Survey 2021 5-Yr Estimate Census Tract Level Data",
                xref="paper",
                yref="paper",
                x=0.01,
                y=0.01,
                showarrow=False,
                font=dict(size=10),
                align="left",
            )
        ],
    )

    fig.write_html("Your_Path\\Blog_choropleth_map_FINAL.html")
    fig.show()


if __name__ == "__main__":
    catestvisual()
