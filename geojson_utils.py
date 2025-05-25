import os
import geopandas as gpd
import pandas as pd
import zipfile
import tempfile
import shutil

def extract_shapefiles(zip_directory, temp_dir):
    """Extract all shapefile zip archives to a temporary directory."""
    for filename in os.listdir(zip_directory):
        if filename.endswith('_tract.zip'):
            zip_path = os.path.join(zip_directory, filename)
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)

def simplify_geojson(input_path, output_path, tolerance=0.01):
    """Simplify a GeoJSON file while preserving topology."""
    try:
        # Read the input GeoJSON
        gdf = gpd.read_file(input_path)
        
        # Simplify geometries
        gdf.geometry = gdf.geometry.simplify(tolerance, preserve_topology=True)
        
        # Write simplified GeoJSON
        gdf.to_file(output_path, driver='GeoJSON')
        return output_path
    except Exception:
        return None

def convert_to_geojson(shp_dir, output_geojson_path):
    # If it's a directory, look inside; otherwise
    # you might have code to unzip first (not shown here)
    if not os.path.isdir(shp_dir):
        print("No shapefiles found after extraction")
        return None

    # Find any .shp file
    candidates = [
        os.path.join(shp_dir, f)
        for f in os.listdir(shp_dir)
        if f.lower().endswith('.shp')
    ]
    if not candidates:
        print("No shapefiles found after extraction")
        return None

    shp_path = candidates[0]
    try:
        gdf = gpd.read_file(shp_path)
        gdf.to_file(output_geojson_path, driver='GeoJSON')
        return output_geojson_path
    except Exception:
        print("Failed to create GeoJSON file")
        return None