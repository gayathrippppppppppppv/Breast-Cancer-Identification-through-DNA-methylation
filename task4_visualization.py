import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ==============================
# Paths
# ==============================
STAT_PATH = "../results/task1_statistical_validation.csv"
ANNOT_PATH = "../results/task2_biological_annotation.csv"
PATHWAY_PATH = "../results/task3_pathway_enrichment.csv"
ML_DATA_PATH = "../results/methylation_ml_dataset.csv"
OUT_DIR = "../results/figures/"

# ==============================
# Load data
# ==============================
stat = pd.read_csv(STAT_PATH)
annot = pd.read_csv(ANNOT_PATH)
pathways = pd.read_csv(PATHWAY_PATH)
ml = pd.read_csv(ML_DATA_PATH)

# ==============================
# TASK 4.1 – Volcano Plot
# ==============================
stat["-log10(p)"] = -np.log10(stat["p_value"])

plt.figure(figsize=(8,6))
plt.scatter(stat["Mean_diff"], stat["-log10(p)"], alpha=0.6)
plt.axhline(-np.log10(0.05), linestyle="--")
plt.xlabel("Mean Methylation Difference (Cancer – Normal)")
plt.ylabel("-log10(p-value)")
plt.title("Volcano Plot of Differentially Methylated CpGs")
plt.tight_layout()
plt.savefig(f"{OUT_DIR}/volcano_plot.png", dpi=300)
plt.close()

print("✅ Volcano plot saved")

# ==============================
# TASK 4.2 – Heatmap (Top 20 CpGs)
# ==============================
top_cpgs = stat.sort_values("p_value").head(20)["CpG"]

heat_data = ml.set_index("sample")[top_cpgs]
heat_data["Label"] = ml["label"].values

heat_data = heat_data.sort_values("Label")
heat_matrix = heat_data.drop(columns="Label")

plt.figure(figsize=(10,6))
sns.heatmap(heat_matrix, cmap="viridis", yticklabels=False)
plt.title("Heatmap of Top 20 Differential CpGs")
plt.xlabel("CpG Sites")
plt.ylabel("Samples")
plt.tight_layout()
plt.savefig(f"{OUT_DIR}/top20_cpg_heatmap.png", dpi=300)
plt.close()

print("✅ Heatmap saved")

# ==============================
# TASK 4.3 – Pathway Enrichment Bar Plot
# ==============================
top_pathways = pathways.sort_values("Adjusted P-value").head(10)

plt.figure(figsize=(8,5))
plt.barh(
    top_pathways["Term"],
    -np.log10(top_pathways["Adjusted P-value"])
)
plt.xlabel("-log10 Adjusted P-value")
plt.title("Top Enriched KEGG Pathways")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig(f"{OUT_DIR}/pathway_enrichment.png", dpi=300)
plt.close()

print("✅ Pathway enrichment plot saved")

print("\n🎯 TASK 4 COMPLETED – All figures generated")
