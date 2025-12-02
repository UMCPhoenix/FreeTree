import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def visualize_tree_data(input_file_path, output_dir):
    """
    Reads the processed tree data and creates visualizations.

    Args:
        input_file_path (str): The path to the input CSV file with cost data.
        output_dir (str): The directory to save the plots.
    """
    try:
        # Read the data
        print(f"Reading data from {input_file_path}...")
        tree_data = pd.read_csv(input_file_path)
        print("Data read successfully.")

        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # --- Visualization 1: Scatter plot of Diameter vs. Cost ---
        print("Creating scatter plot of tree diameter vs. estimated cost...")
        plt.figure(figsize=(10, 6))
        sns.scatterplot(data=tree_data, x='tree_dbh', y='estimated_cost', alpha=0.5)
        plt.title('Tree Diameter vs. Estimated Removal Cost')
        plt.xlabel('Tree Diameter (inches)')
        plt.ylabel('Estimated Cost ($)')
        plt.grid(True)
        scatter_plot_path = os.path.join(output_dir, 'diameter_vs_cost_scatter.png')
        plt.savefig(scatter_plot_path)
        plt.close()
        print(f"Scatter plot saved to {scatter_plot_path}")

        # --- Visualization 2: Histogram of Estimated Costs ---
        print("Creating histogram of estimated costs...")
        plt.figure(figsize=(10, 6))
        sns.histplot(tree_data['estimated_cost'].dropna(), bins=50, kde=True)
        plt.title('Distribution of Estimated Tree Removal Costs')
        plt.xlabel('Estimated Cost ($)')
        plt.ylabel('Number of Trees')
        plt.grid(True)
        histogram_path = os.path.join(output_dir, 'cost_distribution_histogram.png')
        plt.savefig(histogram_path)
        plt.close()
        print(f"Histogram saved to {histogram_path}")

    except FileNotFoundError:
        print(f"Error: The file {input_file_path} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    input_dir = 'NEWDATA'
    output_dir = 'VISUALIZATIONS'
    input_file_name = 'new_york_tree_census_2015_with_costs.csv'
    
    input_path = os.path.join(input_dir, input_file_name)

    visualize_tree_data(input_path, output_dir)
