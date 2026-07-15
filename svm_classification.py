import pandas as pd
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from joblib import dump

# ==============================
# Load TCGA ML dataset
# ==============================
DATA_PATH = "../results/methylation_ml_dataset.csv"
data = pd.read_csv(DATA_PATH)

X = data.drop(columns=["label", "sample"], errors="ignore")
y = data["label"]

print("📄 Loaded dataset:", X.shape)

# ==============================
# Train-test split
# ==============================
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    stratify=y,
    random_state=42
)

# ==============================
# Train SVM (THIS *IS* THE SVM)
# ==============================
model = SVC(kernel="linear", probability=True)
model.fit(X_train, y_train)

# ==============================
# Save trained model
# ==============================
dump(model, "../results/svm_model.joblib")
print("💾 SVM model saved")

# ==============================
# Save CpGs used during training
# ==============================
pd.Series(X.columns).to_csv(
    "../results/train_cpgs.csv",
    index=False,
    header=False
)
print(f"💾 CpG list saved: {len(X.columns)} CpGs")

# ==============================
# Evaluate on TCGA test set
# ==============================
y_pred = model.predict(X_test)

print("\n✅ Classification Report")
print(classification_report(y_test, y_pred))

# ==============================
# SAVE TCGA TEST PREDICTIONS (CRITICAL)
# ==============================
tcga_test_predictions = pd.DataFrame({
    "Sample_Index": X_test.index,
    "True_Label": y_test.values,
    "Predicted_Label": y_pred
})

tcga_test_predictions.to_csv(
    "../results/tcga_test_predictions.csv",
    index=False
)

print("💾 Saved TCGA test predictions → tcga_test_predictions.csv")
