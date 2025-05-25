import pytest
import os
import json
import pandas as pd
import shutil
from pathlib import Path
from main import main


@pytest.fixture
def mock_environment(tmp_path, monkeypatch):
    """Set up a mock environment for testing main.py."""
    # Create directory structure
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    output_dir = tmp_path / "output"
    output_dir.mkdir()

    # Copy the pre-simplified GeoJSON to the test environment
    src_geojson = Path("data/blog_tracts_zip.json")
    if not src_geojson.exists():
        raise FileNotFoundError(
            "Pre-simplified GeoJSON not found. Please ensure data/blog_tracts_zip.json exists."
        )

    dst_geojson = output_dir / "blog_tracts_zip.json"
    shutil.copy(src_geojson, dst_geojson)

    # Create sample ACS data with correct column names
    acs_data = pd.DataFrame(
        {
            "GEO_ID": ["1400000US01001", "1400000US01002"],
            "NAME": ["Tract 1", "Tract 2"],
            "S2701_C01_001E": ["1000", "2000"],
        }
    )
    acs_file = data_dir / "ACSST5Y2021.S2701-Data.csv"
    acs_data.to_csv(acs_file, index=False)

    # Create Mapbox token
    token_file = config_dir / "accesstoken.txt"
    token_file.write_text("mock_token")

    # Create test configuration
    config = {
        "output_dir": str(output_dir),
        "acs_file": str(acs_file),
        "token_file": str(token_file),
        "simplified_json": str(dst_geojson),
    }
    config_file = config_dir / "test_config.json"
    with open(config_file, "w") as f:
        json.dump(config, f)

    # Set environment variable for test configuration
    monkeypatch.setenv("CENSUS_CONFIG", str(config_file))

    return {
        "data_dir": data_dir,
        "config_dir": config_dir,
        "output_dir": output_dir,
        "acs_file": acs_file,
        "token_file": token_file,
        "config_file": config_file,
        "simplified_json": dst_geojson,
    }


@pytest.fixture(autouse=True)
def cleanup():
    """Clean up any files created during tests."""
    yield
    # Restore original config.py after tests
    with open("config.py", "w") as f:
        f.write(
            """import os
from pathlib import Path

# Base directories
DATA_DIR = Path("data")
OUTPUT_DIR = Path("output")
CONFIG_DIR = Path("config")

# Input paths
RAW_CSV_PATH = str(DATA_DIR / "ACSST5Y2021.S2701-Data.csv")
ACCESS_TOKEN_PATH = str(CONFIG_DIR / "accesstoken.txt")

# Output paths
PROCESSED_CSV_PATH = str(OUTPUT_DIR / "Blog_Data.csv")
SIMPLIFIED_JSON_PATH = str(OUTPUT_DIR / "blog_tracts_zip.json")
CHOROPLETH_HTML_PATH = str(OUTPUT_DIR / "Blog_choropleth_map_FINAL.html")
"""
        )


def test_main_success(mock_environment):
    """Test successful execution of main function."""
    try:
        main()

        # Verify output files were created
        output_dir = mock_environment["output_dir"]
        expected_files = ["Blog_Data.csv", "Blog_choropleth_map_FINAL.html"]

        for file in expected_files:
            assert os.path.exists(output_dir / file)

    except Exception as e:
        pytest.fail(f"Main function failed: {str(e)}")


def test_main_invalid_acs_data(mock_environment):
    """Test main function with invalid ACS data."""
    # Corrupt the ACS data file
    with open(mock_environment["acs_file"], "w") as f:
        f.write("invalid,csv,data\n")

    with pytest.raises(SystemExit):
        main()


def test_main_invalid_token(mock_environment):
    """Test main function with invalid Mapbox token."""
    # Remove token file
    os.remove(mock_environment["token_file"])

    with pytest.raises(SystemExit):
        main()
