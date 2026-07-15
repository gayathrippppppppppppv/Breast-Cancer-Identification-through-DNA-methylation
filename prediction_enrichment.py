import pandas as pd

# ==============================
# Paths
# ==============================
TCGA_PATH = "../results/tcga_test_predictions.csv"
GEO_PATH = "../results/geo_predictions.csv"

# ==============================
# Load predictions
# ==============================
tcga = pd.read_csv(TCGA_PATH)
geo = pd.read_csv(GEO_PATH)

print("📄 TCGA columns:", tcga.columns.tolist())
print("📄 GEO columns:", geo.columns.tolist())

# ==============================
# TCGA Prediction Distribution
# ==============================
tcga_counts = (
    tcga["Predicted_Label"]
    .value_counts(normalize=True)
    * 100
)

# ==============================
# GEO Prediction Distribution
# ==============================
geo_counts = (
    geo["Prediction"]
    .value_counts(normalize=True)
    * 100
)

# ==============================
# Combine results
# ==============================
enrichment = pd.DataFrame({
    "TCGA (%)": tcga_counts,
    "GEO (%)": geo_counts
}).fillna(0)

print("\n📊 Prediction Enrichment Comparison (%)")
print(enrichment)

# ==============================
# Save results
# ==============================
enrichment.to_csv("../results/prediction_enrichment.csv")
print("💾 Saved → prediction_enrichment.csv")
