import pandas as pd
import numpy as np
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler

# Load dataset
data = pd.read_csv("../results/methylation_ml_dataset.csv")

X = data.drop(columns=["sample", "label"])
y = data["label"]

# Scale
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train linear SVM
model = SVC(kernel="linear", class_weight="balanced")
model.fit(X_scaled, y)

# Feature importance
importance = np.abs(model.coef_[0])
features = X.columns

imp_df = pd.DataFrame({
    "CpG": features,
    "importance": importance
}).sort_values(by="importance", ascending=False)

# Save
imp_df.to_csv("../results/top_cpg_importance.csv", index=False)

print("✅ Feature importance extracted")
print(imp_df.head(10))
