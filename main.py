import pandas as pd
from config import (
    TRACT_ZIP_DIR, RAW_CSV_PATH, BLOG_DATA_PATH, PROCESSED_CSV_PATH,
    GEOJSON_OUTPUT_PATH, SIMPLIFIED_JSON_PATH, ACCESS_TOKEN_PATH, CHOROPLETH_HTML_PATH
)
from geojson_utils import convert_to_geojson
from data_processing import process_csv, convert_and_save_csv, print_population_stats
from visualization import generate_choropleth

if __name__ == '__main__':
    geojson_path = convert_to_geojson(TRACT_ZIP_DIR, GEOJSON_OUTPUT_PATH)
    print("GeoJSON saved to:", geojson_path)

    process_csv(RAW_CSV_PATH, BLOG_DATA_PATH, ['GEO_ID', 'S2701_C01_001E'])

    rename_map = {'GEO_ID': 'GEOID', 'S2701_C03_001E': 'Total_Population'}
    dtypes, missing = convert_and_save_csv(BLOG_DATA_PATH, PROCESSED_CSV_PATH, ['GEOID', 'Total_Population'], rename_map)
    print("Data Types:\n", dtypes)
    print("\nMissing Values:\n", missing)

    df = pd.read_csv(PROCESSED_CSV_PATH)
    print_population_stats(df, 'Total_Population')

    generate_choropleth(PROCESSED_CSV_PATH, SIMPLIFIED_JSON_PATH, ACCESS_TOKEN_PATH, CHOROPLETH_HTML_PATH)
    print("Choropleth map saved to:", CHOROPLETH_HTML_PATH)