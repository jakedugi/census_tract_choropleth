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

def print_population_stats(df, column):
    df[column] = pd.to_numeric(df[column], errors='coerce')
    percentiles = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 99, 100]
    print("Summary Statistics:")
    print(f"min: {df[column].min()}")
    for p in percentiles:
        print(f"{p}%ile: {df[column].quantile(p / 100)}")
    print(f"max: {df[column].max()}")