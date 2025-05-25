import pytest
from data_processing import clean_data
import pandas as pd

def test_clean_data_basic():
    # Create a simple test DataFrame
    test_data = pd.DataFrame({
        'column1': ['value1', 'value2'],
        'column2': [1, 2]
    })
    
    # Test that the function doesn't raise any errors
    try:
        result = clean_data(test_data)
        assert isinstance(result, pd.DataFrame)
    except Exception as e:
        pytest.fail(f"clean_data raised an exception: {e}")

def test_imports():
    """Test that all main project modules can be imported."""
    try:
        import main
        import visualization
        import geojson_utils
        import config
    except ImportError as e:
        pytest.fail(f"Failed to import project modules: {e}") 