import pandas as pd
from config import (
    TRACT_ZIP_DIR, RAW_CSV_PATH, PROCESSED_CSV_PATH,
    GEOJSON_OUTPUT_PATH, SIMPLIFIED_JSON_PATH, ACCESS_TOKEN_PATH, CHOROPLETH_HTML_PATH
)
from geojson_utils import convert_to_geojson, simplify_geojson
from data_processing import process_acs_csv, print_population_stats
from visualization import generate_choropleth

# ACS Column Documentation:
# S2701_C01_001E breakdown:
# - S2701: Table number (Selected Characteristics of Health Insurance Coverage)
# - C01: Column number (first column)
# - 001: Row number (total population)
# - E: Estimate (vs M for margin of error)

if __name__ == '__main__':
    # Convert shapefiles to GeoJSON
    geojson_path = convert_to_geojson(TRACT_ZIP_DIR, GEOJSON_OUTPUT_PATH)
    if not geojson_path:
        print("Failed to create GeoJSON file")
        exit(1)
    
    # Simplify GeoJSON for visualization
    simplified_path = simplify_geojson(GEOJSON_OUTPUT_PATH, SIMPLIFIED_JSON_PATH)
    if not simplified_path:
        print("Failed to simplify GeoJSON file")
        exit(1)
    
    print("GeoJSON processing complete")

    # Process ACS data with explicit column mapping
    column_mapping = {
        'S2701_C01_001E': 'Total_Population'  # Map ACS column code to readable name
    }
    
    dtypes, missing = process_acs_csv(RAW_CSV_PATH, PROCESSED_CSV_PATH, column_mapping)
    print("Data Types:\n", dtypes)
    print("\nMissing Values:\n", missing)

    # Generate statistics
    df = pd.read_csv(PROCESSED_CSV_PATH)
    print_population_stats(df, 'Total_Population')

    # Create visualization using simplified GeoJSON
    generate_choropleth(PROCESSED_CSV_PATH, SIMPLIFIED_JSON_PATH, ACCESS_TOKEN_PATH, CHOROPLETH_HTML_PATH)
    print("Choropleth map saved to:", CHOROPLETH_HTML_PATH)