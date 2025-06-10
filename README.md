# Fundus Image Analysis

This project analyzes fundus (eye) images using OpenAI's GPT-4 Vision model and saves the results to CSV and Excel files.

## How to Use

1. **Add your images**  
   Put your JPG/PNG images in the `images/` folder.

2. **Set up your environment**  
   - Install Python 3 and create a virtual environment (optional).
   - Install dependencies:
     ```sh
     pip install openai python-dotenv pandas openpyxl
     ```
   - Create a `.env` file with your OpenAI API key:
    3.**Important**
    - 
     ```
     OPENAI_API_KEY=your_openai_api_key_here
     ```

3. **Run the analysis**  
   - As a script:
     ```sh
     python main.py
     ```
   - Or open and run `main_nb.ipynb` in Jupyter.

4. **View your results**  
   - Results are saved in `results.csv` and `results.xlsx` with one row per image.


---

**Questions?**  
Contact [Diwash Patel](https://github.com/DiwashPatel).