import numpy as np
import pandas as pd
from pathlib import Path

mergedfile = pd.read_excel(f"results/merged_on_ranid_tracking_20250624_155649.xlsx")

for col in mergedfile.columns:
    print(f"{col}: {mergedfile[col].unique()}")