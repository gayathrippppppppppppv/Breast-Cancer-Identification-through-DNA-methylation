import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    accuracy_score,
    roc_auc_score,
    roc_curve,
    confusion_matrix,
    precision_recall_curve
)

print("🚀 Generating Advanced Subtype Visualizations\n")

# ==============================
# Load methylation
# ==============================

meth = pd.read_csv(
    r"C:\Users\Shalini\Desktop\IBS2_PROJECT\dataset\methylation_cleaned.csv",
    index_col=0
)

meth = meth.T

train_cpgs = pd.read_csv(
    r"C:\Users\Shalini\Desktop\IBS2_PROJECT\results\train_cpgs.csv",
    header=None
)[0].tolist()

meth = meth[train_cpgs]

# ==============================
# Load clinical
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

meth["sample"] = meth.index
merged = meth.merge(clinical, on="sample")


def assign_subtype(row):
    if row["ER"] == "Negative" and row["PR"] == "Negative" and row["HER2"] == "Negative":
        return "Basal"
    elif row["ER"] == "Positive" and row["HER2"] == "Negative":
        return "Luminal"
    else:
        return "Other"


merged["Subtype"] = merged.apply(assign_subtype, axis=1)

subset = merged[merged["Subtype"].isin(["Basal", "Luminal"])].copy()
subset["label"] = subset["Subtype"].apply(lambda x: 1 if x == "Basal" else 0)

X = subset[train_cpgs].fillna(subset[train_cpgs].mean())
y = subset["label"]

# ==============================
# Model
# ==============================

pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("svm", SVC(kernel="linear", probability=True, class_weight="balanced"))
])

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

y_pred = cross_val_predict(pipeline, X, y, cv=cv)
y_prob = cross_val_predict(pipeline, X, y, cv=cv, method="predict_proba")[:, 1]

# ==============================
# 1️⃣ Confusion Matrix Heatmap
# ==============================

cm = confusion_matrix(y, y_pred)

plt.figure(figsize=(5, 4))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
            xticklabels=["Luminal", "Basal"],
            yticklabels=["Luminal", "Basal"])
plt.title("Confusion Matrix (Basal vs Luminal)")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.tight_layout()
plt.show()

# ==============================
# 2️⃣ ROC Curve
# ==============================

fpr, tpr, _ = roc_curve(y, y_prob)
auc = roc_auc_score(y, y_prob)

plt.figure(figsize=(5, 4))
plt.plot(fpr, tpr, label=f"AUC = {auc:.3f}")
plt.plot([0, 1], [0, 1], linestyle="--")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("Cross-Validated ROC")
plt.legend()
plt.tight_layout()
plt.show()

# ==============================
# 3️⃣ Precision-Recall Curve
# ==============================

precision, recall, _ = precision_recall_curve(y, y_prob)

plt.figure(figsize=(5, 4))
plt.plot(recall, precision)
plt.xlabel("Recall")
plt.ylabel("Precision")
plt.title("Precision-Recall Curve")
plt.tight_layout()
plt.show()

# ==============================
# 4️⃣ Probability Distribution
# ==============================

plt.figure(figsize=(6, 4))
sns.histplot(y_prob[y == 1], color="red", label="Basal", kde=True)
sns.histplot(y_prob[y == 0], color="blue", label="Luminal", kde=True)
plt.legend()
plt.title("Predicted Probability Distribution")
plt.xlabel("Predicted Basal Probability")
plt.tight_layout()
plt.show()

# ==============================
# 5️⃣ Feature Importance
# ==============================

pipeline.fit(X, y)
coef = pipeline.named_steps["svm"].coef_[0]

feature_importance = pd.DataFrame({
    "CpG": train_cpgs,
    "Weight": coef
}).sort_values("Weight", key=abs, ascending=False).head(15)

plt.figure(figsize=(6, 5))
sns.barplot(x="Weight", y="CpG", data=feature_importance)
plt.title("Top 15 CpGs Driving Subtype Separation")
plt.tight_layout()
plt.show()

print("\n🔥 Visualizations Complete")
