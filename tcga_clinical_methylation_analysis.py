import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
import seaborn as sns

print("🚀 FAST TCGA Clinical + Methylation Analysis\n")

# ==============================
# 1️⃣ Load methylation
# ==============================

meth = pd.read_csv(
    r"C:\Users\Shalini\Desktop\IBS2_PROJECT\dataset\methylation_cleaned.csv",
    index_col=0
)

meth = meth.T
print("Methylation shape:", meth.shape)

# ==============================
# 2️⃣ Load top CpGs used in training
# ==============================

train_cpgs = pd.read_csv(
    r"C:\Users\Shalini\Desktop\IBS2_PROJECT\results\train_cpgs.csv",
    header=None
)[0].tolist()

meth = meth[train_cpgs]
print("Using top CpGs:", meth.shape)

# ==============================
# 3️⃣ Load clinical
# ==============================

clinical = pd.read_csv(
    r"C:\Users\Shalini\Downloads\brca_tcga_clinical_data.tsv",
    sep="\t"
)

clinical = clinical[[
    "Sample ID",
    "ER Status By IHC",
    "PR status by ihc",
    "HER2 fish status"
]].copy()

clinical.columns = ["sample", "ER", "PR", "HER2"]

# ==============================
# 4️⃣ Merge
# ==============================

meth["sample"] = meth.index
merged = meth.merge(clinical, on="sample")

print("Merged shape:", merged.shape)

# ==============================
# 5️⃣ Construct subtype
# ==============================


def assign_subtype(row):
    if row["ER"] == "Negative" and row["PR"] == "Negative" and row["HER2"] == "Negative":
        return "Basal"
    elif row["ER"] == "Positive" and row["HER2"] == "Negative":
        return "Luminal_A"
    elif row["ER"] == "Positive" and row["HER2"] == "Positive":
        return "Luminal_B"
    elif row["ER"] == "Negative" and row["HER2"] == "Positive":
        return "HER2_Enriched"
    else:
        return "Other"


merged["Subtype"] = merged.apply(assign_subtype, axis=1)

print("\nSubtype distribution:")
print(merged["Subtype"].value_counts())

# ==============================
# 6️⃣ Scale + PCA
# ==============================

features = merged.drop(columns=["sample", "ER", "PR", "HER2", "Subtype"])

features = features.fillna(features.mean())

scaler = StandardScaler()
X_scaled = scaler.fit_transform(features)

pca = PCA(n_components=10, random_state=42)
X_pca = pca.fit_transform(X_scaled)

# ==============================
# 7️⃣ KMeans
# ==============================

kmeans = KMeans(n_clusters=4, random_state=42)
clusters = kmeans.fit_predict(X_pca)

merged["Cluster"] = clusters

print("\nSilhouette Score:", silhouette_score(X_pca, clusters))

print("\nCluster vs Subtype:")
print(pd.crosstab(merged["Cluster"], merged["Subtype"]))

# ==============================
# 8️⃣ PCA Plot
# ==============================

pca_2d = PCA(n_components=2, random_state=42)
pca_result = pca_2d.fit_transform(X_scaled)

plt.figure(figsize=(8, 6))
sns.scatterplot(
    x=pca_result[:, 0],
    y=pca_result[:, 1],
    hue=merged["Subtype"],
    palette="tab10"
)

plt.title("TCGA Methylation (Top CpGs) by Clinical Subtype")
plt.show()

print("\n🔥 FAST Clinical Validation Complete")
