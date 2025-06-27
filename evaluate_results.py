import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import os
from sklearn.metrics import (
    accuracy_score, f1_score, cohen_kappa_score,
    roc_auc_score, recall_score, precision_score,
    confusion_matrix, ConfusionMatrixDisplay
)

os.makedirs("evaluations", exist_ok= True)
from datetime import datetime

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
eval_dir = f"evaluations/{timestamp}"
os.makedirs(eval_dir, exist_ok=True)


# === Step 1: Load Merged Data ===
#Change the file_name with the latest and Complete merged file...

file_name = "merged_on_ranid_tracking_20250624_155649.xlsx"
file_path = Path(f"results/{file_name}")

if file_path.suffix == ".xlsx":
    merged = pd.read_excel(file_path)
else:
    merged = pd.read_csv(file_path)

# === Step 2: Rename columns for simplicity ===
# Rename predicted 'glaucoma (Glaucoma Diagnosis)' to 'glaucoma'
merged.rename(columns={'glaucoma (Glaucoma Diagnosis)': 'glaucoma'}, inplace=True)

# Optional: rename numerical prediction columns to match ground truth names
col_rename_map = {
    'vcdratio (Vertical Cup-Disc Ratio)': 'vcdratio_pred',
    'hcdratio (Horizontal Cup-Disc Ratio)': 'hcdratio_pred',
    'dischem (Disc Hemorrhage)': 'dischem_pred',
    'rimnotch (Rim Notch)': 'rimnotch_pred',
    'rimthin (Rim Thinning)': 'rimthin_pred',
    'ntchclkhrs (Rim Notch Location)': 'ntchclkhrs_pred',
    'dhemlocn (Disc Hemorrhage Location)': 'dhemlocn_pred',
    'pericrescent (Peripapillary Atrophy Crescent)': 'pericrescent_pred'
}
merged.rename(columns=col_rename_map, inplace=True)


# Map string labels to integers
label_map_fundus = {'normal': 0, 'poag': 1}
label_map_glaucoma = {'No': 0, 'Yes': 1}

merged['fundus_label'] = merged['fundus_label'].map(label_map_fundus)
merged['glaucoma'] = merged['glaucoma'].map(label_map_glaucoma)

# Drop rows where mapping failed (i.e., label was not recognized)
merged = merged.dropna(subset=['fundus_label', 'glaucoma'])

# Ensure data is int for metrics
merged['fundus_label'] = merged['fundus_label'].astype(int)
merged['glaucoma'] = merged['glaucoma'].astype(int)


# === Step 4: Classification Metrics ===
y_true = merged['fundus_label']
y_pred = merged['glaucoma']

tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()

metrics = {
    'Accuracy': accuracy_score(y_true, y_pred),
    'F1 Score': f1_score(y_true, y_pred),
    'Cohen’s Kappa': cohen_kappa_score(y_true, y_pred),
    'AUC': roc_auc_score(y_true, y_pred),
    'Sensitivity (Recall for Positive)': recall_score(y_true, y_pred),
    'Specificity': recall_score(y_true, y_pred, pos_label=0),
    'False Positive Rate': fp / (fp + tn),
    'False Negative Rate': fn / (fn + tp)
}

print("\n=== Evaluation Metrics ===")
for k, v in metrics.items():
    print(f"{k}: {v:.4f}")


with open(f"{eval_dir}/metrics.txt", "w") as f:
    f.write("=== Evaluation Metrics ===\n")
    for k, v in metrics.items():
        f.write(f"{k}: {v:.4f}\n")

# === Step 5: Confusion Matrix ===
ConfusionMatrixDisplay.from_predictions(y_true, y_pred, display_labels=["No Glaucoma", "Glaucoma"])
plt.title("Confusion Matrix")
plt.savefig(f"{eval_dir}/Confusion matrix")
plt.close()
# plt.show()


# === Step 6: Scatter Plots (Numeric Predictions) ===
numeric_pairs = [
    ('vcdratio', 'vcdratio_pred'),
    ('hcdratio', 'hcdratio_pred'),
    ('dischem', 'dischem_pred'),
    ('rimthin', 'rimthin_pred'),
    ('rimnotch', 'rimnotch_pred'),
    ('ntchclkhrs', 'ntchclkhrs_pred'),
    ('dhemlocn', 'dhemlocn_pred'),
    ('pericrescent', 'pericrescent_pred'),
]



for actual, predicted in numeric_pairs:
    if actual in merged.columns and predicted in merged.columns:
        x = pd.to_numeric(merged[actual], errors='coerce')
        y = pd.to_numeric(merged[predicted], errors='coerce')
        valid = ~(x.isna() | y.isna())
        if valid.sum() > 0:
            plt.figure(figsize=(8, 6))
            # Scatter plot with larger dots and color
            sns.scatterplot(x=x[valid], y=y[valid], s=60, color="#1f77b4", alpha=0.7, edgecolor="k")
            # Regression line
            sns.regplot(x=x[valid], y=y[valid], scatter=False, color="red", line_kws={"lw":2, "ls":"--"})
            # Diagonal reference line
            min_val = min(x[valid].min(), y[valid].min())
            max_val = max(x[valid].max(), y[valid].max())
            plt.plot([min_val, max_val], [min_val, max_val], 'g--', lw=2, label='Ideal')
            plt.xlabel(f"Actual {actual}", fontsize=12)
            plt.ylabel(f"Predicted {predicted}", fontsize=12)
            plt.title(f"Scatter Plot: {actual} vs {predicted}", fontsize=14)
            plt.legend()
            plt.grid(True, linestyle='--', alpha=0.6)
            plt.tight_layout()
            plt.savefig(f"{eval_dir}/{actual}_vs_{predicted}_scatter.png", dpi=150)
            plt.close()
        else:
            print(f"Skipping {actual} vs {predicted}: no valid numeric data")

    
# Confusion Matrices for Other Categorical Variables ===

# Define mapping for categorical variables
cat_maps = {
    # Add mappings for each variable as needed
    'dischem': {'yes': 1, 'with': 1, '1': 1, 1: 1, 'no': 0, 'without': 0, '0': 0, 0: 0, 'unknown': np.nan, '': np.nan, np.nan: np.nan},
    'rimnotch': {'yes': 1, 'with': 1, '1': 1, 1: 1, 'no': 0, 'without': 0, '0': 0, 0: 0, 'unknown': np.nan, '': np.nan, np.nan: np.nan},
    'rimthin': {'yes': 1, 'with': 1, '1': 1, 1: 1, 'no': 0, 'without': 0, '0': 0, 0: 0, 'unknown': np.nan, '': np.nan, np.nan: np.nan},
    'pericrescent': {'yes': 1, 'with': 1, '1': 1, 1: 1, 'no': 0, 'without': 0, '0': 0, 0: 0, 'unknown': np.nan, '': np.nan, np.nan: np.nan},
}

for col_base in cat_maps:
    actual_col = col_base
    pred_col = f"{col_base}_pred"
    if actual_col in merged.columns and pred_col in merged.columns:
        # Lowercase and string conversion for mapping
        actual = merged[actual_col].astype(str).str.lower().str.strip()
        pred = merged[pred_col].astype(str).str.lower().str.strip()
        # Map values
        actual_mapped = actual.map(cat_maps[col_base])
        pred_mapped = pred.map(cat_maps[col_base])
        # Drop rows with NaN in either
        valid = ~(actual_mapped.isna() | pred_mapped.isna())
        if valid.sum() < 2 or actual_mapped[valid].nunique() < 2 or pred_mapped[valid].nunique() < 2:
            print(f"Skipping confusion matrix for {col_base}: not enough valid data or only one class present.")
            continue
        # Compute confusion matrix
        cm = confusion_matrix(actual_mapped[valid], pred_mapped[valid], labels=[0, 1])
        disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["No", "Yes"])
        disp.plot(cmap="Blues")
        plt.title(f"Confusion Matrix: {col_base}")
        plt.savefig(f"{eval_dir}/Confusion_matrix_{col_base}.png")
        plt.close()
        print(f"Saved confusion matrix for {col_base} ({valid.sum()} valid samples)")