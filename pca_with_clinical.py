import pandas as pd
import os

# ---------------- Base paths ----------------
BASE_DIR = os.path.abspath("..")

PCA_PATH = os.path.join(BASE_DIR, "results", "pca_coordinates.csv")
CLINICAL_PATH = os.path.join(BASE_DIR, "dataset", "clinical")

# ---------------- Load PCA ----------------
pca = pd.read_csv(PCA_PATH)
print("✅ Loaded PCA:", pca.shape)

# Fix index column
pca = pca.rename(columns={"Unnamed: 0": "sample_id"})
pca["patient_id"] = pca["sample_id"].str[:12]

# ---------------- Load clinical ----------------
clinical = pd.read_csv(CLINICAL_PATH, sep="\t")
print("✅ Loaded clinical:", clinical.shape)

clinical["patient_id"] = clinical["sampleID"].str[:12]

# ---------------- Merge ----------------
merged = pd.merge(
    pca,
    clinical,
    on="patient_id",
    how="inner"
)

print("🔗 Merged PCA + clinical:", merged.shape)

# ---------------- Save ----------------
OUT_PATH = os.path.join(BASE_DIR, "results", "pca_with_clinical.csv")
merged.to_csv(OUT_PATH, index=False)

print("📁 Saved merged file to:")
print(OUT_PATH)
