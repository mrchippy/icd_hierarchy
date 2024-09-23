# icd_hierarchy

Utility for mapping JSON of ICD9-CM diagnoses into a flatter structure needed for some libraries (for example, plotly's Treemap).

## Installation
From the same directory as this README,
```
pip install -e .
```

## Usage
Hierarchy class takes a file reference (name or path object) and a Mapping that returns an int or float value for a given ICD-9 code (dotted or non-dotted MIMIC-style). If a file is not provided, the included json file will be used (see, for example, https://github.com/LuChang-CS/icd_hierarchical_structure).
```python
hier = ICD9_Hierarchy()
flattened_df = hier.get_flattened_df()
```

## Dependencies
Depends on pandas and importlib.