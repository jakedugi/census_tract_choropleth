import sys
import pandas as pd
from config import (
    TRACT_ZIP_DIR, RAW_CSV_PATH, PROCESSED_CSV_PATH,
    GEOJSON_OUTPUT_PATH, SIMPLIFIED_JSON_PATH, ACCESS_TOKEN_PATH, CHOROPLETH_HTML_PATH
)
from data_processing import process_acs_csv, print_population_stats
from geojson_utils import convert_to_geojson, simplify_geojson
from visualization import generate_choropleth

# ACS Column Documentation:
# S2701_C01_001E breakdown:
# - S2701: Table number (Selected Characteristics of Health Insurance Coverage)
# - C01: Column number (first column)
# - 001: Row number (total population)
# - E: Estimate (vs M for margin of error)

def main():
    # Process ACS data with explicit column mapping
    column_mapping = {
        'S2701_C01_001E': 'Total_Population'  # Map ACS column code to readable name
    }
    
    try:
        dtypes, missing = process_acs_csv(RAW_CSV_PATH, PROCESSED_CSV_PATH, column_mapping)
        print("Data Types:\n", dtypes)
        print("\nMissing Values:\n", missing)
    except Exception as e:
        print(f"Error processing ACS data: {e}")
        sys.exit(1)

    # Convert shapefiles → GeoJSON
    geojson = convert_to_geojson(TRACT_ZIP_DIR, GEOJSON_OUTPUT_PATH)
    if not geojson:
        # print already done inside convert_to_geojson
        sys.exit(1)

    # Simplify GeoJSON for visualization
    simplified = simplify_geojson(GEOJSON_OUTPUT_PATH, SIMPLIFIED_JSON_PATH)
    if not simplified:
        print("Failed to simplify GeoJSON")
        sys.exit(1)

    # Create visualization
    try:
        generate_choropleth(PROCESSED_CSV_PATH, SIMPLIFIED_JSON_PATH, 
                          ACCESS_TOKEN_PATH, CHOROPLETH_HTML_PATH)
        print("Choropleth map saved to:", CHOROPLETH_HTML_PATH)
    except Exception as e:
        print(f"Error generating choropleth: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()