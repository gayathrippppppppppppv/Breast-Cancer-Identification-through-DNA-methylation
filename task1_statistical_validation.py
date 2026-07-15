import pandas as pd
from scipy.stats import ttest_ind

# ==============================
# Load ML dataset
# ==============================
DATA_PATH = "../results/methylation_ml_dataset.csv"
data = pd.read_csv(DATA_PATH)

X = data.drop(columns=["label", "sample"], errors="ignore")
y = data["label"]

# ==============================
# Separate classes
# ==============================
cancer = X[y == "Cancer"]
normal = X[y == "Normal"]

results = []

for cpg in X.columns:
    t, p = ttest_ind(
        cancer[cpg],
        normal[cpg],
        nan_policy="omit"
    )

    results.append({
        "CpG": cpg,
        "Cancer_mean": cancer[cpg].mean(),
        "Normal_mean": normal[cpg].mean(),
        "Mean_diff": cancer[cpg].mean() - normal[cpg].mean(),
        "p_value": p
    })

df = pd.DataFrame(results)
df = df.sort_values("p_value")

# ==============================
# SAVE OUTPUT (THIS WAS MISSING)
# ==============================
OUTPUT_PATH = "../results/task1_statistical_validation.csv"
df.to_csv(OUTPUT_PATH, index=False)

print("✅ Statistical validation completed")
print("💾 Saved to:", OUTPUT_PATH)
print("\nTop significant CpGs:")
print(df.head(10))
