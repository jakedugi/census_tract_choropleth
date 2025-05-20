# U.S. Census Tract Level Choropleth Map in Python, Highly Granular Geospatial Visualization
A full pipeline for creating highly granular, interactive choropleth maps of U.S. Census Tracts using public data and modern geospatial visualization tools. 84,414 polygons. 
**By [Jake Dugan](https://www.linkedin.com/in/jakedugi)**
**Blog-style walkthrough on Medium**: [Read the full breakdown here](https://your-medium-blog-link.com)


![image](https://github.com/user-attachments/assets/900e99a4-9aec-4930-b9c6-4338fbd51232)

Most choropleth polygons are nations, states/provinces, or counties/municipalities. However, what if we want to visualize data at a more granular level, such as census tracts? Census tracts are more detailed than counties, have complete coverage of the U.S., unlike zip codes, and have standard population sizes of around 4,000 people per tract. This is a straight-to-the-point technical summary. Choropleths need two basic types of inputs: polygons and data.

# Polygons:
For the “bones” of the choropleth, we need a GeoJSON containing the coordinate point outlines of the regions we are trying to visualize. We can find these for the United States at https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html under FTP Archive by Layer under TRACT/. These are the .zips contacting the .shp .dbf files necessary for creating our GEOJSONs. The names of the files are in the form tl_rd22_01_tract.zip which stands for TigerLine_Redistricting2022_statefipcode_tract.zip. So make sure that you update the year in this code as necessary. It is not just states in this folder but also territories such as Guam and the Northern Mariana Islands, among others. Here is a link to the FIPS codes with their names https://www2.census.gov/geo/docs/reference/codes2020/national_state2020.txt. For the sake of time, we will just focus on the 50 U.S. states. 

# Transform to GeoJSON and Combine:
Combine all the zipped .shp into one GeoJSON. They need to be unzipped into the same folder.

```
import os
import geopandas as gpd
import pandas as pd

def convert_to_geojson(directory, output_path):
    shp_files = [file for file in os.listdir(directory) if file.endswith('.shp')]
    if len(shp_files) > 0:
        gdf_list = []
        for shp_file in shp_files:
            shp_path = os.path.join(directory, shp_file)
            try:
                gdf = gpd.read_file(shp_path)
                # Check if there are invalid geometries and repair them
                gdf['geometry'] = gdf['geometry'].apply(lambda geom: geom.buffer(0) if not geom.is_valid else geom)
                gdf_list.append(gdf)
            except Exception as e:
                print(f"Error reading {shp_path}: {e}")
        combined_gdf = gpd.GeoDataFrame(pd.concat(gdf_list, ignore_index=True))
        # Save the GeoDataFrame as GeoJSON with ".geojson" extension
        combined_gdf.to_file(output_path, driver="GeoJSON")
        return output_path
    else:
        return None


directory_path = 'YOUR_PATH/tractzips/'

output_file_path = 'YOUR_PATH/tracts1.geojson'

output_file_path = convert_to_geojson(directory_path, output_file_path)

print("Output GeoJSON file:", output_file_path)
```

# Simplify:
The main reason highly granular choropleths are not used is their size. A simplified census tract level choropleth will be 2+ GBs, making them impossible to render. Simplification techniques make highly granular choropleths possible. With simplification, census tract level choropleths of the U.S. can become as small as 100 MBs.

Douglas-Peuker is a popular method used for geometry simplification however, I found it turns small geometries into triangles too quickly. We will use Visvalingam / weighted area. It works by iteratively removing the least important points based on a weighted average of their triangle areas, resulting in a simplified but visually similar representation of the original path. It is helpful to visually assess the degree of simplification to avoid overdoing it. I opt for https://mapshaper.org/ it allows you to determine the degree of simplification in real-time.

In Mapshaper, select the combined GeoJSON file, select detect line intersections, import, select simplify, select prevent shape removal, Visvalingam / weighted area, and apply. Zoom into a metro area like Dallas, setting slider should be set to 5%-3%, repair line intersections created by the simplification process, export, name as simplified version, file format GeoJSON, and export. The simplified GeoJSON has been decreased from 1.4GB to 85MB. This is our final GeoJSON. tracts1.geojson is now blog_tracts_zip.json for this example.

# Data:
For the “meat” of the choropleth, we need a pandas data frame containing the census tract-level data we wish to visualize. Data sources easily linkable to census tracts could be data present in the GeoJSON under properties, Census data, American Community Survey data, and you can use the census tract centroid INTPTLAT, INTPTLON to produce straight-line distances for estimated travel times (see future Stroke Center Accessibility). For this, we will link American Community Survey data. Go to https://data.census.gov/advanced, Select Geography, Census Tract, Select State or all States, View Filters, Topics find a topic, for this tutorial income and poverty, income and earnings, Income (Households, Families, Individuals), View Filters, Search, we will use S2701: SELECTED CHARACTERISTICS OF HEALTH INSURANCE COVERAGE IN THE UNITED STATES, download table, select latest year, download .csv.

Unzip, look at Column Metadata, choose columns of data to use, estimate rows are the totals, the rest are comments, and input the names of the rows to keep. We need to keep GEO_ID for linking but change the format. Removing the second row that has names in it. 

```
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

# Example usage:
input_file = r'YOUR_PATH\ACSST5Y2021.S2701-Data.csv'
output_file = r'YOUR_PATH\Blog_Data.csv'
columns_to_keep = ['GEO_ID','S2701_C01_001E']

process_csv(input_file, output_file, columns_to_keep)
```

S2701_C01_001E : Estimate!!Total!! population.
Here are some other columns you could play with. S2701_C01_004E : Estimate!!Total!!AGE!!19 to 25 years, 6S2701_C01_005E : Estimate!!Total!!AGE!!26 to 34 years, S2701_C01_014E : Estimate!!Total!!SEX!!Male, S2701_C01_015E : Estimate!!Total!!SEX!!Female, S2701_C01_041E : Estimate!!Total!!Bachelor’s degree or higher, S2701_C01_056E : Estimate!!Total!!HOUSEHOLD INCOME!!$100,000 and over, S2701_C03_001E : Estimate!!Percent Insured!! population

# Analysis:
We are going to analyze the column of data we wish to visualize to find out more about the distribution and percentiles. If skewed you can log transform the data see my future Stroke Center Accessibility! For this tutorial, we use S2701_C01_001E : Estimate!!Total!! population. To see how far from the mean of 4,000 Pax that each census tract the census borough is shooting for. You need to remove the first 9 digits of the Geo_ID to match the GEOID in the JSON in this format “GEOID”:”01117030611" https://ask.census.gov/prweb/PRServletCustom/app/ECORRAsk2/YACFBFye-rFIz_FoGtyvDRUGg1Uzu5Mn*/!STANDARD?pzuiactionzzz=CXtpbn0rTEpMcGRYOG1vS0tqTFAwaENUZWpvM1NNWEMzZ3p5aFpnWUxzVmw0TjJoOEprcE5BQndaM1Vid1FKbWRibnZu*. 

```
import pandas as pd

def convert_and_save_csv(input_csv_file, output_csv_file, selected_columns, column_rename_mapping):
    # Load the CSV file without specifying data types
    df = pd.read_csv(input_csv_file)

    # Rename columns using the provided mapping
    df.rename(columns=column_rename_mapping, inplace=True)

    # Select the specified columns
    df = df[selected_columns]

    # Convert 'S2701_C03_001E' column to float with NaN for non-float values
    df['Total_Population'] = pd.to_numeric(df['Total_Population'], errors='coerce')

    # Fill missing values with 0
    df['Total_Population'].fillna(0, inplace=True)

    df['GEOID'] = df['GEOID'].str[9:]

    # Save the modified DataFrame to a new CSV file
    df.to_csv(output_csv_file, index=False)

    # Check data types of columns
    data_types = df.dtypes

    # Check for missing values
    missing_values = df.isnull().sum()

    return data_types, missing_values

# Load the CSV file into a DataFrame
csv_file_path = 'YOUR_PATH/Blog_Data.csv'
df = pd.read_csv(csv_file_path)

# Rename the 'S2701_C03_001E' column to a new name
new_column_name = 'Total_Population'
df.rename(columns={'S2701_C03_001E': new_column_name}, inplace=True)

# Extract the 'New_Column_Name' column
column_to_analyze = new_column_name

# Convert the column to numeric (assuming it contains numeric data)
df[column_to_analyze] = pd.to_numeric(df[column_to_analyze], errors='coerce')

# Calculate custom percentiles
custom_percentiles = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 99, 100]

# Calculate the values for custom percentiles
percentile_values = [df[column_to_analyze].quantile(p / 100) for p in custom_percentiles]

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
new_csv_file_path = 'YOUR_PATH/New_Blog_Data.csv'
df.to_csv(new_csv_file_path, index=False)

# Example usage:
input_csv_file = r'YOUR_PATH/Blog_Data.csv'
output_csv_file = r'YOUR_PATH/Blog_Data_Processed.csv'
selected_columns = ['GEOID', 'Total_Population']

# Define the column rename mapping
column_rename_mapping = {
    'GEO_ID': 'GEOID',  
    'S2701_C03_001E':'Total_Population'
}

# Call the function to convert and save the CSV file with missing values filled with 0
data_types, missing_values = convert_and_save_csv(input_csv_file, output_csv_file, selected_columns, column_rename_mapping)

# Print data types and missing values
print("Data Types:")
print(data_types)

print("\nMissing Values:")
print(missing_values)
```

Summary Statistics: [0, 1931, 2493, 2943, 3355, 3754, 4170, 4648, 5244, 6114, 8600], 'ticktext': ['0%:0', '10%:1931', '20%:2493', '30%:2943', '40%:3355', '50%:3754', '60%:4170', '70%:4648', '80%:5244', '90%:6114', '99%:8600'],

The largest population tracts are military bases, which are outliers to the 4,000 population rule. We will use these to construct our choropleth legend.

# Choropleth:
For the base map, I like to use Mapbox choropleth. You need an API access token to access their light base map. https://account.mapbox.com/access-tokens/ create an account, create an access token, and add to a file (“YOUR_PATH/accesstoken.txt”, “r”), ( mapbox_access_token = “pk.YOUR_TOKEN”

px.set_mapbox_access_token(mapbox_access_token)), (mapbox_style=”light”,). Most issues are because of data types. dtype={‘GEOID’:object,’GEO_ID’:object,’Total_Population’:int}). Make sure these are correct all nan values are filled. df = df[df[‘Total_Population’] > 0] so that it only shows polygons that have a pop greater than zero. Some irrelevant tracts with populations of 0 exist. locations and feature id keys need to be the same. locations=’GEOID’, featureidkey=”properties.GEOID”, This is what links the data to the polygons. labels rounded to the nearest int you can change accordingly. Here is more info on the parameters https://plotly.github.io/plotly.py-docs/generated/plotly.express.choropleth_mapbox.html;. This code is for the legend ‘tickvals’: [0, 1931, 2493, 2943, 3355, 3754, 4170, 4648, 5244, 6114, 8600],
‘ticktext’: [‘0%:0’, ‘10%:1931’, ‘20%:2493’, ‘30%:2943’, ‘40%:3355’, ‘50%:3754’, ‘60%:4170’, ‘70%:4648’, ‘80%:5244’, ‘90%:6114’, ‘99%:8600’],
‘orientation’: ‘h’,. This saves as an html file open in any browser.

```
import pandas as pd
import json
import plotly.express as px

def catestvisual():
    # Read the CSV file as df
    csv_file = 'YOUR_PATH/Blog_Data_Processed.csv'
    df = pd.read_csv(csv_file, dtype={'GEOID':object,'GEO_ID':object,'Total_Population':int})
    
    # Select the specified columns
    df = df[[ 'GEOID','GEO_ID','Total_Population']]
 
    
    df = df[df['Total_Population'] > 0]

    # Check data types of columns
    print("Data Types:")
    print(df.dtypes)

    # Check for missing values
    print("\nMissing Values:")
    print(df.isnull().sum())

    with open("YOUR_PATH/accesstoken.txt", "r") as token_file:
        token = token_file.read().strip()

    # Load the JSON data for California tracts
    with open('YOUR_PATH/blog_tracts_zip.json', 'r') as json_file:
        json_data = json.load(json_file)

    mapbox_access_token = "<pk.YOUR ACCESS TOKEN>"
    px.set_mapbox_access_token(mapbox_access_token)

    # Create the choropleth map
    fig = px.choropleth_mapbox(df,
                                geojson=json_data,
                                locations='GEOID',
                                color='Total_Population',
                                color_continuous_scale="Reds",
                                range_color=(0, 8600),
                                featureidkey="properties.GEOID",
                                mapbox_style="light",
                                zoom=3.5,
                                opacity=1.0,
                                center={"lat": 37.0902, "lon": -95.7129},
                                title='Health Insurance Coverage by Tract',
                                hover_data={'Total_Population':True,'GEO_ID':True},
                                labels={'Total_Population':"Total Population",'GEO_ID':"3-digit summary level+2-digit geographic variant+2-digit geographic component+“US”+STATE+COUNTY+TRACT"},
                                )

    fig = fig.update_traces(
        marker_line_width=0.000000001,
        marker_line_color='#D3D3D3',
    )

    fig.update_layout(
        margin={"r": 0, "t": 25, "l": 0, "b": 0},
        title={'xanchor': 'center', 'x': 0.5},
        coloraxis_colorbar={
            'title': 'Estimated Total Population',
            'title_side': 'bottom',
            'tickformat': '.1f',
            'tickvals': [0, 1931, 2493, 2943, 3355, 3754, 4170, 4648, 5244, 6114, 8600],
            'ticktext': ['0%:0', '10%:1931', '20%:2493', '30%:2943', '40%:3355', '50%:3754', '60%:4170', '70%:4648', '80%:5244', '90%:6114', '99%:8600'],
            'orientation': 'h',
            'x': 0.5,
            'xanchor': 'center',
            'y': -0.00000001,
            'yanchor': 'top',
            'len': 0.9,
        },
        annotations=[
            dict(
                text='Source: U.S. Census Bureau 2023 Shapefiles,<br>American Community Survey 2021 5-Yr Estimate Census Tract Level Data',
                xref='paper',
                yref='paper',
                x=0.01,
                y=0.01,
                showarrow=False,
                font=dict(size=10),
                align='left'
            )
        ]
    )

    fig.write_html('YOUR_PATH/Blog_choropleth_map_FINAL.html')
    fig.show()
