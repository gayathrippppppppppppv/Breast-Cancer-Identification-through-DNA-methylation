import pandas as pd
from joblib import load
import numpy as np

print("🚀 Starting TNBC external validation...")

# ===============================
# 1️⃣ Load trained TCGA model
# ===============================
model = load(r"C:\Users\Shalini\Desktop\IBS2_PROJECT\results\svm_model.joblib")
print("✅ Model loaded")

# ===============================
# 2️⃣ Load trained CpGs (ORDER MATTERS)
# ===============================
train_cpgs = pd.read_csv(
    r"C:\Users\Shalini\Desktop\IBS2_PROJECT\results\train_cpgs.csv",
    header=None
)[0].tolist()

print("✅ Loaded", len(train_cpgs), "training CpGs")

# ===============================
# 3️⃣ Load EPIC V1
# ===============================
print("📦 Loading EPIC V1...")
v1 = pd.read_csv(
    r"C:\GEO\GSE290981_ProcessedData_LUepic_V1.txt",
    sep="\t",
    index_col=0
)

# Remove detection p-values
v1 = v1.loc[:, ~v1.columns.str.contains("Detection_Pval")]

# Clean CpG names
v1.index = v1.index.astype(str).str.split("_").str[0]

# Remove duplicate CpGs if any
v1 = v1[~v1.index.duplicated(keep="first")]

print("V1 shape:", v1.shape)

# ===============================
# 4️⃣ Load EPIC V2
# ===============================
print("📦 Loading EPIC V2...")
v2 = pd.read_csv(
    r"C:\GEO\GSE290981_ProcessedData_LUepic_V2_CpGnameChange.txt",
    sep="\t",
    index_col=0
)

v2 = v2.loc[:, ~v2.columns.str.contains("Detection_Pval")]

# Clean CpG names
v2.index = v2.index.astype(str).str.split("_").str[0]

# Remove duplicates
v2 = v2[~v2.index.duplicated(keep="first")]

print("V2 shape:", v2.shape)

# ===============================
# 5️⃣ Merge datasets
# ===============================
print("🔗 Finding common CpGs between V1 and V2...")

common_cpgs = v1.index.intersection(v2.index)
print("Common CpGs:", len(common_cpgs))

if len(common_cpgs) == 0:
    print("❌ No common CpGs between V1 and V2. Stop.")
    exit()

v1 = v1.loc[common_cpgs]
v2 = v2.loc[common_cpgs]

merged = pd.concat([v1, v2], axis=1)
print("Merged shape:", merged.shape)

# ===============================
# 6️⃣ Keep only training CpGs
# ===============================
print("🎯 Filtering to training CpGs...")

matched_cpgs = [cpg for cpg in train_cpgs if cpg in merged.index]

print("Matched training CpGs:", len(matched_cpgs))

if len(matched_cpgs) == 0:
    print("❌ No CpGs matched training model. Stop.")
    exit()

merged = merged.loc[matched_cpgs]

# ===============================
# 7️⃣ Transpose and align feature order
# ===============================
X_external = merged.T

# Ensure exact same column order as training
X_external = X_external[matched_cpgs]

print("Final matrix shape:", X_external.shape)

# ===============================
# 8️⃣ Predict
# ===============================
print("🤖 Predicting...")

pred = model.predict(X_external)
prob = model.predict_proba(X_external)[:, 1]

tumor_rate = np.mean(pred)

print("\n==============================")
print("🧪 TNBC EXTERNAL VALIDATION")
print("==============================")
print("Total samples:", len(pred))
print("Predicted Tumor (%):", round(tumor_rate * 100, 2), "%")
print("Mean Tumor Probability:", round(np.mean(prob), 4))
print("==============================")

print("✅ Done.")
