import pandas as pd
import numpy as np
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from joblib import dump

print("🚀 STARTING HARMONIZED TCGA → TNBC PIPELINE")

# ======================================================
# 1️⃣ LOAD TCGA DATA
# ======================================================
print("\n📦 Loading TCGA dataset...")
tcga = pd.read_csv(
    r"C:\Users\Shalini\Desktop\IBS2_PROJECT\results\methylation_ml_dataset.csv"
)

tcga_cpgs = list(set(tcga.columns) - {"label", "sample"})
print("TCGA CpGs:", len(tcga_cpgs))

# ======================================================
# 2️⃣ LOAD GSE290981 (V1 + V2)
# ======================================================
print("\n📦 Loading GSE290981 V1...")
v1 = pd.read_csv(
    r"C:\GEO\GSE290981_ProcessedData_LUepic_V1.txt",
    sep="\t",
    index_col=0
)

v1 = v1.loc[:, ~v1.columns.str.contains("Detection_Pval")]
v1.index = v1.index.astype(str).str.split("_").str[0]
print("V1 shape:", v1.shape)

print("\n📦 Loading GSE290981 V2...")
v2 = pd.read_csv(
    r"C:\GEO\GSE290981_ProcessedData_LUepic_V2_CpGnameChange.txt",
    sep="\t",
    index_col=0
)

v2 = v2.loc[:, ~v2.columns.str.contains("Detection_Pval")]
v2.index = v2.index.astype(str).str.split("_").str[0]
print("V2 shape:", v2.shape)

# ======================================================
# 3️⃣ FIND COMMON CpGs
# ======================================================
print("\n🔎 Finding common CpGs...")
gse_cpgs = set(v1.index).intersection(set(v2.index))
common_cpgs = list(set(tcga_cpgs).intersection(gse_cpgs))

print("Common CpGs between TCGA and GSE:", len(common_cpgs))

if len(common_cpgs) == 0:
    raise ValueError("❌ No overlapping CpGs found!")

# ======================================================
# 4️⃣ RETRAIN SVM USING COMMON CpGs
# ======================================================
print("\n🤖 Retraining SVM on harmonized CpGs...")

X = tcga[common_cpgs]
y = tcga["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    stratify=y,
    random_state=42
)

model = SVC(kernel="linear", probability=True)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print("\n✅ TCGA INTERNAL PERFORMANCE")
print(classification_report(y_test, y_pred))

dump(
    model,
    r"C:\Users\Shalini\Desktop\IBS2_PROJECT\results\svm_model_harmonized.joblib"
)
print("💾 Saved harmonized SVM model")

# ======================================================
# 5️⃣ MERGE GSE V1 + V2
# ======================================================
print("\n🔗 Merging V1 + V2...")

common_gse = v1.index.intersection(v2.index)
merged = pd.concat(
    [v1.loc[common_gse], v2.loc[common_gse]],
    axis=1
)

print("Merged shape:", merged.shape)

# Keep only harmonized CpGs
merged = merged.loc[common_cpgs]

# Transpose for prediction
X_external = merged.T
print("Final external matrix shape:", X_external.shape)

# ======================================================
# 6️⃣ EXTERNAL VALIDATION
# ======================================================
print("\n🧪 Running TNBC external validation...")

pred = model.predict(X_external)
prob = model.predict_proba(X_external)

# Convert predictions to numeric (Cancer = 1)
pred_numeric = (pred == "Cancer").astype(int)

tumor_rate = np.mean(pred_numeric)

# Find probability column for "Cancer"
cancer_index = list(model.classes_).index("Cancer")
mean_prob = np.mean(prob[:, cancer_index])

print("\n==============================")
print("🧬 TNBC EXTERNAL VALIDATION")
print("==============================")
print("Total TNBC samples:", len(pred))
print("Predicted Tumor (%):", round(tumor_rate * 100, 2))
print("Mean Tumor Probability:", round(mean_prob, 4))
print("==============================")

print("\n🔥 PIPELINE COMPLETE")
