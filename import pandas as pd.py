import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler

# Load data
X = pd.read_csv("../results/methylation_top200.csv", index_col=0).T
labels = pd.read_csv("../results/sample_labels.csv")

# Merge
data = X.merge(labels, left_index=True, right_on="sample")
data = data.drop(columns=["sample"])

y = data["label"]
X = data.drop(columns=["label"])

# Scale
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)

# Train SVM
model = SVC(kernel="linear")
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

print("✅ SVM Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))
