# Fundus Image Analysis with GPT-4 Vision

This repository provides a pipeline to analyze fundus (optic disc) images using OpenAI's GPT-4 Vision model. The code processes images, extracts clinical features, merges results with ground truth, and evaluates model performance with a variety of metrics and plots.

---

## 📁 Folder Structure

```
.
├── datasets/
│   └── Sample with available VCDR.xlsx
├── images/
│   └── (your .jpg/.jpeg/.png files)
├── results/
│   ├── merged_on_ranid_tracking_<timestamp>.xlsx
│   └── (results_*.csv, results_*.xlsx, processed_images.txt, etc.)
├── evaluations/
│   └── <timestamp>/
│       ├── metrics.txt
│       ├── Confusion matrix.png
│       └── *_scatter.png
├── main.py
├── main_nb.ipynb
├── merge_files.py
├── concat_tables.py
├── evaluate_results.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

---

## 🚀 How to Use

### 1. **Prepare Your Data**
- Place your fundus images in the `images/` folder.
- Place your ground truth dataset (e.g., `Sample with available VCDR.xlsx`) in the `datasets/` folder.

### 2. **Merge Results with Ground Truth**

- Open `concat_tables.py`.
- **Important:**  
  On line 7, ensure the `ground_truth_file` matches your dataset file name:
  ```python
  ground_truth_file=os.path.join("datasets", 'Sample with available VCDR.xlsx')
  ```
  Change the file name if your dataset is named differently.

- Run the script:
  ```sh
  python concat_tables.py
  ```
- This will generate a file in `results/` named like:
  ```
  merged_on_ranid_tracking_<date>.xlsx
  ```
  Use this merged file for evaluation.

### 3. **Evaluate Model Metrics**

- Open `evaluate_results.py`.
- **Important:**  
  On line 24, set the `file_name` variable to the latest merged file you want to evaluate:
  ```python
  file_name = "merged_on_ranid_tracking_20250624_155649.xlsx"
  ```
- Run the script:
  ```sh
  python evaluate_results.py
  ```
- This will create a new subfolder in `evaluations/` with the current timestamp.  
  Inside, you'll find:
  - `metrics.txt` (all evaluation metrics)
  - `Confusion matrix.png`
  - Scatter plots for numeric variables

---

## 📝 Notes & Assumptions

- **Ground Truth Labels:**  
  In the ground truth (`fundus_label` column), there are two categories:  
  - `'normal'` (considered as normal, mapped to 0)
  - `'poag'` (considered as not normal, mapped to 1)

- **Prediction Labels:**  
  In the predictions (`glaucoma` column), values are `'Yes'` (1) and `'No'` (0).

- **Further Cleaning:**  
  You may further clean the merged files (e.g., remove unused columns) before evaluation if needed.

- **Folder Structure:**  
  Keep the folder structure as shown above for scripts to work out-of-the-box.

---

## ⚠️ Things to Care About

- Always update the ground truth file name in `concat_tables.py` if your dataset changes.
- Always update the merged file name in `evaluate_results.py` to point to the latest results.
- All evaluation results are organized by timestamp in the `evaluations/` folder for easy tracking.

---

## ❓ Questions

If you have any questions or need help, please contact [Diwash Patel].

---