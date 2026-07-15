import pandas as pd

# ===============================
# FILE PATHS (HARD-CODED, SAFE)
# ===============================
CLINICAL_PATH = r"C:\Users\Shalini\Desktop\IBS2_PROJECT\dataset\clinical"
METHYLATION_PATH = r"C:\Users\Shalini\Desktop\IBS2_PROJECT\dataset\methylation_450k"

# ===============================
# LOAD CLINICAL DATA
# ===============================
clinical = pd.read_csv(CLINICAL_PATH, sep="\t")
print("✅ Clinical data loaded")
print("Clinical shape:", clinical.shape)
print(clinical.head())

# ===============================
# LOAD METHYLATION DATA
# ===============================
methylation = pd.read_csv(METHYLATION_PATH, sep="\t")
print("\n✅ Methylation data loaded")
print("Methylation shape:", methylation.shape)
print(methylation.iloc[:5, :5])

# ===============================
# CLEAN SAMPLE IDS
# ===============================
methylation.columns = methylation.columns.str.replace(".", "-", regex=False)
clinical["sampleID"] = clinical["sampleID"].str.slice(0, 15)

# ===============================
# MATCH SAMPLES
# ===============================
common_samples = set(methylation.columns[1:]).intersection(
    set(clinical["sampleID"]))
print("\n🔗 Matched samples:", len(common_samples))

# ===============================
# FILTER DATA
# ===============================
methylation_filtered = methylation[["sample"] + list(common_samples)]
clinical_filtered = clinical[clinical["sampleID"].isin(common_samples)]

print("\n🎯 Final shapes:")
print("Methylation:", methylation_filtered.shape)
print("Clinical:", clinical_filtered.shape)
