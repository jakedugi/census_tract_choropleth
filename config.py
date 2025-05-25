import os
from pathlib import Path

# Base directories
DATA_DIR = Path("data")
OUTPUT_DIR = Path("output")
CONFIG_DIR = Path("config")

# Input paths
TRACT_ZIP_DIR = str(DATA_DIR / "tractzips")
RAW_CSV_PATH = str(DATA_DIR / "ACSST5Y2021.S2701-Data.csv")
ACCESS_TOKEN_PATH = str(CONFIG_DIR / "accesstoken.txt")

# Output paths
PROCESSED_CSV_PATH = str(OUTPUT_DIR / "Blog_Data.csv")
GEOJSON_OUTPUT_PATH = str(OUTPUT_DIR / "tracts1.geojson")
SIMPLIFIED_JSON_PATH = str(OUTPUT_DIR / "blog_tracts_zip.json")
CHOROPLETH_HTML_PATH = str(OUTPUT_DIR / "Blog_choropleth_map_FINAL.html")
