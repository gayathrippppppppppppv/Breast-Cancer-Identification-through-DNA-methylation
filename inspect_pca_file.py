import pandas as pd
import os

BASE_DIR = os.path.abspath("..")
RESULTS_DIR = os.path.join(BASE_DIR, "results")

PCA_PATH = os.path.join(RESULTS_DIR, "pca_coordinates.csv")

pca = pd.read_csv(PCA_PATH)

print("\n📊 PCA FILE COLUMNS:")
print(pca.columns.tolist())

print("\n📌 First 5 rows:")
print(pca.head())
