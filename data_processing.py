import pandas as pd

def process_csv(input_file, output_file, columns_to_keep):
    try:
        df = pd.read_csv(input_file)
        df = df.drop(0)
        df = df[columns_to_keep]
        df.to_csv(output_file, index=False)
        print(f"Processed CSV saved to {output_file}")
    except Exception as e:
        print(f"Error: {str(e)}")

def convert_and_save_csv(input_csv_file, output_csv_file, selected_columns, column_rename_mapping):
    df = pd.read_csv(input_csv_file)
    df.rename(columns=column_rename_mapping, inplace=True)
    df = df[selected_columns]
    df['Total_Population'] = pd.to_numeric(df['Total_Population'], errors='coerce')
    df['Total_Population'].fillna(0, inplace=True)
    df['GEOID'] = df['GEOID'].str[9:]
    df.to_csv(output_csv_file, index=False)
    return df.dtypes, df.isnull().sum()

def process_acs_csv(input_file, output_file, column_mapping):
    """
    Process ACS CSV file with proper handling of the dual header structure.
    
    Args:
        input_file: Path to raw ACS CSV file
        output_file: Path to save processed CSV
        column_mapping: Dict mapping ACS column codes to readable names
                       e.g. {'S2701_C01_001E': 'Total_Population'}
    """
    try:
        # Read the CSV file, skipping the second header row
        df = pd.read_csv(input_file)
        df = df.drop(0)
        
        # Select and rename columns in one step
        columns_to_keep = ['GEO_ID'] + list(column_mapping.keys())
        df = df[columns_to_keep]
        
        # Add GEOID to the mapping for consistent naming
        full_mapping = {'GEO_ID': 'GEOID', **column_mapping}
        df.rename(columns=full_mapping, inplace=True)
        
        # Process GEOID to remove the prefix (e.g., "1400000US")
        df['GEOID'] = df['GEOID'].str[9:]
        
        # Convert numeric columns and handle missing values
        for col in column_mapping.values():
            df[col] = pd.to_numeric(df[col], errors='coerce')
            df[col].fillna(0, inplace=True)
        
        # Save processed data
        df.to_csv(output_file, index=False)
        return df.dtypes, df.isnull().sum()
    except Exception as e:
        print(f"Error processing ACS CSV: {str(e)}")
        raise

def print_population_stats(df, column):
    """Print percentile statistics for a numeric column."""
    df[column] = pd.to_numeric(df[column], errors='coerce')
    percentiles = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 99, 100]
    print("Summary Statistics:")
    print(f"min: {df[column].min()}")
    for p in percentiles:
        print(f"{p}%ile: {df[column].quantile(p / 100)}")
    print(f"max: {df[column].max()}")
