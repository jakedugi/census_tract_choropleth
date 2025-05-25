import pytest
import pandas as pd
import json
from pathlib import Path
from visualization import generate_choropleth


@pytest.fixture
def sample_data():
    """Create sample data for testing."""
    return pd.DataFrame({"GEOID": ["01001", "01002"], "Total_Population": [1000, 2000]})


@pytest.fixture
def sample_geojson():
    """Create sample GeoJSON for testing."""
    return {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {"GEOID": "01001"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]],
                },
            },
            {
                "type": "Feature",
                "properties": {"GEOID": "01002"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[[1, 1], [2, 1], [2, 2], [1, 2], [1, 1]]],
                },
            },
        ],
    }


def test_generate_choropleth(tmp_path, sample_data, sample_geojson):
    """Test choropleth map generation."""
    # Create necessary files
    csv_file = tmp_path / "data.csv"
    json_file = tmp_path / "tracts.json"
    token_file = tmp_path / "token.txt"
    output_file = tmp_path / "map.html"

    # Write test data
    sample_data.to_csv(csv_file, index=False)
    with open(json_file, "w") as f:
        json.dump(sample_geojson, f)
    with open(token_file, "w") as f:
        f.write("mock_token")

    # Generate choropleth
    fig = generate_choropleth(csv_file, json_file, token_file, output_file)

    # Verify output
    assert fig is not None
    assert output_file.exists()
    assert output_file.stat().st_size > 0


def test_generate_choropleth_invalid_geojson(tmp_path, sample_data):
    """Test error handling with invalid GeoJSON."""
    csv_file = tmp_path / "data.csv"
    json_file = tmp_path / "invalid.json"
    token_file = tmp_path / "token.txt"
    output_file = tmp_path / "map.html"

    # Write test data
    sample_data.to_csv(csv_file, index=False)
    with open(json_file, "w") as f:
        json.dump({"type": "FeatureCollection"}, f)  # Missing features
    with open(token_file, "w") as f:
        f.write("mock_token")

    with pytest.raises(ValueError, match="Invalid GeoJSON structure"):
        generate_choropleth(csv_file, json_file, token_file, output_file)


def test_generate_choropleth_missing_geoid(tmp_path, sample_geojson):
    """Test error handling with missing GEOID column."""
    csv_file = tmp_path / "data.csv"
    json_file = tmp_path / "tracts.json"
    token_file = tmp_path / "token.txt"
    output_file = tmp_path / "map.html"

    # Create data without GEOID
    bad_data = pd.DataFrame({"Population": [1000, 2000]})

    # Write test data
    bad_data.to_csv(csv_file, index=False)
    with open(json_file, "w") as f:
        json.dump(sample_geojson, f)
    with open(token_file, "w") as f:
        f.write("mock_token")

    with pytest.raises(ValueError, match="must contain a 'GEOID' column"):
        generate_choropleth(csv_file, json_file, token_file, output_file)
