import pandas as pd
from joblib import load
from sklearn.metrics import accuracy_score, roc_auc_score, classification_report

print("🚀 Starting external validation...")

# ==========================================
# 1️⃣ LOAD TRAINED MODEL
# ==========================================
print("📦 Loading trained SVM model...")
model = load(r"C:\Users\Shalini\Desktop\IBS2_PROJECT\results\svm_model.joblib")
print("✅ Model loaded")

# ==========================================
# 2️⃣ LOAD TRAINED CpG LIST
# ==========================================
print("📦 Loading training CpGs...")
selected_cpgs = set(
    pd.read_csv(
        r"C:\Users\Shalini\Desktop\IBS2_PROJECT\results\train_cpgs.csv",
        header=None
    )[0]
)
print(f"✅ {len(selected_cpgs)} CpGs loaded")

# ==========================================
# 3️⃣ LOAD META DATA
# ==========================================
print("📦 Loading meta data...")
meta = pd.read_csv(r"C:\GEO\GSE287331_meta.csv")

meta = meta[meta["Sample Region"].isin(["TU", "HDB"])].copy()
meta["Label"] = meta["Sample Region"].map({"TU": 1, "HDB": 0})

meta = meta.set_index("IDAT")
sample_ids = set(meta.index)

print("📊 Samples selected:", len(sample_ids))

# ==========================================
# 4️⃣ LOAD BETA FILE (ONLY REQUIRED COLUMNS)
# ==========================================
print("⚡ Reading header...")
header = pd.read_csv(
    r"C:\GEO\GSE287331_betas_processed.csv",
    nrows=0
)

all_columns = header.columns.tolist()

# Keep CpG column + relevant samples only
use_columns = [all_columns[0]] + [
    col for col in all_columns[1:] if col in sample_ids
]

print("⚡ Loading required columns only...")
betas = pd.read_csv(
    r"C:\GEO\GSE287331_betas_processed.csv",
    index_col=0,
    usecols=use_columns
)

print("⚡ Filtering to trained CpGs...")
betas_filtered = betas.loc[
    betas.index.intersection(selected_cpgs)
]

print("✅ CpGs matched:", betas_filtered.shape[0])

# ==========================================
# 5️⃣ MATCH SAMPLES
# ==========================================
common_samples = list(
    set(betas_filtered.columns).intersection(sample_ids)
)

betas_filtered = betas_filtered[common_samples]
meta = meta.loc[common_samples]

X_external = betas_filtered.T
y_external = meta["Label"]

print("📊 Final matrix shape:", X_external.shape)

# ==========================================
# 6️⃣ PREDICT
# ==========================================
print("🤖 Running predictions...")

pred = model.predict(X_external)
prob = model.predict_proba(X_external)[:, 1]

accuracy = accuracy_score(y_external, pred)
auc = roc_auc_score(y_external, prob)

print("\n==============================")
print("🧪 EXTERNAL VALIDATION RESULTS")
print("==============================")
print("Samples:", len(y_external))
print("Accuracy:", round(accuracy, 4))
print("AUC:", round(auc, 4))
print("\nClassification Report:\n")
print(classification_report(y_external, pred))

print("✅ Done.")
