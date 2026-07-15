import pandas as pd

print("🔎 Finding common CpGs between TCGA and GSE290981...")

# Load TCGA ML dataset
tcga = pd.read_csv(
    r"C:\Users\Shalini\Desktop\IBS2_PROJECT\results\methylation_ml_dataset.csv"
)

tcga_cpgs = set(tcga.columns) - {"label", "sample"}

print("TCGA CpGs:", len(tcga_cpgs))

# Load V1
v1 = pd.read_csv(
    r"C:\GEO\GSE290981_ProcessedData_LUepic_V1.txt",
    sep="\t",
    index_col=0
)

v1 = v1.loc[:, ~v1.columns.str.contains("Detection_Pval")]
v1.index = v1.index.astype(str).str.split("_").str[0]

# Load V2
v2 = pd.read_csv(
    r"C:\GEO\GSE290981_ProcessedData_LUepic_V2_CpGnameChange.txt",
    sep="\t",
    index_col=0
)

v2 = v2.loc[:, ~v2.columns.str.contains("Detection_Pval")]
v2.index = v2.index.astype(str).str.split("_").str[0]

# Find common CpGs in GSE
gse_cpgs = set(v1.index).intersection(set(v2.index))

print("GSE CpGs:", len(gse_cpgs))

# Find overlap with TCGA
common_cpgs = list(tcga_cpgs.intersection(gse_cpgs))

print("Common CpGs:", len(common_cpgs))

# Save list
pd.Series(common_cpgs).to_csv(
    r"C:\Users\Shalini\Desktop\IBS2_PROJECT\results\common_cpgs_tcga_gse290981.csv",
    index=False,
    header=False
)

print("💾 Saved common CpGs list")
