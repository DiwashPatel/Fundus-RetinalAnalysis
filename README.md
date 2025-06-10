# Fundus Image Analysis

This project analyzes fundus (eye) images using OpenAI's GPT-4 Vision model and saves the results to CSV and Excel files.

---

## How to Use

1. **Add your images**  
   Put your JPG/PNG images in the `images/` folder.

2. **Set up your environment**  
   - Install Python 3 and create a virtual environment (optional).
   - Install dependencies:
     ```sh
     pip install openai python-dotenv pandas openpyxl
     ```

3. **Important**  
   - Create a `.env` file with your OpenAI API key and save your API key there (for this we installed python-dotenv):
     ```
     OPENAI_API_KEY=your_openai_api_key_here
     ```
   - If you don't want to install python-dotenv, you can directly use your API key in the main script like:
     ```python
     client = OpenAI(api_key="YOUR_OPENAI_API_KEY")
     ```
     and you can remove these lines:
     ```python
     from dotenv import load_dotenv
     load_dotenv() 
     ```

4. **Run the analysis**  
   - As a script:
     ```sh
     python main.py
     ```
   - Or open and run `main_nb.ipynb` in Jupyter.

5. **View your results**  
   - Results are saved in `results.csv` and `results.xlsx` with one row per image.

---

**Questions? Pleae Contact**  
-[Diwash Patel](diwashpatel.com)

dpatel10@my.fisk.edu

diwashpatel1123@gmail.com

(615)-482-1894
```