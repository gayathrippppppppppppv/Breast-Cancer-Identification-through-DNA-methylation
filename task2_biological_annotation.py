import pandas as pd

# ==============================
# Paths
# ==============================
SIG_CPG_PATH = "../results/task1_statistical_validation.csv"
ANNOT_PATH = "../dataset/GEO/humanmethylation450_15017482_v1-2.csv"
OUT_PATH = "../results/task2_biological_annotation.csv"

# ==============================
# Load significant CpGs
# ==============================
sig = pd.read_csv(SIG_CPG_PATH)
print(f"🧬 Significant CpGs loaded: {sig.shape}")

# ==============================
# Load Illumina 450K annotation
# IMPORTANT: skip metadata rows
# ==============================
annot = pd.read_csv(
    ANNOT_PATH,
    skiprows=7,          # <-- THIS IS THE FIX
    low_memory=False
)

print(f"📄 Annotation table loaded: {annot.shape}")

# ==============================
# Keep only useful columns
# ==============================
annot = annot[[
    "IlmnID",
    "UCSC_RefGene_Name",
    "UCSC_RefGene_Group",
    "Relation_to_UCSC_CpG_Island"
]]

annot.rename(columns={"IlmnID": "CpG"}, inplace=True)

# ==============================
# Merge CpGs with annotation
# ==============================
merged = sig.merge(annot, on="CpG", how="left")

# ==============================
# Save output
# ==============================
merged.to_csv(OUT_PATH, index=False)

print("✅ Biological annotation completed")
print("💾 Saved to:", OUT_PATH)

print("\nTop annotated CpGs:")
print(merged.head(10))
