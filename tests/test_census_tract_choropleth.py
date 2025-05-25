import os
import pytest
import pandas as pd
import geopandas as gpd
from shapely.geometry import Polygon
from census_tract_choropleth import convert_to_geojson, process_csv


@pytest.fixture
def sample_shapefile(tmp_path):
    """Create a sample shapefile for testing."""
    shp_dir = tmp_path / "shapefiles"
    shp_dir.mkdir()
    
    # Create a simple polygon
    polygon = Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])
    gdf = gpd.GeoDataFrame({
        'geometry': [polygon],
        'GEOID': ['01001']
    })
    
    # Save as shapefile
    shp_path = shp_dir / "test.shp"
    gdf.to_file(shp_path)
    
    return str(shp_dir)


@pytest.fixture
def sample_csv(tmp_path):
    """Create a sample CSV file for testing."""
    # Create DataFrame with header row and data row
    df = pd.DataFrame({
        'GEO_ID': ['Header Description', '1400000US01001', '1400000US01002'],
        'S2701_C03_001E': ['Population Estimate', '1000', '2000'],
        'Extra_Column': ['Extra Info', 'a', 'b']
    })
    
    csv_path = tmp_path / "test.csv"
    df.to_csv(csv_path, index=False)
    return str(csv_path)


def test_convert_to_geojson(sample_shapefile, tmp_path):
    """Test converting shapefiles to GeoJSON."""
    output_path = str(tmp_path / "output.geojson")
    
    # Test successful conversion
    result = convert_to_geojson(sample_shapefile, output_path)
    assert result == output_path
    assert os.path.exists(output_path)
    
    # Test with empty directory
    empty_dir = str(tmp_path / "empty")
    os.makedirs(empty_dir)
    result = convert_to_geojson(empty_dir, output_path)
    assert result is None


def test_process_csv(sample_csv, tmp_path):
    """Test CSV processing functionality."""
    output_path = str(tmp_path / "processed.csv")
    columns_to_keep = ['GEO_ID', 'S2701_C03_001E']
    
    # Test successful processing
    process_csv(sample_csv, output_path, columns_to_keep)
    assert os.path.exists(output_path)
    
    # Verify output
    df = pd.read_csv(output_path)
    assert list(df.columns) == columns_to_keep
    assert len(df) == 2  # Should have 2 data rows after dropping header row
    
    # Test with invalid columns
    with pytest.raises(KeyError):
        process_csv(sample_csv, output_path, ['NonExistentColumn']) 