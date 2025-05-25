import os
from pathlib import Path

# Base directories
DATA_DIR = Path(
    "/private/var/folders/w7/6rbmdvg163x5kscfm1zh1t8h0000gn/T/pytest-of-jakedugan/pytest-25/test_pipeline_error_handling0/data"
)
OUTPUT_DIR = Path(
    "/private/var/folders/w7/6rbmdvg163x5kscfm1zh1t8h0000gn/T/pytest-of-jakedugan/pytest-25/test_pipeline_error_handling0/output"
)
CONFIG_DIR = Path(
    "/private/var/folders/w7/6rbmdvg163x5kscfm1zh1t8h0000gn/T/pytest-of-jakedugan/pytest-25/test_pipeline_error_handling0/config"
)

# Input paths
RAW_CSV_PATH = str(DATA_DIR / "ACSST5Y2021.S2701-Data.csv")
ACCESS_TOKEN_PATH = str(CONFIG_DIR / "accesstoken.txt")

# Output paths
PROCESSED_CSV_PATH = str(OUTPUT_DIR / "Blog_Data.csv")
SIMPLIFIED_JSON_PATH = str(OUTPUT_DIR / "blog_tracts_zip.json")
CHOROPLETH_HTML_PATH = str(OUTPUT_DIR / "Blog_choropleth_map_FINAL.html")
