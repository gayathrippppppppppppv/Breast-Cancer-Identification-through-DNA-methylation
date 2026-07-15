import os
import pandas as pd
import numpy as np

# =============================
# Paths (FILES, not folders)
# =============================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

METH_FILE = os.path.join(
    BASE_DIR,
    "dataset",
    "methylation_450k"
)

RESULTS_DIR = os.path.join(BASE_DIR, "results")
os.makedirs(RESULTS_DIR, exist_ok=True)

# =============================
# Load methylation file
# =============================
meth = pd.read_csv(METH_FILE, sep="\t", index_col=0)
print(f"✅ Loaded methylation data: {meth.shape}")

# =============================
# Step 1: Remove CpGs with >20% missing values
# =============================
missing_frac = meth.isna().mean(axis=1)
meth = meth.loc[missing_frac <= 0.20]
print(f"🧹 After CpG missing-value filter: {meth.shape}")

# =============================
# Step 2: Impute remaining NaNs (row median)
# =============================
meth = meth.apply(lambda row: row.fillna(row.median()), axis=1)
print("🧬 Missing values imputed using CpG-wise median")

# =============================
# Step 3: Variance filtering (top 25%)
# =============================
variances = meth.var(axis=1)
threshold = variances.quantile(0.75)
meth = meth.loc[variances >= threshold]
print(f"📉 After variance filtering: {meth.shape}")

# =============================
# Save cleaned methylation
# =============================
OUT_PATH = os.path.join(RESULTS_DIR, "methylation_cleaned.csv")
meth.to_csv(OUT_PATH)

print("✅ Cleaned methylation saved to:")
print(OUT_PATH)
