# Fundus Image Analysis with GPT-4 Vision

This repository provides a pipeline to analyze fundus (optic disc) images using OpenAI's GPT-4 Vision model. The code processes images, extracts clinical features, and saves the results in CSV and Excel formats. It also keeps track of processed images to avoid redundant analysis.

---

## 📁 Folder Structure

```
.
├── datasets/
│   └── last_visit_with_img_exist_subcol_v2.csv
├── images/
│   ├── 90001-KW254-L.jpg
│   ├── 90001-KW254-R.jpg
│   ├── 90001-VR219-L.jpg
│   ├── 90001-VR219-R.jpg
│   ├── 90002-CV822-L.jpg
│   └── 90002-CV822-R.jpg
├── main_nb.ipynb
├── main.py
├── merge_files.py
├── Prompt.docx
├── README.md
├── requirements.txt
└── results/
    ├── merged_output_20250618_001455.xlsx
    ├── processed_images.txt
    ├── results_20250617_232031.csv
    └── results_20250617_232031.xlsx
```

---

## 🚀 How to Use

### 1. **Add Your Images**
- Put all your `.jpg`, `.jpeg`, or `.png` fundus images in the `images/` folder.

### 2. **Set Up Your Environment**
- Install Python 3.
- (Optional) Create and activate a virtual environment:
  ```sh
  python3 -m venv fundus_venv
  source fundus_venv/bin/activate
  ```
- Install dependencies:
  ```sh
  pip install -r requirements.txt
  ```
  or, if `requirements.txt` is missing:
  ```sh
  pip install openai python-dotenv pandas openpyxl
  ```

### 3. **Configure Your OpenAI API Key**
- Create a `.env` file in the project root:
  ```
  OPENAI_API_KEY=your_openai_api_key_here
  ```

### 4. **Run the Analysis**
- To process all images in the `images/` folder, run:
  ```sh
  python main.py
  ```
- The script will:
  - Analyze each image using GPT-4 Vision.
  - Save results in `results/results_<timestamp>.csv` and `.xlsx`.
  - Keep track of processed images in `results/processed_images.txt` to avoid redundant processing.

- **Jupyter Notebook:**  
  You can also open and run `main_nb.ipynb` for step-by-step execution.

---

## 📝 Notes

- **Folder structure must remain the same** for the code to work out-of-the-box.
- The script automatically skips images that have already been processed (tracked in `results/processed_images.txt`).
- You can replace or update the dataset in the `datasets/` folder as needed for merging or validation.
- To merge your results with a ground truth dataset, use `merge_files.py` and update the dataset path as needed.

---

## 📂 Customizing Datasets

- Place your actual dataset (e.g., ground truth CSV) in the `datasets/` folder.
- Update the path in `merge_files.py` if your dataset file name or location changes.

---

## ❓ Questions

If you have any questions or need help, please contact Diwash Patel

---