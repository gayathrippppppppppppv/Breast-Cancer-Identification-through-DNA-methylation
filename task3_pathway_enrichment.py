import pandas as pd
import gseapy as gp

# ==============================
# Paths
# ==============================
ANNOT_PATH = "../results/task2_biological_annotation.csv"
OUT_PATH = "../results/task3_pathway_enrichment.csv"

# ==============================
# Load annotated CpGs
# ==============================
annot = pd.read_csv(ANNOT_PATH)
print("📄 Annotation loaded:", annot.shape)

# ==============================
# Extract gene list
# ==============================
genes = (
    annot["UCSC_RefGene_Name"]
    .dropna()
    .str.split(";")
    .explode()
    .unique()
)

genes = [g for g in genes if g != ""]
print("🧬 Unique genes:", len(genes))

# ==============================
# Run pathway enrichment (KEGG)
# ==============================
enr = gp.enrichr(
    gene_list=genes,
    gene_sets="KEGG_2021_Human",
    organism="Human",
    outdir=None
)

# ==============================
# Save results
# ==============================
results = enr.results.sort_values("Adjusted P-value")
results.to_csv(OUT_PATH, index=False)

print("✅ Pathway enrichment completed")
print("💾 Saved to:", OUT_PATH)

# ==============================
# Show top pathways
# ==============================
print("\n🔬 Top enriched pathways:")
print(results[["Term", "Adjusted P-value", "Genes"]].head(10))
