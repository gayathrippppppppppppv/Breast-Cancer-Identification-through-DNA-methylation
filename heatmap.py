import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
data = pd.read_csv("../results/methylation_ml_dataset.csv")
top = pd.read_csv("../results/top_cpg_importance.csv").head(20)["CpG"]

# Subset
heatmap_data = data.set_index("sample")[top]

# Plot
plt.figure(figsize=(10, 6))
sns.heatmap(heatmap_data, cmap="viridis")
plt.title("Top CpG Methylation Patterns")
plt.tight_layout()
plt.savefig("../results/figures/cpg_heatmap.png")
plt.close()

print("✅ Heatmap saved")
