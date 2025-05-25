import os
import sys
import json
from pathlib import Path
import pandas as pd
from config import (
    RAW_CSV_PATH,
    PROCESSED_CSV_PATH,
    SIMPLIFIED_JSON_PATH,
    ACCESS_TOKEN_PATH,
    CHOROPLETH_HTML_PATH,
)
from data_processing import process_acs_csv
from visualization import generate_choropleth

# ACS Column Documentation:
# S2701_C01_001E breakdown:
# - S2701: Table number (Selected Characteristics of Health Insurance Coverage)
# - C01: Column number (first column)
# - 001: Row number (total population)
# - E: Estimate (vs M for margin of error)


def main():
    # Override paths with test configuration if provided
    config_path = os.getenv("CENSUS_CONFIG")
    if config_path:
        try:
            with open(config_path) as cf:
                cfg = json.load(cf)
            # Update paths from config
            global RAW_CSV_PATH, PROCESSED_CSV_PATH
            global SIMPLIFIED_JSON_PATH, ACCESS_TOKEN_PATH, CHOROPLETH_HTML_PATH

            output_dir = Path(cfg.get("output_dir"))
            RAW_CSV_PATH = str(cfg.get("acs_file", RAW_CSV_PATH))
            PROCESSED_CSV_PATH = str(output_dir / "Blog_Data.csv")
            SIMPLIFIED_JSON_PATH = str(cfg.get("simplified_json", SIMPLIFIED_JSON_PATH))
            ACCESS_TOKEN_PATH = str(cfg.get("token_file", ACCESS_TOKEN_PATH))
            CHOROPLETH_HTML_PATH = str(output_dir / "Blog_choropleth_map_FINAL.html")
        except Exception as e:
            print(f"Error loading config file: {e}")
            sys.exit(1)

    # Process ACS data with explicit column mapping
    column_mapping = {
        "S2701_C01_001E": "Total_Population"  # Map ACS column code to readable name
    }

    try:
        dtypes, missing = process_acs_csv(
            RAW_CSV_PATH, PROCESSED_CSV_PATH, column_mapping
        )
        print("Data Types:\n", dtypes)
        print("\nMissing Values:\n", missing)
    except Exception as e:
        print(f"Error processing ACS data: {e}")
        sys.exit(1)

    # Create visualization
    try:
        generate_choropleth(
            PROCESSED_CSV_PATH,
            SIMPLIFIED_JSON_PATH,
            ACCESS_TOKEN_PATH,
            CHOROPLETH_HTML_PATH,
        )
        print("Choropleth map saved to:", CHOROPLETH_HTML_PATH)
    except Exception as e:
        print(f"Error generating choropleth: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
