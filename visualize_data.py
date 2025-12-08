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
        print(f"Reading data from {input_file_path}...")
        tree_data = pd.read_csv(input_file_path)
        print("Data read successfully.")

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        import seaborn as sns
        sns.set_theme(style="whitegrid")

        # --- Visualization 1: Enhanced Scatter plot ---
        plt.figure(figsize=(12, 8))
        scatter = sns.scatterplot(
            data=tree_data, x='tree_dbh', y='estimated_cost',
            hue='health', palette='viridis', alpha=0.4, edgecolor=None, legend='brief')
        plt.title('Tree Diameter vs. Estimated Removal Cost', fontsize=18, weight='bold')
        plt.xlabel('Tree Diameter (inches)', fontsize=14)
        plt.ylabel('Estimated Cost ($)', fontsize=14)
        plt.grid(True, linestyle='--', alpha=0.6)
        # Annotate mean and median
        mean_cost = tree_data['estimated_cost'].mean()
        median_cost = tree_data['estimated_cost'].median()
        plt.axhline(mean_cost, color='red', linestyle='--', label=f'Mean Cost (${mean_cost:.0f})')
        plt.axhline(median_cost, color='blue', linestyle=':', label=f'Median Cost (${median_cost:.0f})')
        plt.legend()
        scatter_plot_path = os.path.join(output_dir, 'diameter_vs_cost_scatter.png')
        plt.tight_layout()
        plt.savefig(scatter_plot_path, dpi=150)
        plt.close()
        print(f"Scatter plot saved to {scatter_plot_path}")

        # --- Visualization 2: Enhanced Histogram ---
        plt.figure(figsize=(12, 8))
        hist = sns.histplot(
            tree_data['estimated_cost'].dropna(), bins=50, kde=True,
            color='teal', edgecolor=None)
        plt.title('Distribution of Estimated Tree Removal Costs', fontsize=18, weight='bold')
        plt.xlabel('Estimated Cost ($)', fontsize=14)
        plt.ylabel('Number of Trees', fontsize=14)
        plt.grid(True, linestyle='--', alpha=0.6)
        # Annotate mean and median
        plt.axvline(mean_cost, color='red', linestyle='--', label=f'Mean (${mean_cost:.0f})')
        plt.axvline(median_cost, color='blue', linestyle=':', label=f'Median (${median_cost:.0f})')
        plt.legend()
        histogram_path = os.path.join(output_dir, 'cost_distribution_histogram.png')
        plt.tight_layout()
        plt.savefig(histogram_path, dpi=150)
        plt.close()
        print(f"Histogram saved to {histogram_path}")

    except FileNotFoundError:
        print(f"Error: The file {input_file_path} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    input_dir = 'DATA'
    output_dir = 'VISUALIZATIONS'
    input_file_name = 'new_york_tree_census_2015_with_costs.csv'
    
    input_path = os.path.join(input_dir, input_file_name)

    visualize_tree_data(input_path, output_dir)
