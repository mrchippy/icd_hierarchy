"""A setuptools based setup module.
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
    name="icd_hierarchy",  
    version="0.0.1",  
    description="Map ICD_CM hierarchy to flatter structure", 
    long_description=long_description, 
    long_description_content_type="text/markdown",
    url="https://github.com/mrchippy/icd_hierarchy",
    package_dir={"":"src"},
    packages=find_packages(where="src"),
    python_requires=">=3.10, <4",
    install_requires=["pandas","importlib"], 
    package_data={ 
        "icd_hierarchy": ["icd9_cm.json"]
    }
)