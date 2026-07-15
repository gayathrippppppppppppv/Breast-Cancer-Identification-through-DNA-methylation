import pandas as pd
import numpy as np
from joblib import load
from sklearn.metrics import classification_report, confusion_matrix

# ==============================
# Paths
# ==============================
GEO_PATH = "../dataset/GEO/GSE60185_series_matrix.txt"
MODEL_PATH = "../results/svm_model.joblib"
CPG_PATH = "../results/common_cpgs.csv"

# ==============================
# Load CpGs used by TCGA model
# ==============================
cpgs = pd.read_csv(CPG_PATH, header=None)[0].tolist()

# KEEP ONLY CpG probes
cpgs = [c for c in cpgs if c.startswith("cg")]

print(f"🧬 CpGs loaded: {len(cpgs)}")

# ==============================
# Load GEO methylation data
# ==============================
print("📥 Loading GEO data...")
geo_raw = pd.read_csv(
    GEO_PATH,
    sep="\t",
    comment="!",
    index_col=0
)

# Transpose → samples × CpGs
geo = geo_raw.T

# ==============================
# Align CpGs (INTERSECTION)
# ==============================
available_cpgs = list(set(cpgs) & set(geo.columns))
geo = geo[available_cpgs]

print(f"✅ GEO CpGs matched: {len(available_cpgs)}")

# ==============================
# Load trained SVM model
# ==============================
model = load(MODEL_PATH)
print("🤖 Model loaded")

# ==============================
# Predict GEO samples
# ==============================
predictions = model.predict(geo)

geo_results = pd.DataFrame({
    "Sample": geo.index,
    "Predicted_Label": predictions
})

# ==============================
# Extract Phenotype Labels
# ==============================
print("🧬 Extracting phenotype labels...")

meta = pd.read_csv(GEO_PATH, sep="\t", header=None)

phenotype_lines = meta[0].str.contains("disease state", case=False, na=False)
phenotypes = meta[phenotype_lines][0].values

labels = []
for p in phenotypes:
    if "normal" in p.lower():
        labels.append("Normal")
    else:
        labels.append("Cancer")

geo_results["True_Label"] = labels[:len(geo_results)]

# ==============================
# Evaluation
# ==============================
print("\n📊 CONFUSION MATRIX")
print(confusion_matrix(
    geo_results["True_Label"],
    geo_results["Predicted_Label"],
    labels=["Cancer", "Normal"]
))

print("\n📈 CLASSIFICATION REPORT")
print(classification_report(
    geo_results["True_Label"],
    geo_results["Predicted_Label"]
))

# ==============================
# Save results
# ==============================
geo_results.to_csv("../results/geo_validation_with_phenotype.csv", index=False)
print("💾 Validation results saved")
