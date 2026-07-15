import pandas as pd
from joblib import load

# ==============================
# Paths
# ==============================
GEO_PATH = "../dataset/GEO/GSE60185_series_matrix.txt"
MODEL_PATH = "../results/svm_model.joblib"
CPG_PATH = "../results/train_cpgs.csv"

# ==============================
# Load GEO
# ==============================
print("📥 Loading GEO data...")
geo_raw = pd.read_csv(
    GEO_PATH,
    sep="\t",
    comment="!",
    index_col=0
)

print("Raw GEO shape:", geo_raw.shape)

# ==============================
# Transpose → samples × CpGs
# ==============================
geo = geo_raw.T
geo = geo.loc[:, geo.columns.str.startswith("cg")]
geo = geo.apply(pd.to_numeric, errors="coerce")

# ==============================
# Load training CpGs
# ==============================
train_cpgs = pd.read_csv(CPG_PATH, header=None)[0].tolist()
print("🧬 CpGs expected:", len(train_cpgs))

# ==============================
# ALIGN FEATURES (THIS IS THE FIX)
# ==============================
geo = geo.reindex(columns=train_cpgs, fill_value=0)
print("✅ GEO aligned shape:", geo.shape)

# ==============================
# Load model & predict
# ==============================
model = load(MODEL_PATH)
predictions = model.predict(geo)

# ==============================
# Save output
# ==============================
out = pd.DataFrame({
    "Sample": geo.index,
    "Prediction": predictions
})

out.to_csv("../results/geo_predictions.csv", index=False)

print("\n📊 GEO Prediction Counts")
print(out["Prediction"].value_counts())
print("💾 Saved: geo_predictions.csv")
