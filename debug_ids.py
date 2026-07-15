import pandas as pd

meth = pd.read_csv("../results/methylation_top200.csv", index_col=0)
labels = pd.read_csv("../results/sample_labels.csv")

print("Methylation samples (first 5):")
print(meth.index[:5])

print("\nLabels samples (first 5):")
print(labels["sample"].head())

print("\nMethylation patient IDs:")
print(meth.index.str[:12].unique()[:5])

print("\nLabel patient IDs:")
print(labels["sample"].str[:12].unique()[:5])

print("\nOverlap count:")
print(len(set(meth.index.str[:12]) & set(labels["sample"].str[:12])))
