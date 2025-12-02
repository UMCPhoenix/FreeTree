import pandas as pd
import os

# Correct file path, assuming check.py is in the same directory as the CSV
file_path = 'new_york_tree_census_2015_with_costs.csv'

# Check if the file exists before trying to load it
if not os.path.exists(file_path):
    print(f"Error: The file '{file_path}' was not found in the current directory.")
    print("Please make sure 'add_tree_costs.py' has been run successfully.")
else:
    # Load your new dataset
    df = pd.read_csv(file_path)

    print("--- DATA SANITY CHECK ---")

    # 1. Check average cost by health status
    if 'health' in df.columns and 'estimated_cost' in df.columns:
        print("\nAverage Cost by Health Status:")
        # Fill NaN values in 'health' for groupby to work, e.g., with 'Unknown'
        print(df.groupby(df['health'].fillna('Unknown'))['estimated_cost'].mean().sort_values())
    else:
        print("\nCould not perform health vs. cost analysis. Missing 'health' or 'estimated_cost' column.")

    # 2. Compare costs of two different common species
    if 'tree_dbh' in df.columns and 'spc_common' in df.columns and 'estimated_cost' in df.columns:
        # We filter for a specific size range (e.g. 15-25 inches) to make it a fair comparison
        mid_size = df[(df['tree_dbh'] >= 15) & (df['tree_dbh'] <= 25)].copy()

        print("\nAverage Cost for 15-25 inch trees (Oak vs. London Planetree):")
        
        # Calculate mean cost for oaks
        oaks = mid_size[mid_size['spc_common'].str.contains('oak', case=False, na=False)]
        oaks_mean = oaks['estimated_cost'].mean()

        # Calculate mean cost for planetrees
        planetrees = mid_size[mid_size['spc_common'].str.contains('planetree', case=False, na=False)]
        planetrees_mean = planetrees['estimated_cost'].mean()

        if pd.notna(oaks_mean):
            print(f"Oak: ${oaks_mean:.2f} (from {len(oaks)} trees)")
        else:
            print("No 'Oak' trees found in this size range.")
            
        if pd.notna(planetrees_mean):
            print(f"London Planetree: ${planetrees_mean:.2f} (from {len(planetrees)} trees)")
        else:
            print("No 'London Planetree' trees found in this size range.")
    else:
        print("\nCould not perform species cost comparison. Missing required columns.")


    # 3. Check for Null/Missing values in the target
    if 'estimated_cost' in df.columns:
        missing_prices = df['estimated_cost'].isnull().sum()
        total_rows = len(df)
        missing_percentage = (missing_prices / total_rows) * 100
        print(f"\nMissing Prices: {missing_prices} ({missing_percentage:.2f}%)")
    else:
        print("\n'estimated_cost' column not found for null value check.")
