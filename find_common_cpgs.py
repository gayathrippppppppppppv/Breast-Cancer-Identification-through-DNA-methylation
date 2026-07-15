import pandas as pd

# Load TCGA CpGs
tcga = pd.read_csv("../results/methylation_top200.csv")
tcga_cpgs = set(tcga.columns[1:])

# Load GEO data (just CpG names)
geo = pd.read_csv(
    "../dataset/GEO/GSE60185_series_matrix.txt",
    sep="\t",
    comment="!",
    index_col=0
)
geo_cpgs = set(geo.index)

# Intersection
common = sorted(tcga_cpgs.intersection(geo_cpgs))

print(f"✅ Common CpGs found: {len(common)}")

pd.DataFrame(common, columns=["CpG"]).to_csv(
    "../results/common_cpgs.csv",
    index=False
)
