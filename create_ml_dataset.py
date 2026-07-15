import pandas as pd

# Paths
METH_PATH = "../results/methylation_top200.csv"
LABEL_PATH = "../results/sample_labels.csv"
OUT_PATH = "../results/methylation_ml_dataset.csv"

# Load methylation (CpGs x Samples)
meth = pd.read_csv(METH_PATH, index_col=0)

# 🔁 TRANSPOSE → Samples x CpGs
meth = meth.T

# Create sample column
meth["sample"] = meth.index

# Reset index
meth.reset_index(drop=True, inplace=True)

# Load labels
labels = pd.read_csv(LABEL_PATH)

# Merge
data = meth.merge(labels, on="sample", how="inner")

# Safety check
if data.shape[0] == 0:
    raise ValueError("❌ Merge failed: no overlapping samples")

# Save
data.to_csv(OUT_PATH, index=False)

print("✅ ML dataset created")
print(data["label"].value_counts())
