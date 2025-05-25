import os
import geopandas as gpd
import pandas as pd


def convert_to_geojson(directory, output_path):
    """
    Convert shapefiles in a directory to a single GeoJSON file.

    Args:
        directory (str): Directory containing shapefiles
        output_path (str): Path to save the output GeoJSON file

    Returns:
        str: Path to the output file if successful, None otherwise
    """
    if not os.path.isdir(directory):
        print(f"Directory not found: {directory}")
        return None

    shp_files = [file for file in os.listdir(directory) if file.endswith(".shp")]
    if not shp_files:
        print("No shapefiles found in directory")
        return None

    try:
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

        if not gdf_list:
            print("No valid shapefiles could be read")
            return None

        combined_gdf = gpd.GeoDataFrame(pd.concat(gdf_list, ignore_index=True))
        combined_gdf.to_file(output_path, driver="GeoJSON")
        return output_path

    except Exception as e:
        print(f"Error converting to GeoJSON: {e}")
        return None


def process_csv(input_file, output_file, columns_to_keep):
    """
    Process a CSV file by selecting specific columns and handling data types.

    Args:
        input_file (str): Path to input CSV file
        output_file (str): Path to save the processed CSV file
        columns_to_keep (list): List of column names to keep
    """
    try:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(input_file)

        # Remove the second row (header descriptions)
        df = df.drop(0)

        # Keep only the specified columns
        df = df[columns_to_keep]

        # Save the processed DataFrame to a new CSV file
        df.to_csv(output_file, index=False)
        print(f"Processed CSV saved to {output_file}")

    except Exception as e:
        print(f"Error processing CSV: {e}")
        raise
