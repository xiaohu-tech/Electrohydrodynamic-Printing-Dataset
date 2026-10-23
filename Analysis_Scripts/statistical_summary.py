# -*- coding: utf-8 -*-
"""Generate reproducible statistical summaries for the dataset.

Run from any working directory with:
    python Analysis_Scripts/statistical_summary.py

By default, four CSV summaries are written to Analysis_Scripts/output/.
Use --output-dir PATH to choose a different destination.

Requires:
    pandas
"""

import argparse
from pathlib import Path
import sys

import pandas as pd

from data_loading import DATA_FILE, load_dataset


try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, OSError):
    pass


DEFAULT_OUTPUT_DIR = Path(__file__).resolve().parent / "output"

NUMERIC_FIELDS = {
    "Bias_V": ("Bias voltage", "V"),
    "Amplitude_V": ("Voltage amplitude", "V"),
    "DutyCycle_pct": ("Duty cycle", "%"),
    "Height_um": ("Printing height", "µm"),
    "AirPressure_mbar": ("Air pressure", "mbar"),
    "PrintingTime_ms": ("Printing time", "ms"),
    "DropletDiameter_um": ("Droplet diameter", "µm"),
}

MISSING_VALUE_NOTES = {
    "DropletDiameter_um": (
        "Recorded only for Stable jetting; missing for all other jet states"
    ),
}


def make_overview(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Return dataset-level facts."""
    stable_count = int(dataframe["JetState"].eq("Stable jetting").sum())
    return pd.DataFrame(
        [
            ("File name", DATA_FILE.name),
            ("Rows", len(dataframe)),
            ("Columns", len(dataframe.columns)),
            ("Encoding", "UTF-8 with BOM"),
            ("Jet-state categories", "Stable jetting; Unstable jetting; No jetting"),
            ("Stable-jetting rows", stable_count),
        ],
        columns=["Item", "Value"],
    )


def make_numeric_summary(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Return descriptive statistics for published numeric fields."""
    rows = []
    for column, (label, unit) in NUMERIC_FIELDS.items():
        series = dataframe[column]
        count = int(series.count())
        rows.append(
            {
                "Variable": label,
                "Column": column,
                "Unit": unit,
                "Count": count,
                "Missing": int(series.isna().sum()),
                "Mean": round(series.mean(), 2) if count else None,
                "Std": round(series.std(), 2) if count else None,
                "Min": round(series.min(), 2) if count else None,
                "P25": round(series.quantile(0.25), 2) if count else None,
                "Median": round(series.median(), 2) if count else None,
                "P75": round(series.quantile(0.75), 2) if count else None,
                "Max": round(series.max(), 2) if count else None,
                "Unique": int(series.nunique()),
            }
        )
    return pd.DataFrame(rows)


def make_jet_state_summary(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Return counts and percentages for each jet-state category."""
    counts = dataframe["JetState"].value_counts(dropna=False)
    total = len(dataframe)
    return pd.DataFrame(
        [
            {
                "JetState": category,
                "Count": int(count),
                "Percentage_pct": round(count / total * 100, 2),
            }
            for category, count in counts.items()
        ]
    )


def make_missing_values_summary(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Return missing-value counts, rates, and documented reasons."""
    total = len(dataframe)
    return pd.DataFrame(
        [
            {
                "Column": column,
                "Missing": int(dataframe[column].isna().sum()),
                "Missing_Rate_pct": round(dataframe[column].isna().mean() * 100, 2),
                "Note": MISSING_VALUE_NOTES.get(column, ""),
            }
            for column in dataframe.columns
        ]
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help=f"Directory for generated CSV files (default: {DEFAULT_OUTPUT_DIR})",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_dir = args.output_dir.expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    dataframe = load_dataset()
    summaries = {
        "overview.csv": make_overview(dataframe),
        "numeric_summary.csv": make_numeric_summary(dataframe),
        "jet_state_summary.csv": make_jet_state_summary(dataframe),
        "missing_values_summary.csv": make_missing_values_summary(dataframe),
    }

    for filename, summary in summaries.items():
        output_path = output_dir / filename
        summary.to_csv(output_path, index=False, encoding="utf-8-sig")
        print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
