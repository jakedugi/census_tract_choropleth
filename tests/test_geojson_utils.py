import pytest
import geopandas as gpd
from shapely.geometry import Polygon
import json
from pathlib import Path
from geojson_utils import simplify_geojson, convert_to_geojson


@pytest.fixture
def sample_geojson(tmp_path):
    """Create a sample GeoJSON file for testing."""
    # Create a simple GeoDataFrame
    polygon = Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])
    gdf = gpd.GeoDataFrame({"geometry": [polygon]})
    gdf["GEOID"] = ["01001"]  # Add GEOID for identification

    # Save as GeoJSON
    input_file = tmp_path / "input.geojson"
    gdf.to_file(input_file, driver="GeoJSON")
    return input_file


def test_simplify_geojson(tmp_path, sample_geojson):
    """Test GeoJSON simplification function."""
    output_file = tmp_path / "simplified.geojson"

    # Test simplification
    result = simplify_geojson(str(sample_geojson), str(output_file))
    assert result == str(output_file)
    assert output_file.exists()

    # Verify simplified GeoJSON structure
    with open(output_file) as f:
        simplified = json.load(f)
    assert "type" in simplified
    assert "features" in simplified
    assert len(simplified["features"]) > 0


def test_convert_to_geojson(tmp_path):
    """Test shapefile to GeoJSON conversion."""
    # Create a mock shapefile directory
    shp_dir = tmp_path / "shapefiles"
    shp_dir.mkdir()

    # Create a simple shapefile
    polygon = Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])
    gdf = gpd.GeoDataFrame({"geometry": [polygon]})
    gdf["GEOID"] = ["01001"]
    shp_file = shp_dir / "tract.shp"
    gdf.to_file(shp_file)

    # Test conversion
    output_file = tmp_path / "output.geojson"
    result = convert_to_geojson(str(shp_dir), str(output_file))

    assert result == str(output_file)
    assert Path(result).exists()

    # Verify GeoJSON structure
    with open(result) as f:
        geojson = json.load(f)
    assert "type" in geojson
    assert "features" in geojson
    assert len(geojson["features"]) > 0


def test_simplify_geojson_invalid_input(tmp_path):
    """Test error handling for invalid GeoJSON input."""
    input_file = tmp_path / "invalid.geojson"
    output_file = tmp_path / "output.geojson"

    # Create invalid GeoJSON
    with open(input_file, "w") as f:
        json.dump({"type": "Invalid"}, f)

    result = simplify_geojson(str(input_file), str(output_file))
    assert result is None  # Should return None for invalid input
