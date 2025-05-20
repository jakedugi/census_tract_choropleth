from geojson_utils import convert_to_geojson
from data_processing import process_csv, convert_and_save_csv, print_population_stats
from visualization import generate_choropleth

if __name__ == '__main__':
    # GeoJSON conversion
    geojson_path = convert_to_geojson('data/tractzips/', 'output/tracts1.geojson')
    print("GeoJSON saved to:", geojson_path)

    # CSV Processing
    process_csv('data/ACSST5Y2021.S2701-Data.csv', 'output/Blog_Data.csv', ['GEO_ID', 'S2701_C01_001E'])

    # Column transformation and data inspection
    input_csv = 'output/Blog_Data.csv'
    output_csv = 'output/Blog_Data_Processed.csv'
    rename_map = {'GEO_ID': 'GEOID', 'S2701_C03_001E': 'Total_Population'}
    dtypes, missing = convert_and_save_csv(input_csv, output_csv, ['GEOID', 'Total_Population'], rename_map)
    print("Data Types:\n", dtypes)
    print("\nMissing Values:\n", missing)

    # Summary Stats
    df = pd.read_csv(output_csv)
    print_population_stats(df, 'Total_Population')

    # Generate visualization
    generate_choropleth(
        csv_file=output_csv,
        json_file='output/blog_tracts_zip.json',
        token_file='config/accesstoken.txt',
        output_html='output/Blog_choropleth_map_FINAL.html'
    )
