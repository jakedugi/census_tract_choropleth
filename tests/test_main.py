import pytest
import os
import pandas as pd
import geopandas as gpd
from shapely.geometry import Polygon
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
    tractzips_dir = data_dir / "tractzips"
    tractzips_dir.mkdir()

    # Create sample shapefile
    polygon = Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])
    gdf = gpd.GeoDataFrame({
        'geometry': [polygon],
        'GEOID': ['01001']
    })
    shp_path = tractzips_dir / "test.shp"
    gdf.to_file(shp_path)

    # Create sample ACS data with correct column names
    acs_data = pd.DataFrame({
        'GEO_ID': ['1400000US01001', '1400000US01002'],
        'NAME': ['Tract 1', 'Tract 2'],
        'S2701_C01_001E': ['1000', '2000']
    })
    acs_file = data_dir / "ACSST5Y2021.S2701-Data.csv"
    acs_data.to_csv(acs_file, index=False)

    # Create Mapbox token
    token_file = config_dir / "accesstoken.txt"
    token_file.write_text("mock_token")

    # Update config.py with test paths
    config_content = f"""
import os

TRACT_ZIP_DIR = "{str(tractzips_dir)}"
RAW_CSV_PATH = "{str(acs_file)}"
PROCESSED_CSV_PATH = "{str(output_dir / 'Blog_Data.csv')}"
GEOJSON_OUTPUT_PATH = "{str(output_dir / 'tracts1.geojson')}"
SIMPLIFIED_JSON_PATH = "{str(output_dir / 'blog_tracts_zip.json')}"
ACCESS_TOKEN_PATH = "{str(token_file)}"
CHOROPLETH_HTML_PATH = "{str(output_dir / 'Blog_choropleth_map_FINAL.html')}"
"""
    with open("config.py", "w") as f:
        f.write(config_content)

    return {
        'data_dir': data_dir,
        'config_dir': config_dir,
        'output_dir': output_dir,
        'tractzips_dir': tractzips_dir,
        'acs_file': acs_file,
        'token_file': token_file
    }


@pytest.fixture(autouse=True)
def cleanup():
    """Clean up any files created during tests."""
    yield
    # Restore original config.py after tests
    with open("config.py", "w") as f:
        f.write("""import os

TRACT_ZIP_DIR = "/private/var/folders/w7/6rbmdvg163x5kscfm1zh1t8h0000gn/T/pytest-of-jakedugan/pytest-15/test_pipeline_error_handling0/data/tractzips"
RAW_CSV_PATH = "/private/var/folders/w7/6rbmdvg163x5kscfm1zh1t8h0000gn/T/pytest-of-jakedugan/pytest-15/test_pipeline_error_handling0/data/ACSST5Y2021.S2701-Data.csv"
PROCESSED_CSV_PATH = "/private/var/folders/w7/6rbmdvg163x5kscfm1zh1t8h0000gn/T/pytest-of-jakedugan/pytest-15/test_pipeline_error_handling0/output/Blog_Data.csv"
GEOJSON_OUTPUT_PATH = "/private/var/folders/w7/6rbmdvg163x5kscfm1zh1t8h0000gn/T/pytest-of-jakedugan/pytest-15/test_pipeline_error_handling0/output/tracts1.geojson"
SIMPLIFIED_JSON_PATH = "/private/var/folders/w7/6rbmdvg163x5kscfm1zh1t8h0000gn/T/pytest-of-jakedugan/pytest-15/test_pipeline_error_handling0/output/blog_tracts_zip.json"
ACCESS_TOKEN_PATH = "/private/var/folders/w7/6rbmdvg163x5kscfm1zh1t8h0000gn/T/pytest-of-jakedugan/pytest-15/test_pipeline_error_handling0/config/accesstoken.txt"
CHOROPLETH_HTML_PATH = "/private/var/folders/w7/6rbmdvg163x5kscfm1zh1t8h0000gn/T/pytest-of-jakedugan/pytest-15/test_pipeline_error_handling0/output/Blog_choropleth_map_FINAL.html"
""")


def test_main_success(mock_environment):
    """Test successful execution of main function."""
    try:
        main()
        
        # Verify output files were created
        output_dir = mock_environment['output_dir']
        expected_files = [
            "Blog_Data.csv",
            "tracts1.geojson",
            "blog_tracts_zip.json",
            "Blog_choropleth_map_FINAL.html"
        ]
        
        for file in expected_files:
            assert os.path.exists(output_dir / file)
            
    except Exception as e:
        pytest.fail(f"Main function failed: {str(e)}")


def test_main_invalid_acs_data(mock_environment):
    """Test main function with invalid ACS data."""
    # Corrupt the ACS data file
    with open(mock_environment['acs_file'], 'w') as f:
        f.write("invalid,csv,data\n")
    
    with pytest.raises(SystemExit):
        main()


def test_main_missing_shapefile(mock_environment):
    """Test main function with missing shapefile."""
    # Remove all files from tractzips directory
    for file in os.listdir(mock_environment['tractzips_dir']):
        os.remove(os.path.join(mock_environment['tractzips_dir'], file))
    
    with pytest.raises(SystemExit):
        main()


def test_main_invalid_token(mock_environment):
    """Test main function with invalid Mapbox token."""
    # Remove token file
    os.remove(mock_environment['token_file'])
    
    with pytest.raises(SystemExit):
        main() 