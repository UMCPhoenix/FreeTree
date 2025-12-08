import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Load cleaned tree census data
data_path = os.path.join('DATA', 'new_york_tree_census_2015_with_costs.csv')
df = pd.read_csv(data_path)

diameter_stats = df['tree_dbh'].describe()
cost_stats = df['estimated_cost'].describe()
health_counts = df['health'].value_counts(dropna=False)
status_counts = df['status'].value_counts(dropna=False)
top_species = df['spc_common'].value_counts().head(5)

sns.set_theme(style="whitegrid")
fig, axes = plt.subplots(2, 2, figsize=(16, 10))
fig.suptitle('NYC Tree Census 2015: Dataset Summary', fontsize=20, weight='bold')

axes[0,0].axis('off')
stats_text = (
    f"Total Trees: {len(df):,}\n"
    f"Diameter (inches):\n"
    f"  Mean: {diameter_stats['mean']:.1f}\n"
    f"  Median: {diameter_stats['50%']:.1f}\n"
    f"  Min: {diameter_stats['min']:.1f}\n"
    f"  Max: {diameter_stats['max']:.1f}\n"
    f"Cost ($):\n"
    f"  Mean: {cost_stats['mean']:.0f}\n"
    f"  Median: {cost_stats['50%']:.0f}\n"
    f"  Min: {cost_stats['min']:.0f}\n"
    f"  Max: {cost_stats['max']:.0f}\n"
)
axes[0,0].text(0, 0.5, stats_text, fontsize=14, va='center', ha='left', family='monospace')
axes[0,0].set_title('Key Statistics', fontsize=16, weight='bold')

sns.barplot(x=health_counts.index, y=health_counts.values, ax=axes[0,1], palette='crest')
axes[0,1].set_title('Tree Health Distribution', fontsize=16, weight='bold')
axes[0,1].set_xlabel('Health')
axes[0,1].set_ylabel('Count')

sns.barplot(x=status_counts.index, y=status_counts.values, ax=axes[1,0], palette='flare')
axes[1,0].set_title('Tree Status Distribution', fontsize=16, weight='bold')
axes[1,0].set_xlabel('Status')
axes[1,0].set_ylabel('Count')

sns.barplot(y=top_species.index, x=top_species.values, ax=axes[1,1], palette='viridis')
axes[1,1].set_title('Top 5 Tree Species', fontsize=16, weight='bold')
axes[1,1].set_xlabel('Count')
axes[1,1].set_ylabel('Species')

plt.tight_layout(rect=[0, 0, 1, 0.96])
output_path = os.path.join('VISUALIZATIONS', 'dataset_summary.png')
plt.savefig(output_path, dpi=150)
plt.close()
print(f"Infographic saved to {output_path}")
