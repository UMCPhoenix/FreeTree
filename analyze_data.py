import pandas as pd
import os

def analyze_tree_data(input_file_path):
    """
    Performs a basic analysis of the tree data.

    Args:
        input_file_path (str): The path to the input CSV file.
    """
    try:
        # Read the data
        print(f"Reading data from {input_file_path}...")
        tree_data = pd.read_csv(input_file_path)
        print("Data read successfully.\n")

        print("--- Data Analysis Report ---")

        # --- 1. Basic Information ---
        print("\n1. Basic Information:")
        print(f"Number of trees in dataset: {len(tree_data)}")
        print(f"Number of columns (features): {len(tree_data.columns)}")
        
        # --- 2. Descriptive Statistics for Numerical Columns ---
        print("\n2. Summary for Numerical Columns:")
        # Select only numeric columns for describe()
        numeric_cols = tree_data.select_dtypes(include=['number'])
        print(numeric_cols.describe())

        # --- 3. Health Distribution ---
        if 'health' in tree_data.columns:
            print("\n3. Tree Health Distribution:")
            print(tree_data['health'].value_counts(normalize=True) * 100)
        
        # --- 4. Species Distribution ---
        if 'spc_common' in tree_data.columns:
            print("\n4. Top 10 Most Common Tree Species:")
            print(tree_data['spc_common'].value_counts().head(10))
            
        # --- 5. Status Distribution ---
        if 'status' in tree_data.columns:
            print("\n5. Tree Status Distribution:")
            print(tree_data['status'].value_counts(normalize=True) * 100)

        print("\n--- End of Report ---")


    except FileNotFoundError:
        print(f"Error: The file {input_file_path} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    input_dir = 'NEWDATA'
    input_file_name = 'new_york_tree_census_2015_with_costs.csv'
    
    input_path = os.path.join(input_dir, input_file_name)

    analyze_tree_data(input_path)
