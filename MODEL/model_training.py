import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import xgboost as xgb
import matplotlib.pyplot as plt
import os

# --- 1. SETUP & DATA LOADING ---
print("--- Starting Model Training Script ---")
try:
    # Use an absolute path based on the script's location to prevent file not found errors
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(script_dir, 'new_york_tree_census_2015_with_costs.csv')
    df = pd.read_csv(data_path)
    print(f"Successfully loaded dataset from {data_path}")
except FileNotFoundError:
    print(f"FATAL ERROR: The data file was not found at {data_path}")
    exit()

# --- 2. FEATURE ENGINEERING ---
print("Starting feature engineering...")
# Define the target variable we want to predict
TARGET_VARIABLE = 'estimated_cost'

# Drop rows where the target variable is missing
df.dropna(subset=[TARGET_VARIABLE], inplace=True)

# Convert 'health' status from text to numbers. Default to 2 ('Fair') if value is missing.
health_map = {'Poor': 1, 'Fair': 2, 'Good': 3}
df['health_encoded'] = df['health'].map(health_map).fillna(2)

# To prevent the model from getting confused by too many rare species,
# we group all but the top 10 most common species into an 'Other' category.
top_10_species = df['spc_common'].value_counts().nlargest(10).index
df['species_simplified'] = df['spc_common'].apply(lambda x: x if x in top_10_species else 'Other')

# One-Hot Encode the simplified species categories into separate columns (spc_honeylocust, spc_pin oak, etc.)
species_dummies = pd.get_dummies(df['species_simplified'], prefix='spc')

# --- 3. FINAL FEATURE SELECTION ---
# Create a final, clean list of features for the model.
# This is the crucial step to prevent data type errors.
feature_list = ['tree_dbh', 'health_encoded'] + species_dummies.columns.tolist()
X = pd.concat([df[['tree_dbh', 'health_encoded']], species_dummies], axis=1)[feature_list]
y = df[TARGET_VARIABLE]
print("Feature engineering complete.")
print(f"Selected Features: {feature_list}")

# --- 4. DATA SPLITTING ---
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"Data split into {len(X_train)} training and {len(X_test)} testing samples.")

# --- 5. MODEL TRAINING ---
print("Training XGBoost model...")
# Initialize the XGBoost Regressor model
model = xgb.XGBRegressor(n_estimators=100, learning_rate=0.1, random_state=42, objective='reg:squarederror')
# Train the model on our training data
model.fit(X_train, y_train)
print("Model training complete.")

# --- 6. MODEL EVALUATION ---
predictions = model.predict(X_test)
mae = mean_absolute_error(y_test, predictions)
print(f"\n--- MODEL PERFORMANCE ---")
print(f"Mean Absolute Error: ${mae:,.2f}")
print("-------------------------\n")

# --- 7. FEATURE IMPORTANCE & VISUALIZATION ---
print("Generating feature importance plot...")
# Define the output directory for the plot
project_root = os.path.dirname(script_dir)
output_dir = os.path.join(project_root, 'VISUALIZATIONS')
os.makedirs(output_dir, exist_ok=True)
plot_path = os.path.join(output_dir, 'feature_importance.png')

# Create the plot
plt.figure(figsize=(10, 8))
xgb.plot_importance(model, height=0.8, max_num_features=10, importance_type='weight', show_values=False, title='Feature Importance')
plt.xlabel("Importance (Weight)")
plt.tight_layout()

# Save the plot
plt.savefig(plot_path)
print(f"SUCCESS: Feature importance plot saved to '{plot_path}'")

# Attempt to show the plot in a window to confirm generation
try:
    print("Attempting to display plot...")
    plt.show()
except Exception as e:
    print(f"Could not display plot window, but file should be saved. Error: {e}")

print("\n--- Script Finished ---")