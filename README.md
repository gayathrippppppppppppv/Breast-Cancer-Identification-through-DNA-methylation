
# Breast-Cancer-Identification-through-DNA-methylation

Table of Content

#  Table of Contents
- [Abstract](#Abstract)
- [Introduction](#Introduction)
- [Base / Reference Paper(s)](#basereference-papers)
- [Dataset overview](#dataset-overview)
- [Dataset link](#dataset-link)
- [Code](#code)
- [PPT](#ppt)

---

# Abstract
Breast cancer exhibits substantial molecular heterogeneity, with subtypes such as Basal and Luminal showing distinct biological behavior and clinical outcomes. Although DNA methylation is known to play a critical role in tumor development, its utility as a robust and clinically relevant biomarker remains incompletely validated.
While large-scale methylation datasets are publicly available, there is a need for systematic evaluation of methylation-based classification models, assessment of their generalizability across independent cohorts, and investigation of their ability to capture clinically meaningful subtype differences.
This study addresses these aspects using integrative analysis of TCGA and independent GEO datasets.

---

# Introduction
Breast cancer is one of the most common malignancies worldwide and is characterized by significant molecular and clinical heterogeneity. Tumors are classified into subtypes such as Basal-like and Luminal based on receptor status and gene expression patterns, which influence prognosis and treatment decisions.
In addition to genetic alterations, epigenetic changes—particularly DNA methylation—play a critical role in cancer development. Aberrant methylation of CpG sites can lead to altered gene regulation, contributing to tumor initiation and progression.
Advances in large-scale projects such as TCGA have generated genome-wide methylation datasets, enabling computational approaches to explore the diagnostic and clinical relevance of methylation patterns.

---
# Base / Reference Paper(s)

<img width="269" height="241" alt="image" src="https://github.com/user-attachments/assets/984752c2-d622-4746-86bf-1377016d750b" />

---

# Dataset overview
TCGA BRCA Dataset\
888 methylation samples\
Illumina 450K platform\
Tumor and normal tissues\
Clinical annotation available\
GEO GSE290981 (2025 Cohort)\
136 TNBC tumor samples\
Illumina EPIC platform\
Independent external validation dataset\
Clinical Subtype Information\
Subtype assignment based on:\
ER status\
PR status\
HER2 status\
Basal = ER-, PR-, HER2-Luminal = ER+ (HER2 variable)

---
# Dataset link
https://pmc.ncbi.nlm.nih.gov/search/?term=dataset
---
# Code
[svm_classification.py](https://github.com/user-attachments/files/30032969/svm_classification.py)\
[prediction_enrichment.py](https://github.com/user-attachments/files/30032968/prediction_enrichment.py)\
[pca_with_clinical.py](https://github.com/user-attachments/files/30032967/pca_with_clinical.py)\
[methylation_preprocessing.py](https://github.com/user-attachments/files/30032966/methylation_preprocessing.py)\
[methylation_pca.py](https://github.com/user-attachments/files/30032965/methylation_pca.py)\
[heatmap.py](https://github.com/user-attachments/files/30032964/heatmap.py)\
[geo_extract_and_evaluate.py](https://github.com/user-attachments/files/30032963/geo_extract_and_evaluate.py)\
[find_common_cpgs_tcga_gse290981.py](https://github.com/user-attachments/files/30032962/find_common_cpgs_tcga_gse290981.py)\
[find_common_cpgs.py](https://github.com/user-attachments/files/30032961/find_common_cpgs.py)\
[methylation_preprocessing.py](https://github.com/user-attachments/files/30032922/methylation_preprocessing.py)\
[brca_methylation_pipeline.py](https://github.com/user-attachments/files/30032921/brca_methylation_pipeline.py)\
[validate_gse290981_external.py](https://github.com/user-attachments/files/30032919/validate_gse290981_external.py)\
[validate_gse287331_external.py](https://github.com/user-attachments/files/30032918/validate_gse287331_external.py)\
[validate_geo_with_phenotype.py](https://github.com/user-attachments/files/30032917/validate_geo_with_phenotype.py)\
[validate_geo_on_tcga_model.py](https://github.com/user-attachments/files/30032915/validate_geo_on_tcga_model.py)\
[tcga_subtype_visual.py](https://github.com/user-attachments/files/30032914/tcga_subtype_visual.py)\
[tcga_subtype_classification.py](https://github.com/user-attachments/files/30032913/tcga_subtype_classification.py)\
[tcga_clinical_methylation_analysis.py](https://github.com/user-attachments/files/30032911/tcga_clinical_methylation_analysis.py)

# PPT
[IBS ppt.pptx](https://github.com/user-attachments/files/30033102/IBS.ppt.pptx)

