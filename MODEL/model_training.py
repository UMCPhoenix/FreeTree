import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import xgboost as xgb
import matplotlib.pyplot as plt
import os

# 1. Load cleaned tree census data
print("--- Starting Model Training Script ---")
try:
    # Use absolute path for reliability
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(script_dir, '..', 'DATA', 'new_york_tree_census_2015_with_costs.csv')
    df = pd.read_csv(data_path)
    print(f"Successfully loaded dataset from {data_path}")
except FileNotFoundError:
    print(f"ERROR: Data file not found at {data_path}")
    exit()

# 2. Prepare features for regression
print("Starting feature engineering...")
# Target variable: estimated tree removal cost
TARGET_VARIABLE = 'estimated_cost'
df.dropna(subset=[TARGET_VARIABLE], inplace=True)

# Encode health status numerically (Poor=1, Fair=2, Good=3)
health_map = {'Poor': 1, 'Fair': 2, 'Good': 3}
df['health_encoded'] = df['health'].map(health_map).fillna(2)

# Group rare species as 'Other' and one-hot encode top 10 species
top_10_species = df['spc_common'].value_counts().nlargest(10).index
df['species_simplified'] = df['spc_common'].apply(lambda x: x if x in top_10_species else 'Other')
species_dummies = pd.get_dummies(df['species_simplified'], prefix='spc')

# Final feature set: diameter, health, and species indicators
feature_list = ['tree_dbh', 'health_encoded'] + species_dummies.columns.tolist()
X = pd.concat([df[['tree_dbh', 'health_encoded']], species_dummies], axis=1)[feature_list]
y = df[TARGET_VARIABLE]
print("Feature engineering complete.")
print(f"Selected Features: {feature_list}")

# 3. Split data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"Data split: {len(X_train)} train / {len(X_test)} test samples.")

# 4. Fit regression model
print("Training XGBoost regression model...")
model = xgb.XGBRegressor(n_estimators=100, learning_rate=0.1, random_state=42, objective='reg:squarederror')
model.fit(X_train, y_train)
print("Model training complete.")

# 5. Evaluate model performance
predictions = model.predict(X_test)
mae = mean_absolute_error(y_test, predictions)
print(f"\nModel Mean Absolute Error: ${mae:,.2f}")
print("-------------------------\n")

# 6. Visualize feature importance
print("Generating feature importance plot...")
output_dir = os.path.abspath(os.path.join(script_dir, '..', 'VISUALIZATIONS'))
os.makedirs(output_dir, exist_ok=True)
plot_path = os.path.join(output_dir, 'feature_importance.png')

plt.figure(figsize=(10, 8))
xgb.plot_importance(model, height=0.8, max_num_features=10, importance_type='weight', show_values=False, title='Feature Importance')
plt.xlabel("Importance (Weight)")
plt.tight_layout()
plt.savefig(plot_path)
print(f"Feature importance plot saved to '{plot_path}'")

try:
    print("Attempting to display plot...")
    plt.show()
except Exception as e:
    print(f"Could not display plot window, but file should be saved. Error: {e}")

print("\nScript finished.")