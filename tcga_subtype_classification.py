import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    accuracy_score,
    roc_auc_score,
    roc_curve,
    confusion_matrix,
    classification_report
)

print("🚀 FINAL TCGA Subtype Validation (Basal vs Luminal)\n")

# ==============================
# 1️⃣ Load methylation
# ==============================

meth = pd.read_csv(
    r"C:\Users\Shalini\Desktop\IBS2_PROJECT\dataset\methylation_cleaned.csv",
    index_col=0
)

meth = meth.T

# ==============================
# 2️⃣ Use top CpGs
# ==============================

train_cpgs = pd.read_csv(
    r"C:\Users\Shalini\Desktop\IBS2_PROJECT\results\train_cpgs.csv",
    header=None
)[0].tolist()

meth = meth[train_cpgs]

# ==============================
# 3️⃣ Load clinical
# ==============================

clinical = pd.read_csv(
    r"C:\Users\Shalini\Downloads\brca_tcga_clinical_data.tsv",
    sep="\t"
)

clinical = clinical[[
    "Sample ID",
    "ER Status By IHC",
    "PR status by ihc",
    "HER2 fish status"
]].copy()

clinical.columns = ["sample", "ER", "PR", "HER2"]

# ==============================
# 4️⃣ Merge
# ==============================

meth["sample"] = meth.index
merged = meth.merge(clinical, on="sample")

# ==============================
# 5️⃣ Assign subtype
# ==============================


def assign_subtype(row):
    if row["ER"] == "Negative" and row["PR"] == "Negative" and row["HER2"] == "Negative":
        return "Basal"
    elif row["ER"] == "Positive" and row["HER2"] == "Negative":
        return "Luminal_A"
    elif row["ER"] == "Positive" and row["HER2"] == "Positive":
        return "Luminal_B"
    else:
        return "Other"


merged["Subtype"] = merged.apply(assign_subtype, axis=1)

subset = merged[merged["Subtype"].isin(
    ["Basal", "Luminal_A", "Luminal_B"])].copy()

subset["label"] = subset["Subtype"].apply(
    lambda x: 1 if x == "Basal" else 0
)

print("Class balance:")
print(subset["label"].value_counts())

# ==============================
# 6️⃣ Prepare data
# ==============================

X = subset[train_cpgs].fillna(subset[train_cpgs].mean())
y = subset["label"]

# ==============================
# 7️⃣ Pipeline
# ==============================

pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("svm", SVC(kernel="linear", probability=True))
])

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

# ==============================
# 8️⃣ Cross-validated predictions
# ==============================

y_pred = cross_val_predict(pipeline, X, y, cv=cv)
y_prob = cross_val_predict(pipeline, X, y, cv=cv, method="predict_proba")[:, 1]

# ==============================
# 9️⃣ Metrics
# ==============================

accuracy = accuracy_score(y, y_pred)
auc = roc_auc_score(y, y_prob)

print("\nCross-Validated Performance")
print("Accuracy:", round(accuracy, 4))
print("ROC AUC :", round(auc, 4))

print("\nClassification Report:")
print(classification_report(y, y_pred))

# ==============================
# 🔟 Confusion Matrix
# ==============================

cm = confusion_matrix(y, y_pred)

tn, fp, fn, tp = cm.ravel()

print("Confusion Matrix:")
print(cm)

basal_sensitivity = tp / (tp + fn)
print("\nBasal Sensitivity (Recall):", round(basal_sensitivity, 4))

# ==============================
# 📊 Cross-Validated ROC Curve
# ==============================

fpr, tpr, _ = roc_curve(y, y_prob)

plt.figure(figsize=(6, 5))
plt.plot(fpr, tpr, label=f"AUC = {auc:.3f}")
plt.plot([0, 1], [0, 1], linestyle="--")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("Cross-Validated ROC (Basal vs Luminal)")
plt.legend()
plt.tight_layout()
plt.show()

print("\n🔥 Final Clinical Validation Complete")
