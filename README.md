# icd_hierarchy

Utility for mapping JSON of ICD9-CM diagnoses into a flatter structure needed for some libraries (for example, plotly's Treemap).

## Installation
From the same directory as this README,
```
pip install -e .
```

## Usage
```python
hier = ICD9_Hierarchy('icd9_cm.json')
flattened_df = hier.get_flattened_df()
```