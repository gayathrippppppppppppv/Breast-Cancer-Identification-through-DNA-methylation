import pandas as pd

# Load cleaned methylation
meth = pd.read_csv("../results/methylation_cleaned.csv", index_col=0)

# Extract sample type from TCGA barcode
labels = []
for sample in meth.columns:
    if sample.endswith("-01"):
        labels.append("Cancer")
    elif sample.endswith("-11"):
        labels.append("Normal")
    else:
        labels.append(None)

label_df = pd.DataFrame({
    "sample": meth.columns,
    "label": labels
})

# Keep only Cancer and Normal
label_df = label_df.dropna()

label_df.to_csv("../results/sample_labels.csv", index=False)

print("✅ Labels created")
print(label_df["label"].value_counts())
