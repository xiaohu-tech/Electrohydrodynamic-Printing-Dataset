# EHD Printing Dataset

This repository contains an electrohydrodynamic (EHD) printing dataset and two small Python examples for reproducible loading and summary generation.

## Package contents

```text
EHD_Printing_Dataset/
├── EHD_Printing_MainData.csv
├── Data_Dictionary.csv
├── README.md
└── Analysis_Scripts/
    ├── data_loading_example.py
    └── statistical_summary.py
```

- `EHD_Printing_MainData.csv` is the main data file.
- `Data_Dictionary.csv` defines every field, unit, value range or allowed values, and relevant notes.
- `Analysis_Scripts/data_loading_example.py` demonstrates loading, validation, previewing, and simple filtering.
- `Analysis_Scripts/statistical_summary.py` generates dataset, numeric, categorical, and missing-value summaries.

## Data format

The main file is a comma-separated, UTF-8 file with a single header row. It contains 203,759 observations and 10 columns. Each row represents one EHD printing observation.

Published fields are:

| Field | Meaning | Unit |
| --- | --- | --- |
| `Num` | Sequential observation identifier | none |
| `Bias_V` | Bias voltage | V |
| `Amplitude_V` | Voltage amplitude | V |
| `DutyCycle_pct` | Duty cycle | % |
| `Height_um` | Printing height | µm |
| `AirPressure_mbar` | Air pressure | mbar |
| `PrintingTime_ms` | Printing duration | ms |
| `JetState` | Observed jet state | none |
| `DropletDiameter_um` | Measured droplet diameter | µm |
| `DropletVolume_pL` | Droplet volume | pL |

See `Data_Dictionary.csv` for complete definitions and observed ranges.

## Measurement availability

`DropletDiameter_um` is defined for observations classified as `Stable jetting`.

## Quick start

Python 3.9 or later and `pandas` are recommended.

```bash
python -m pip install pandas
python Analysis_Scripts/data_loading_example.py
python Analysis_Scripts/statistical_summary.py
```

The scripts locate the dataset relative to their own file paths, so they can be launched from any working directory.

The summary script creates these files under `Analysis_Scripts/output/` by default:

- `overview.csv`
- `numeric_summary.csv`
- `jet_state_summary.csv`
- `missing_values_summary.csv`

To choose another output location:

```bash
python Analysis_Scripts/statistical_summary.py --output-dir path/to/output
```

## Load the data in your own code

```python
import pandas as pd

data = pd.read_csv("EHD_Printing_MainData.csv", encoding="utf-8-sig")
print(data.shape)
print(data.head())
```

The expected shape is `(203759, 10)`. The scripts additionally validate the exact published column order to help detect accidental file changes.

## Reproducibility notes

- The main CSV stores the original observation values; only the legacy multi-row heading was replaced with stable, machine-readable column names.
- Field names are identical across the main CSV, data dictionary, README, and analysis scripts.
- Generated summaries are derivative outputs and are not included in the four-component source package.
