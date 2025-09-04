# Fundus: Automated Analysis of Retinal Images           👁️🩺👁️

## Project Description

Fundus is an automated tool for analyzing retinal (fundus) images to extract glaucoma-related clinical features. The project uses GPT-4 to interpret images and generate basic clinical summaries. The project provides a basic workflow for image preprocessing & feature extractions.

## Getting Started 🚀

### Prerequisites

- Python 3.8+
- Required libraries listed in `requirements.txt`
- A folder of retinal images (JPEG, PNG, etc.)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/DiwashPatel/Fundus.git
   cd Fundus
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Usage

1. Place your retinal images in the designated input folder.
2. Run the analysis script:
   ```bash
   python analyze.py --input_folder ./images
   ```

## Important Notes ⚠️

- Some file paths are hardcoded; please keep the directory structure as provided.
- The project assumes images are in standard formats (JPEG, PNG).
- Review and adjust file paths in the code if you change the folder names or structure.
- Keep the folder structure as shown above for scripts to work out-of-the-box.
- You may further clean the merged files (e.g., remove unused columns) before evaluation if needed.

## Notes & Things to Know 📝

- **Ground Truth Labels:**  
  In the ground truth (`fundus_label` column), there are two categories:  
  - `'normal'` (considered as normal, mapped to 0)
  - `'poag'` (considered as not normal, mapped to 1)

  In the predictions (`glaucoma` column), values are `'Yes'` (1) and `'No'` (0).

---

## Credits 🙏

- Code writing was assisted by ChatGPT (OpenAI).

## Suggestions??

- If you have suggestions or find issues, feel free to open an issue or submit a pull request.