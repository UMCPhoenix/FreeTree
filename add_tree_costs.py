import pandas as pd
import numpy as np
import os

def calculate_tree_removal_cost(diameter):
    """
    Calculates the estimated cost of tree removal based on its diameter.
    This is a revised model with more realistic costs and variation. Costs can 
    vary greatly based on location, tree health, accessibility, and other factors.

    Args:
        diameter (float): The diameter of the tree in inches.

    Returns:
        float: The estimated removal cost.
    """
    base_cost = 150  # Increased base cost for setup, etc.
    cost_per_inch_diameter = 25  # Increased cost per inch of trunk diameter
    
    if pd.isna(diameter) or diameter <= 0:
        return np.nan
        
    # Base calculation using a quadratic term for non-linear growth
    cost = base_cost + (diameter * cost_per_inch_diameter) + (diameter**1.2 * 5)

    # Larger trees have a higher cost multiplier
    if diameter > 40:
        cost *= 2.0
    elif diameter > 20:
        cost *= 1.5

    # Add some random variation to make it more realistic
    # Using a normal distribution with a mean of 1 and a standard deviation of 0.20
    variation = np.random.normal(1, 0.20)
    cost *= variation
    
    # Ensure cost is not negative and round to 2 decimal places
    return round(max(200, cost), 2)

# --- 1. LOAD DATA & APPLY PRE-PROCESSING ---
print("--- Starting Data Processing Script ---")
try:
    # Use an absolute path for robustness
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join("DATA", "OLDDATA", "new_york_tree_census_2015.csv")
    tree_data = pd.read_csv(input_path)
    print(f"Successfully loaded dataset from {input_path}")
except FileNotFoundError:
    print(f"FATAL ERROR: The data file was not found at {input_path}")
    exit()

# --- 2. DATA CLEANING ---
# Remove rows with missing or zero diameter, as they cannot have a cost
original_rows = len(tree_data)
tree_data.dropna(subset=['tree_dbh'], inplace=True)
tree_data = tree_data[tree_data['tree_dbh'] > 0]
rows_after_nan = len(tree_data)
print(f"Removed {original_rows - rows_after_nan} rows with missing or zero diameter.")

# Remove extreme outliers that are likely data entry errors
max_diameter = 60 # A generous but realistic cap for urban trees
outliers = tree_data[tree_data['tree_dbh'] > max_diameter]
num_outliers = len(outliers)
if num_outliers > 0:
    tree_data = tree_data[tree_data['tree_dbh'] <= max_diameter]
    print(f"Removed {num_outliers} outlier trees with diameter > {max_diameter} inches.")

# --- 3. COST CALCULATION ---
print("Calculating removal costs...")
tree_data['estimated_cost'] = tree_data['tree_dbh'].apply(calculate_tree_removal_cost)
print("Cost calculation complete.")

# --- 4. SAVE CLEANED DATA ---
output_dir = os.path.join("DATA")
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, 'new_york_tree_census_2015_with_costs.csv')

tree_data.to_csv(output_path, index=False)
print(f"SUCCESS: Cleaned data with costs saved to '{output_path}'")
print(f"Final dataset contains {len(tree_data)} rows.")
print("\n--- Script Finished ---")
