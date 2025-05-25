import subprocess
import os
import pytest
import json
import pandas as pd
import geopandas as gpd
from pathlib import Path
from shapely.geometry import Polygon


@pytest.fixture
def mock_environment(tmp_path):
    """Set up a mock environment for testing."""
    # Create directory structure
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    output_dir = tmp_path / "output"
    output_dir.mkdir()

    # Create mock shapefile
    tract_zip_dir = data_dir / "tractzips"
    tract_zip_dir.mkdir()

    # Create a simple shapefile
    polygon = Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])
    gdf = gpd.GeoDataFrame({"geometry": [polygon]})
    gdf["GEOID"] = ["01001"]
    shp_file = tract_zip_dir / "tract.shp"
    gdf.to_file(shp_file)

    # Create mock ACS data
    acs_data = pd.DataFrame(
        {
            "GEO_ID": ["1400000US01001", "1400000US01002"],
            "S2701_C01_001E": ["1000", "2000"],
        }
    )
    acs_file = data_dir / "ACSST5Y2021.S2701-Data.csv"
    acs_data.to_csv(acs_file, index=False)

    # Create mock Mapbox token
    token_file = config_dir / "accesstoken.txt"
    token_file.write_text("mock_token")

    # Create mock config.py
    config_content = f"""
import os

TRACT_ZIP_DIR = "{tract_zip_dir}"
RAW_CSV_PATH = "{acs_file}"
PROCESSED_CSV_PATH = "{output_dir}/Blog_Data.csv"
GEOJSON_OUTPUT_PATH = "{output_dir}/tracts1.geojson"
SIMPLIFIED_JSON_PATH = "{output_dir}/blog_tracts_zip.json"
ACCESS_TOKEN_PATH = "{token_file}"
CHOROPLETH_HTML_PATH = "{output_dir}/Blog_choropleth_map_FINAL.html"
"""
    config_file = Path("config.py")
    config_file.write_text(config_content)

    return tmp_path


def test_pipeline_runs(mock_environment):
    """Test that the main pipeline runs without errors."""
    try:
        result = subprocess.run(
            ["python", "main.py"],
            check=False,
            capture_output=True,
            text=True,
            env={**os.environ, "PYTHONPATH": "."},
        )

        # Print output for debugging in CI
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)

        assert result.returncode == 0, f"Pipeline failed with: {result.stderr}"

        # Check that output files were created
        output_dir = mock_environment / "output"
        expected_files = [
            "Blog_Data.csv",
            "tracts1.geojson",
            "blog_tracts_zip.json",
            "Blog_choropleth_map_FINAL.html",
        ]

        for file in expected_files:
            assert (
                output_dir / file
            ).exists(), f"Expected output file {file} not found"

    finally:
        # Clean up temporary config file
        if Path("config.py").exists():
            Path("config.py").unlink()


def test_pipeline_error_handling(mock_environment):
    """Test pipeline error handling with invalid input."""
    # Corrupt the ACS data file
    acs_file = mock_environment / "data" / "ACSST5Y2021.S2701-Data.csv"
    acs_file.write_text("invalid,csv,data")

    result = subprocess.run(
        ["python", "main.py"],
        check=False,
        capture_output=True,
        text=True,
        env={**os.environ, "PYTHONPATH": "."},
    )

    assert result.returncode != 0, "Pipeline should fail with invalid input"
