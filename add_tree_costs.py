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

def process_tree_data(input_file_path, output_file_path):
    """
    Reads tree census data, calculates removal costs, and saves the
    data to a new CSV file.

    Args:
        input_file_path (str): The path to the input CSV file.
        output_file_path (str): The path where the output CSV file will be saved.
    """
    try:
        # Read the CSV file
        print(f"Reading data from {input_file_path}...")
        tree_data = pd.read_csv(input_file_path)
        print("Data read successfully.")

        # Ensure the 'tree_dbh' column exists
        if 'tree_dbh' not in tree_data.columns:
            print("Error: 'tree_dbh' column not found in the input file.")
            return

        # Calculate the removal cost
        print("Calculating removal costs...")
        tree_data['estimated_cost'] = tree_data['tree_dbh'].apply(calculate_tree_removal_cost)
        print("Cost calculation complete.")

        # Save the new dataframe to a CSV
        print(f"Saving data to {output_file_path}...")
        tree_data.to_csv(output_file_path, index=False)
        print(f"Successfully created {output_file_path}")

    except FileNotFoundError:
        print(f"Error: The file {input_file_path} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Define file paths
    input_dir = 'OLDDATA'
    output_dir = 'NEWDATA'
    input_file_name = 'new_york_tree_census_2015.csv'
    output_file_name = 'new_york_tree_census_2015_with_costs.csv'

    input_path = os.path.join(input_dir, input_file_name)
    
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    output_path = os.path.join(output_dir, output_file_name)

    # Process the data
    process_tree_data(input_path, output_path)
