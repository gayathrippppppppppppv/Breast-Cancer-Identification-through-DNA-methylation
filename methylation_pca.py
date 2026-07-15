import os
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# =============================
# Paths
# =============================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS_DIR = os.path.join(BASE_DIR, "results")
FIG_DIR = os.path.join(RESULTS_DIR, "figures")

os.makedirs(FIG_DIR, exist_ok=True)

METH_PATH = os.path.join(RESULTS_DIR, "methylation_cleaned.csv")

# =============================
# Load methylation
# =============================
if not os.path.exists(METH_PATH):
    raise FileNotFoundError("❌ methylation_cleaned.csv not found in results/")

meth = pd.read_csv(METH_PATH, index_col=0)
print(f"✅ Loaded cleaned methylation: {meth.shape}")

# =============================
# Transpose for PCA (samples × features)
# =============================
X = meth.T
print(f"🔄 PCA input shape (samples × CpGs): {X.shape}")

# =============================
# Standardization
# =============================
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# =============================
# PCA
# =============================
pca = PCA(n_components=10)
X_pca = pca.fit_transform(X_scaled)

# =============================
# Save PCA coordinates
# =============================
pca_df = pd.DataFrame(
    X_pca[:, :2],
    columns=["PC1", "PC2"],
    index=X.index
)

pca_df.to_csv(os.path.join(RESULTS_DIR, "pca_coordinates.csv"))

# =============================
# Plot PCA
# =============================
plt.figure(figsize=(7, 6))
plt.scatter(pca_df["PC1"], pca_df["PC2"], s=10)
plt.xlabel(f"PC1 ({pca.explained_variance_ratio_[0]*100:.2f}%)")
plt.ylabel(f"PC2 ({pca.explained_variance_ratio_[1]*100:.2f}%)")
plt.title("TCGA BRCA DNA Methylation PCA")
plt.tight_layout()

plt.savefig(os.path.join(FIG_DIR, "methylation_pca.png"), dpi=300)
plt.close()

print("📊 PCA completed")
print("📁 Saved:")
print(" - results/pca_coordinates.csv")
print(" - results/figures/methylation_pca.png")
