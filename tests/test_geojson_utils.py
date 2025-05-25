import os
import pytest
import geopandas as gpd
import zipfile
from shapely.geometry import Polygon
from geojson_utils import extract_shapefiles, simplify_geojson, convert_to_geojson


@pytest.fixture
def sample_shapefile(tmp_path):
    """Create a sample shapefile for testing."""
    # Create a simple polygon
    polygon = Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])
    gdf = gpd.GeoDataFrame({"geometry": [polygon], "GEOID": ["01001"]})

    # Save as shapefile
    shp_dir = tmp_path / "shp"
    shp_dir.mkdir()
    shp_path = shp_dir / "test.shp"
    gdf.to_file(shp_path)

    # Create zip file
    zip_dir = tmp_path / "zips"
    zip_dir.mkdir()
    zip_path = zip_dir / "01_tract.zip"

    with zipfile.ZipFile(zip_path, "w") as zipf:
        for ext in [".shp", ".shx", ".dbf", ".prj"]:
            file_path = str(shp_path).replace(".shp", ext)
            if os.path.exists(file_path):
                zipf.write(file_path, os.path.basename(file_path))

    return {"zip_dir": str(zip_dir), "shp_dir": str(shp_dir), "gdf": gdf}


def test_extract_shapefiles(sample_shapefile, tmp_path):
    """Test shapefile extraction from zip files."""
    extract_dir = tmp_path / "extract"
    extract_dir.mkdir()

    extract_shapefiles(sample_shapefile["zip_dir"], str(extract_dir))

    # Verify files were extracted
    assert any(f.endswith(".shp") for f in os.listdir(extract_dir))


def test_simplify_geojson(sample_shapefile, tmp_path):
    """Test GeoJSON simplification."""
    # Create input GeoJSON
    input_path = str(tmp_path / "input.geojson")
    sample_shapefile["gdf"].to_file(input_path, driver="GeoJSON")

    # Test successful simplification
    output_path = str(tmp_path / "simplified.geojson")
    result = simplify_geojson(input_path, output_path)
    assert result == output_path
    assert os.path.exists(output_path)

    # Test with invalid input
    invalid_path = str(tmp_path / "invalid.geojson")
    with open(invalid_path, "w") as f:
        f.write("invalid json")
    result = simplify_geojson(invalid_path, output_path)
    assert result is None


def test_convert_to_geojson(sample_shapefile, tmp_path):
    """Test conversion of shapefiles to GeoJSON."""
    output_path = str(tmp_path / "output.geojson")

    # Test successful conversion
    result = convert_to_geojson(sample_shapefile["shp_dir"], output_path)
    assert result == output_path
    assert os.path.exists(output_path)

    # Test with empty directory
    empty_dir = str(tmp_path / "empty")
    os.makedirs(empty_dir)
    result = convert_to_geojson(empty_dir, output_path)
    assert result is None

    # Test with invalid directory
    result = convert_to_geojson("/nonexistent/dir", output_path)
    assert result is None
