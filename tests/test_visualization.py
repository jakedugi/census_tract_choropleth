import pytest
import pandas as pd
import json
import os
from visualization import generate_choropleth


@pytest.fixture
def sample_data(tmp_path):
    """Create sample data files for testing."""
    # Create CSV data
    df = pd.DataFrame({"GEOID": ["01001", "01002"], "Total_Population": [1000, 2000]})
    csv_path = tmp_path / "test.csv"
    df.to_csv(csv_path, index=False)

    # Create GeoJSON data
    geojson = {
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
    json_path = tmp_path / "test.json"
    with open(json_path, "w") as f:
        json.dump(geojson, f)

    # Create token file
    token_path = tmp_path / "token.txt"
    token_path.write_text("dummy_token")

    return {
        "csv_path": str(csv_path),
        "json_path": str(json_path),
        "token_path": str(token_path),
    }


def test_generate_choropleth_success(sample_data, tmp_path):
    """Test successful choropleth generation."""
    output_path = str(tmp_path / "output.html")

    fig = generate_choropleth(
        sample_data["csv_path"],
        sample_data["json_path"],
        sample_data["token_path"],
        output_path,
    )

    assert os.path.exists(output_path)
    assert fig is not None


def test_generate_choropleth_missing_geoid(sample_data, tmp_path):
    """Test choropleth generation with missing GEOID column."""
    # Create CSV without GEOID
    df = pd.DataFrame({"Population": [1000, 2000]})
    bad_csv = tmp_path / "bad.csv"
    df.to_csv(bad_csv, index=False)

    output_path = str(tmp_path / "output.html")

    with pytest.raises(ValueError, match="CSV file must contain a 'GEOID' column"):
        generate_choropleth(
            str(bad_csv),
            sample_data["json_path"],
            sample_data["token_path"],
            output_path,
        )


def test_generate_choropleth_invalid_geojson(sample_data, tmp_path):
    """Test choropleth generation with invalid GeoJSON."""
    # Create invalid GeoJSON
    invalid_json = tmp_path / "invalid.json"
    with open(invalid_json, "w") as f:
        json.dump({"type": "FeatureCollection"}, f)  # Missing features

    output_path = str(tmp_path / "output.html")

    with pytest.raises(ValueError, match="Invalid GeoJSON structure"):
        generate_choropleth(
            sample_data["csv_path"],
            str(invalid_json),
            sample_data["token_path"],
            output_path,
        )


def test_generate_choropleth_no_matching_geoids(sample_data, tmp_path):
    """Test choropleth generation with no matching GEOIDs."""
    # Create CSV with non-matching GEOIDs
    df = pd.DataFrame({"GEOID": ["99999", "88888"], "Total_Population": [1000, 2000]})
    no_match_csv = tmp_path / "no_match.csv"
    df.to_csv(no_match_csv, index=False)

    output_path = str(tmp_path / "output.html")

    with pytest.raises(ValueError, match="No matching GEOIDs found"):
        generate_choropleth(
            str(no_match_csv),
            sample_data["json_path"],
            sample_data["token_path"],
            output_path,
        )
