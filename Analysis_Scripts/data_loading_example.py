# -*- coding: utf-8 -*-
"""Load and preview the EHD printing dataset.

Run from any working directory with:
    python Analysis_Scripts/data_loading_example.py

Requires:
    pandas
"""

from pathlib import Path
import sys

import pandas as pd


try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, OSError):
    pass


PACKAGE_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = PACKAGE_DIR / "EHD_Printing_MainData.csv"

EXPECTED_COLUMNS = [
    "Num",
    "Bias_V",
    "Amplitude_V",
    "DutyCycle_pct",
    "Height_um",
    "AirPressure_mbar",
    "PrintingTime_ms",
    "JetState",
    "DropletDiameter_um",
    "DropletVolume_pL",
]


def load_dataset(data_file: Path = DATA_FILE) -> pd.DataFrame:
    """Load the main CSV and validate its published column structure."""
    if not data_file.exists():
        raise FileNotFoundError(f"Data file not found: {data_file}")

    dataframe = pd.read_csv(data_file, encoding="utf-8-sig")
    if dataframe.columns.tolist() != EXPECTED_COLUMNS:
        raise ValueError(
            "Unexpected columns in the main data file.\n"
            f"Expected: {EXPECTED_COLUMNS}\n"
            f"Found:    {dataframe.columns.tolist()}"
        )
    return dataframe


def main() -> None:
    """Print a compact loading example and basic integrity information."""
    dataframe = load_dataset()

    print(f"Loaded: {DATA_FILE}")
    print(f"Shape: {dataframe.shape[0]:,} rows x {dataframe.shape[1]} columns")

    print("\nColumn data types:")
    print(dataframe.dtypes.to_string())

    print("\nFirst five rows:")
    print(dataframe.head().to_string(index=False))

    print("\nJet-state counts:")
    print(dataframe["JetState"].value_counts(dropna=False).to_string())

    stable_diameters = dataframe.loc[
        dataframe["JetState"].eq("Stable jetting"), "DropletDiameter_um"
    ]
    print(
        "\nStable-jetting droplet diameter: "
        f"n={stable_diameters.count():,}, "
        f"mean={stable_diameters.mean():.2f} µm, "
        f"std={stable_diameters.std():.2f} µm"
    )


if __name__ == "__main__":
    main()
