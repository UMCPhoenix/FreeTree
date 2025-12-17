# FreeTree: NYC Tree Census Data Analysis and Modeling

## Overview
FreeTree is a data science project that analyzes and models the cost of tree removal in New York City using public tree census data. The project includes data cleaning, cost estimation, visualization, and predictive modeling, with a focus on interpretability and reproducibility.

## Project Structure
```
FreeTree/
├── add_tree_costs.py                # Cleans raw data, estimates removal costs, outputs cleaned CSV
├── analyze_data.py                  # (Optional) Prints summary stats and distributions
├── dataset_summary.py               # Generates infographic summary of dataset
├── visualize_data.py                # Creates scatter/histogram plots from cleaned data
├── MODEL/
│   ├── model_training.py            # Trains regression model, outputs feature importance
│   └── check.py                     # (Optional) Helper or test script
├── DATA/
│   ├── new_york_tree_census_2015_with_costs.csv   # Cleaned data with costs
│   └── OLDDATA/
│       ├── new_york_tree_census_1995.csv          # Raw census data
│       ├── new_york_tree_census_2005.csv
│       ├── new_york_tree_census_2015.csv
│       └── new_york_tree_species.csv
├── VISUALIZATIONS/
│   ├── cost_distribution_histogram.png
│   ├── diameter_vs_cost_scatter.png
│   ├── feature_importance.png
│   └── dataset_summary.png
```

## Workflow
1. **Data Cleaning & Cost Estimation**
   - Run `add_tree_costs.py` to clean the raw 2015 census data, remove outliers, and estimate removal costs.
   - Output: `DATA/new_york_tree_census_2015_with_costs.csv`

2. **Visualization**
   - Run `visualize_data.py` to generate scatter and histogram plots of diameter vs. cost and cost distribution.
   - Run `dataset_summary.py` to create an infographic summary of the dataset.
   - Outputs: PNG files in `VISUALIZATIONS/`

3. **Model Training**
   - Run `MODEL/model_training.py` to train a regression model (XGBoost) on the cleaned data.
   - The script encodes categorical variables, splits data, trains the model, evaluates performance, and saves a feature importance plot.
   - Output: `feature_importance.png` in `VISUALIZATIONS/`

## Key Scripts
- **add_tree_costs.py**: Cleans and processes raw data, estimates tree removal costs.
- **visualize_data.py**: Visualizes relationships and distributions in the cleaned data.
- **dataset_summary.py**: Creates a multi-panel infographic of key dataset stats.
- **MODEL/model_training.py**: Trains and evaluates a regression model, visualizes feature importance.

## Data Sources
- NYC Street Tree Census data (1995, 2005, 2015)
- Tree species reference data

## Requirements
- Python 3.8+
- pandas, numpy, matplotlib, seaborn, xgboost, scikit-learn

Install dependencies with:
```
pip install pandas numpy matplotlib seaborn xgboost scikit-learn
```

## Usage
1. Place raw census CSVs in `DATA/OLDDATA/`.
2. Run scripts in the order above for a full workflow.
3. View outputs in `DATA/` and `VISUALIZATIONS/`.

## Notes
- All scripts use relative paths for cross-platform compatibility.
- Feature importance in the model is based on XGBoost's split count ("weight").
- For questions or improvements, see code comments for guidance.

---
Created by UMCPhoenix, 2025.
