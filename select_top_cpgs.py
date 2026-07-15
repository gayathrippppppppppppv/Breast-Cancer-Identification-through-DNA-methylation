import pandas as pd
import numpy as np

meth = pd.read_csv("../results/methylation_cleaned.csv", index_col=0)

# Variance across samples
variances = meth.var(axis=1)

top_cpgs = variances.sort_values(ascending=False).head(200).index

meth_top = meth.loc[top_cpgs]

meth_top.to_csv("../results/methylation_top200.csv")

print("✅ Selected top 200 CpGs")
