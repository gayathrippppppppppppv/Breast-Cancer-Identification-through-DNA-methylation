import pandas as pd

# ==============================
# PATHS
# ==============================
GEO_MATRIX = "../dataset/GEO/GSE60185_series_matrix.txt"
PRED_PATH = "../results/geo_predictions.csv"
OUT_PATH = "../results/geo_phenotype_evaluation.csv"

# ==============================
# 1️⃣ EXTRACT GEO PHENOTYPES
# ==============================
print("📥 Reading GEO metadata...")

with open(GEO_MATRIX, "r") as f:
    lines = f.readlines()

# Extract GSM IDs
gsm_line = [l for l in lines if l.startswith("!Sample_geo_accession")][0]
gsm_ids = gsm_line.strip().split("\t")[1:]

# Extract phenotype lines
pheno_lines = [
    l for l in lines
    if l.startswith("!Sample_characteristics_ch1")
]

phenotypes = []

for i in range(len(gsm_ids)):
    combined = " ".join([p.split("\t")[i+1].lower() for p in pheno_lines])

    if "normal" in combined:
        phenotypes.append("Normal")
    elif "dcis" in combined:
        phenotypes.append("DCIS")
    elif "invasive" in combined or "carcinoma" in combined:
        phenotypes.append("Invasive")
    else:
        phenotypes.append("Unknown")

pheno_df = pd.DataFrame({
    "Sample": gsm_ids,
    "Phenotype": phenotypes
})

print("\n🧬 GEO Phenotype Counts")
print(pheno_df["Phenotype"].value_counts())

# ==============================
# 2️⃣ LOAD GEO PREDICTIONS
# ==============================
pred = pd.read_csv(PRED_PATH)

# ==============================
# 3️⃣ MERGE CORRECTLY (GSM IDs)
# ==============================
merged = pred.merge(pheno_df, on="Sample", how="inner")

print(f"\n🔗 Merged samples: {merged.shape[0]}")

# ==============================
# 4️⃣ PHENOTYPE VS PREDICTION
# ==============================
summary = pd.crosstab(
    merged["Phenotype"],
    merged["Prediction"],
    normalize="index"
) * 100

print("\n📊 Phenotype vs Prediction (%)")
print(summary.round(2))

# ==============================
# 5️⃣ SAVE OUTPUT
# ==============================
merged.to_csv(OUT_PATH, index=False)
print(f"\n💾 Saved evaluation to: {OUT_PATH}")
