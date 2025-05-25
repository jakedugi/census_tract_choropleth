import pytest
import pandas as pd
import os
from data_processing import (
    process_acs_csv,
    process_csv,
    print_population_stats,
    clean_data,
)


@pytest.fixture
def sample_acs_data():
    """Create sample ACS data for testing."""
    return pd.DataFrame(
        {
            "GEO_ID": ["1400000US01001", "1400000US01002"],
            "S2701_C01_001E": ["1000", "2000"],
            "S2701_C01_002E": ["800", "1600"],
        }
    )


@pytest.fixture
def column_mapping():
    """Sample column mapping for testing."""
    return {
        "S2701_C01_001E": "Total_Population",
        "S2701_C01_002E": "Insured_Population",
    }


def test_process_acs_csv(tmp_path, sample_acs_data, column_mapping):
    """Test ACS CSV processing functionality."""
    # Create input file
    input_file = tmp_path / "input.csv"
    sample_acs_data.to_csv(input_file, index=False)

    # Create output file path
    output_file = tmp_path / "output.csv"

    # Process the data
    dtypes, null_counts = process_acs_csv(input_file, output_file, column_mapping)

    # Read processed data
    processed_df = pd.read_csv(output_file)

    # Verify processing
    assert "GEOID" in processed_df.columns
    assert "Total_Population" in processed_df.columns
    assert processed_df["GEOID"].iloc[0] == "01001"  # Check GEOID format
    assert (
        processed_df["Total_Population"].dtype == "float64"
    )  # Check numeric conversion
    assert (
        processed_df["Total_Population"].iloc[0] == 1000.0
    )  # Check value preservation
    assert len(processed_df) == len(sample_acs_data)  # Check row count preservation


def test_process_csv(tmp_path):
    """Test basic CSV processing."""
    # Create test data with header row and data row
    test_df = pd.DataFrame(
        {"col1": ["header", "1"], "col2": ["header", "a"], "col3": ["header", "true"]}
    )

    input_file = tmp_path / "input.csv"
    output_file = tmp_path / "output.csv"
    test_df.to_csv(input_file, index=False)

    # Test processing with subset of columns
    columns_to_keep = ["col1", "col2"]
    process_csv(input_file, output_file, columns_to_keep)

    # Verify results - read with string types
    result_df = pd.read_csv(output_file, dtype=str)
    assert list(result_df.columns) == columns_to_keep
    assert len(result_df) == 1  # One row after dropping header
    assert result_df["col1"].iloc[0] == "1"  # Check value preservation


def test_print_population_stats(capsys):
    """Test population statistics printing."""
    df = pd.DataFrame({"Total_Population": [100, 200, 300, 400, 500]})

    print_population_stats(df, "Total_Population")
    captured = capsys.readouterr()

    # Verify output contains key statistics
    assert "Summary Statistics:" in captured.out
    assert "min: 100.0" in captured.out
    assert "max: 500.0" in captured.out
    for percentile in [0, 50, 100]:
        assert f"{percentile}%ile:" in captured.out


def test_process_acs_csv_error_handling(tmp_path):
    """Test error handling in ACS processing."""
    non_existent_file = tmp_path / "nonexistent.csv"
    output_file = tmp_path / "output.csv"

    with pytest.raises(Exception):
        process_acs_csv(non_existent_file, output_file, {})


def test_clean_data_basic():
    """Test basic data cleaning functionality."""
    # Create a simple test DataFrame
    test_data = pd.DataFrame({"column1": ["value1", "value2"], "column2": [1, 2]})

    # Test that the function doesn't raise any errors
    try:
        result = clean_data(test_data)
        assert isinstance(result, pd.DataFrame)
    except Exception as e:
        pytest.fail(f"clean_data raised an exception: {e}")


def test_clean_data_missing_values():
    """Test handling of missing values in data cleaning."""
    test_data = pd.DataFrame(
        {"column1": ["value1", None, "value3"], "column2": [1, 2, None]}
    )

    result = clean_data(test_data)
    assert isinstance(result, pd.DataFrame)
    # Verify that NaN values are handled appropriately
    assert result["column1"].isna().sum() == 1
    assert result["column2"].isna().sum() == 1


def test_imports():
    """Test that all main project modules can be imported."""
    try:
        import main
        import visualization
        import geojson_utils
        import config
    except ImportError as e:
        pytest.fail(f"Failed to import project modules: {e}")
