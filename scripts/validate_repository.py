"""Perform lightweight structural checks on the public repository."""

from __future__ import annotations

import json
import sys
from pathlib import Path


REQUIRED_FILES = (
    "README.md",
    "LICENSE",
    "CITATION.cff",
    "DATA_AVAILABILITY.md",
    "requirements.txt",
    "environment.yml",
    "notebooks/01_preprocessing_rp_pos.ipynb",
    "notebooks/02_statistical_analysis_rp_pos.ipynb",
    "data/raw/CELL_export_mzmine.csv",
    "data/metadata/CELL_injection_order.xlsx",
    "data/databases/DTB_contaminants_exogenous_features.xlsx",
    "data/processed/08_CELL_final_cleaned_dataset.xlsx",
)


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    problems: list[str] = []

    for relative in REQUIRED_FILES:
        if not (root / relative).is_file():
            problems.append(f"Missing required file: {relative}")

    checkpoints = list(root.rglob(".ipynb_checkpoints"))
    if checkpoints:
        problems.extend(
            f"Jupyter checkpoint directory should not be published: {path.relative_to(root)}"
            for path in checkpoints
        )

    for notebook_name in (
        "notebooks/01_preprocessing_rp_pos.ipynb",
        "notebooks/02_statistical_analysis_rp_pos.ipynb",
    ):
        path = root / notebook_name
        if path.is_file():
            try:
                notebook = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as error:
                problems.append(f"Invalid notebook {notebook_name}: {error}")
                continue
            if notebook.get("nbformat") != 4:
                problems.append(f"Unexpected notebook format: {notebook_name}")

    if not list((root / "outputs" / "figures").rglob("*.png")):
        problems.append("No PNG figure found below outputs/figures")
    if not list((root / "outputs" / "tables").rglob("*.xlsx")):
        problems.append("No Excel result table found below outputs/tables")

    if problems:
        print("Repository validation failed:")
        for problem in problems:
            print(f"- {problem}")
        return 1

    print("Repository validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
