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

def simplify_geojson(input_path, output_path, tolerance=0.001):
    """
    Simplify a GeoJSON file to reduce its size while maintaining topology.
    
    Args:
        input_path: Path to input GeoJSON file
        output_path: Path to save simplified GeoJSON
        tolerance: Simplification tolerance (higher = more simplification)
    
    Returns:
        str: Path to simplified GeoJSON file
    """
    try:
        # Read the GeoJSON
        gdf = gpd.read_file(input_path)
        
        # Simplify geometries
        gdf['geometry'] = gdf['geometry'].simplify(tolerance=tolerance, preserve_topology=True)
        
        # Save simplified GeoJSON
        gdf.to_file(output_path, driver='GeoJSON')
        
        print(f"Simplified GeoJSON saved to {output_path}")
        print(f"Original size: {os.path.getsize(input_path) / 1024 / 1024:.1f}MB")
        print(f"Simplified size: {os.path.getsize(output_path) / 1024 / 1024:.1f}MB")
        
        return output_path
    
    except Exception as e:
        print(f"Error simplifying GeoJSON: {str(e)}")
        return None

def convert_to_geojson(directory, output_path):
    """
    Convert Census Tract shapefiles to GeoJSON format.
    
    Args:
        directory: Directory containing zipped tract shapefiles
        output_path: Path to save the combined GeoJSON file
    
    Returns:
        str: Path to the created GeoJSON file, or None if failed
    """
    try:
        # Create a temporary directory for extracted files
        with tempfile.TemporaryDirectory() as temp_dir:
            # Extract all zip files
            extract_shapefiles(directory, temp_dir)
            
            # Find all extracted shapefiles
            shp_files = [f for f in os.listdir(temp_dir) if f.endswith('.shp')]
            
            if not shp_files:
                print("No shapefiles found after extraction")
                return None
            
            # Process each shapefile
            gdf_list = []
            for shp_file in shp_files:
                shp_path = os.path.join(temp_dir, shp_file)
                try:
                    gdf = gpd.read_file(shp_path)
                    
                    # Ensure GEOID column exists and is properly formatted
                    if 'GEOID' not in gdf.columns and 'GEOID20' in gdf.columns:
                        gdf['GEOID'] = gdf['GEOID20']
                    elif 'GEOID' not in gdf.columns and 'TRACTCE20' in gdf.columns:
                        # Construct GEOID from state and tract codes if needed
                        gdf['GEOID'] = gdf['STATEFP20'] + gdf['COUNTYFP20'] + gdf['TRACTCE20']
                    
                    # Keep only necessary columns
                    gdf = gdf[['GEOID', 'geometry']]
                    
                    # Fix any invalid geometries
                    gdf['geometry'] = gdf['geometry'].apply(lambda geom: geom.buffer(0) if not geom.is_valid else geom)
                    gdf_list.append(gdf)
                    
                except Exception as e:
                    print(f"Error processing {shp_path}: {e}")
            
            if not gdf_list:
                print("No valid shapefiles could be processed")
                return None
            
            # Combine all GeoDataFrames
            combined_gdf = gpd.GeoDataFrame(pd.concat(gdf_list, ignore_index=True))
            
            # Ensure GEOID is string type for proper matching
            combined_gdf['GEOID'] = combined_gdf['GEOID'].astype(str)
            
            # Create output directory if it doesn't exist
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Save to GeoJSON
            combined_gdf.to_file(output_path, driver="GeoJSON")
            print(f"Successfully created GeoJSON with {len(combined_gdf)} features")
            return output_path
            
    except Exception as e:
        print(f"Error in convert_to_geojson: {str(e)}")
        return None