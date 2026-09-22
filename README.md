# HepaRG psychostimulant endometabolomics workflow — RP_POS

[![Validate repository](https://github.com/cargla/heparg-psychostimulant-metabolomics/actions/workflows/validate.yml/badge.svg)](https://github.com/cargla/heparg-psychostimulant-metabolomics/actions/workflows/validate.yml)

This repository contains the Python workflow used to preprocess and analyse the
intracellular untargeted LC-HRMS dataset acquired in reversed-phase positive
ionization mode (`RP_POS`) from differentiated HepaRG cells exposed to four
psychostimulants: methamphetamine, MDMA, 3-MMC, and α-PHP.

The repository provides the two analysis notebooks together with the RP_POS
input files, intermediate datasets, statistical result tables, and figures.
It is intended to make the complete RP_POS application understandable and
reproducible from the MZmine feature-table export onward.

## Scope

Only the `RP_POS` dataset is included in this repository. Data from the other
LC-HRMS acquisition modes used in the associated study are available from the
corresponding author upon reasonable request.

The file referred to here as “raw data” is the feature table exported from
MZmine. Vendor LC-HRMS files and converted mzXML files are not included.

## Repository structure

```text
.
├── notebooks/
│   ├── 01_preprocessing_rp_pos.ipynb
│   └── 02_statistical_analysis_rp_pos.ipynb
├── data/
│   ├── raw/
│   ├── metadata/
│   ├── databases/
│   └── processed/
└── outputs/
    ├── figures/
    └── tables/
```

### Main notebooks

`notebooks/01_preprocessing_rp_pos.ipynb` performs all preprocessing steps and creates the
numbered files stored in `data/processed/`.

`notebooks/02_statistical_analysis_rp_pos.ipynb` uses the final cleaned dataset produced by the first
notebook and creates the statistical tables and figures stored in `outputs/`.

The notebooks must therefore be run in this order:

1. `notebooks/01_preprocessing_rp_pos.ipynb`
2. `notebooks/02_statistical_analysis_rp_pos.ipynb`

## Input files

| File | Purpose |
| --- | --- |
| `data/raw/CELL_export_mzmine.csv` | RP_POS feature table exported from MZmine; starting point of the Python workflow |
| `data/metadata/CELL_injection_order.xlsx` | Sample identifiers, injection order, analytical batch, sample type, experimental condition, exposure time, dilution, and replicate |
| `data/databases/DTB_contaminants_exogenous_features.xlsx` | Internal list used to exclude contaminant and exogenous features |

The directory structure and filenames should be kept unchanged because the
notebooks use these relative paths directly.

## Notebook 1 — data preprocessing

`notebooks/01_preprocessing_rp_pos.ipynb` performs the following operations:

| Step | Operation | Main output |
| --- | --- | --- |
| 1 | Selection of one representative feature per MZmine correlation group | `01_CELL_representative_features.xlsx` |
| 2 | Removal of contaminant and exogenous features | `02_CELL_endogenous_features.xlsx` |
| 3 | Formatting of the sample-by-feature matrix and integration of sample metadata | `03_CELL_formatted_dataset.xlsx` |
| 4 | Removal of features with a zero mean in the reference pooled QC in at least one batch | `04_CELL_filter1_qc_mean_nonzero.xlsx` |
| 5 | Within-batch QC-RLSC signal-drift correction | `05_CELL_qcrlsc_corrected.xlsx` |
| 6 | Post-correction filtering using robust QC variability and dilution-series correlation | `06_CELL_filter2_qc_stability_filtered.xlsx` |
| 7 | Between-batch correction using reference pooled-QC medians | `07_CELL_interbatch_corrected.xlsx` |
| 8 | Removal of features with a zero median across cellular samples | `08_CELL_final_cleaned_dataset.xlsx` |
| 9 | PCA-based visualization of pooled-QC samples throughout preprocessing | `09_qc_pca_preprocessing_steps.xlsx` and associated PNG figure |

The supplied RP_POS workflow starts from 4,065 MZmine features and produces a
final cleaned matrix containing 212 samples and 1,313 features.

## Notebook 2 — statistical analysis

`notebooks/02_statistical_analysis_rp_pos.ipynb` performs:

- assessment of the solvent effect;
- blocked univariate analysis of the global psychostimulant response;
- ASCA+ modelling and restricted permutation testing;
- leave-one-experiment-out assessment of ASCA+ contributor stability;
- PLS-DA modelling, validation, permutation testing, and VIP stability;
- integration of candidates selected by the complementary methods;
- evaluation of cross-drug consistency at 1 and 24 hours.

The corresponding Excel workbooks are stored below
`outputs/tables/statistical_analysis/`. Generated figures are stored below
`outputs/figures/`.

## Python environment

The workflow was developed with Python 3.13.9 and the following package
versions:

| Package | Version |
| --- | ---: |
| NumPy | 2.3.5 |
| pandas | 2.3.3 |
| SciPy | 1.16.3 |
| statsmodels | 0.14.5 |
| scikit-learn | 1.7.2 |
| Matplotlib | 3.10.6 |
| seaborn | 0.13.2 |
| joblib | 1.5.2 |
| openpyxl | 3.1.5 |
| patsy | 1.0.1 |
| tqdm | 4.67.1 |
| ipykernel | 6.31.0 |
| nbclient | 0.10.2 |
| nbformat | 5.10.4 |

To recreate the original Conda environment:

```bash
conda env create -f environment.yml
conda activate heparg-psychostimulant-metabolomics
jupyter lab
```

Alternatively, the dependencies can be installed in an existing Python 3.13
environment with `python -m pip install -r requirements.txt`.

The notebooks should be opened from the repository root. Running them from
another working directory may prevent the relative paths from resolving
correctly.

## Included results

The processed Excel files, result tables, and PNG figures included in the
repository correspond to the supplied RP_POS application. They allow users to
inspect the successive processing stages without first rerunning the complete
workflow. Running the notebooks again will regenerate or replace these files.

## Repository validation

A lightweight automated check verifies the expected directory structure,
required inputs, notebook file format, and presence of result tables and
figures. It runs automatically on GitHub and can also be launched locally:

```bash
python scripts/validate_repository.py
```

## Data availability

The public-data boundary is described in [`DATA_AVAILABILITY.md`](DATA_AVAILABILITY.md).
In summary, the complete RP_POS application from the MZmine feature table onward
is included; the other acquisition modes are available upon reasonable request.

## Citation

GitHub displays the recommended software citation from [`CITATION.cff`](CITATION.cff).
The associated article citation can be added to this file after publication.

## Licence

The software is released under the [`MIT License`](LICENSE).
