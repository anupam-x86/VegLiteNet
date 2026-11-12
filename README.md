# VegLiteNet

### A Lightweight Lesion-Aware Frequency-Spatial Network for Vegetable Leaf Disease Detection

VegLiteNet is a research project exploring a lightweight deep learning architecture for vegetable leaf disease classification.

The project investigates three complementary approaches to disease feature extraction:

- **Spatial Features:** Lightweight depthwise and partial convolutions for capturing visual patterns in leaf images.
- **Frequency Features:** Wavelet-based analysis to explore high-frequency texture details associated with disease symptoms.
- **Lesion-Aware Attention:** An attention mechanism to emphasize potentially disease-relevant regions of leaf images.

The objective is to investigate whether combining these approaches can improve disease feature representation while maintaining computational efficiency.

> **Project Status:** Work in progress — currently focused on dataset preparation and verification.

## Research Objectives

- Develop a lightweight architecture for vegetable leaf disease classification.
- Investigate the contribution of spatial, frequency-domain, and attention-based components.
- Conduct ablation studies to understand individual component contributions.
- Compare against established lightweight CNN architectures.
- Explore generalization to unseen field images.

## Dataset

**[Tomato Leaf Disease Detection](https://www.kaggle.com/datasets/kaustubhb999/tomatoleaf)**

| Property       | Details              |
| -------------- | -------------------- |
| Source         | Kaggle               |
| Dataset author | kaustubhb999         |
| License        | CC0 1.0              |
| Classes        | 10                   |
| Images         | Approximately 11,000 |

**Dataset setup:**

1. Download the dataset from Kaggle.
2. Extract it into `data/raw/tomato/`.
3. Preserve the original `train/` and `val/` directory structure.

Dataset files are not included in this repository. Integrity and duplicate analysis are ongoing. Potentially related or augmented images will be checked to reduce data leakage between splits.

## Project Structure

```text
VegLiteNet/
├── data/
│   ├── raw/
│   │   └── tomato/                  # Original dataset [available]
│   │       ├── train/
│   │       └── val/
│   ├── train/                       # Prepared training split [planned]
│   ├── val/                         # Prepared validation split [planned]
│   └── test/                        # Prepared test split [planned]
│
├── src/
│   └── __init__.py                  # Source package
│
├── models/
│   ├── baseline.py                  # Baseline CNN [planned]
│   └── veglitenet.py                # Proposed architecture [planned]
│
├── notebooks/
│   ├── 01_dataset.ipynb             # Dataset inspection [in progress]
│   ├── 02_baseline.ipynb            # Baseline experiments [planned]
│   ├── 03_laf_block.ipynb           # LAF block development [planned]
│   ├── 04_training.ipynb            # Model training [planned]
│   └── 05_evaluation.ipynb          # Model evaluation [planned]
│
├── results/
│   ├── figures/                     # Experimental visualizations
│   └── tables/                      # Experimental results
│
├── requirements.txt
├── README.md
└── .gitignore
```

**Status legend:**

- `available` — resource or data already present.
- `implemented` — functionality implemented.
- `in progress` — currently being developed.
- `planned` — not yet implemented.

## Setup

**Prerequisites:** Python 3.10 or later and Git.

Clone the repository and navigate to its directory.

Create and activate a virtual environment:

```bash
python3.10 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Author

**Anupam Mishra**  
Indian Institute of Information Technology, Ranchi

## Project Supervisor

**Dr. Rashmi Panda**  
Indian Institute of Information Technology, Ranchi
