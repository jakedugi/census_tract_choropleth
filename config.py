import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(BASE_DIR, 'data')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')
CONFIG_DIR = os.path.join(BASE_DIR, 'config')

TRACT_ZIP_DIR = os.path.join(DATA_DIR, 'tractzips')
RAW_CSV_PATH = os.path.join(DATA_DIR, 'ACSST5Y2021.S2701-Data.csv')
BLOG_DATA_PATH = os.path.join(OUTPUT_DIR, 'Blog_Data.csv')
PROCESSED_CSV_PATH = os.path.join(OUTPUT_DIR, 'Blog_Data_Processed.csv')
GEOJSON_OUTPUT_PATH = os.path.join(OUTPUT_DIR, 'tracts1.geojson')
SIMPLIFIED_JSON_PATH = os.path.join(OUTPUT_DIR, 'blog_tracts_zip.json')
ACCESS_TOKEN_PATH = os.path.join(CONFIG_DIR, 'accesstoken.txt')
CHOROPLETH_HTML_PATH = os.path.join(OUTPUT_DIR, 'Blog_choropleth_map_FINAL.html')
