import os
import base64
import json
import time
from datetime import datetime
import pandas as pd
from openai import OpenAI
from openai.types.chat import ChatCompletionUserMessageParam
from dotenv import load_dotenv

load_dotenv()  
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

PROMPT = """ Please analyze the optic disc photograph I will upload and reply with exactly the following JSON object—nothing else. Use these rules for every field:
• If a value is not discernible, enter "unknown" (or an empty array [] where noted).
• Do not add comments or extra keys.
• Keep number formatting exactly as specified.

{
  "vcdratio (Vertical Cup-Disc Ratio)": "0.0-0.9 in 0.1 increments or 'unknown'",
  "hcdratio (Horizontal Cup-Disc Ratio)": "0.0-0.9 in 0.1 increments or 'unknown'",
  "dischem (Disc Hemorrhage)": "'Yes'/'No'/'unknown'",
  "dhemlocn (Disc Hemorrhage Location)": "['clock hours (e.g., \"7:00\")'] or []",
  "rimnotch (Rim Notch)": "'Yes'/'No'/'unknown'",
  "ntchclkhrs (Rim Notch Location)": "['clock hours (e.g., \"7:30\")'] or []",
  "pericrescent (Peripapillary Atrophy Crescent)": "'Yes'/'No'/'unknown'",
  "rimthin (Rim Thinning)": "'Yes'/'No'/'unknown'",
  "rimthinloc (Rim Thinning Location)": "['clock hour location (e.g., \"7:00\")'] or []",
  "clarity (Image Clarity)": "'Good'/'Fair'/'Poor'/'unknown'",
  "glaucoma (Glaucoma Diagnosis)": "'Yes'/'No'/'unknown'"
}

RULES:
1. Use clock-hour notation (e.g., '7:30') for locations
2. For unclear features, use 'unknown'
3. Empty arrays [] when no locations exist
"""

def encode_image(image_name):
    """Convert image to base64 string"""
    img_path = os.path.join(IMAGE_FOLDER, image_name)
    with open(img_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def analyze_image(image_name):
    """Analyze single image and return result dict with metadata"""
    try:
        start_time = time.time()

        response = client.chat.completions.create(
            model="gpt-4.1-mini",  # change if needed
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": PROMPT},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{encode_image(image_name)}"
                        }
                    }
                ]
            }],
            response_format={"type": "json_object"}
        )

        elapsed_time = time.time() - start_time

        if not response.choices or not hasattr(response.choices[0], "message"):
            print(f"No choices/message returned for {image_name}")
            return None

        generated_content = response.choices[0].message.content
        if not generated_content:
            print(f"No content returned for {image_name}")
            return None

        # Parse result JSON
        result = json.loads(generated_content)

        # Add metadata
        result["image_name"] = image_name
        result["processed_at"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        result["elapsed_time_sec"] = round(elapsed_time, 2)

        # Token usage
        usage = response.usage if hasattr(response, "usage") else None
        result["prompt_tokens"] = usage.prompt_tokens if usage else "unknown"
        result["completion_tokens"] = usage.completion_tokens if usage else "unknown"
        result["total_tokens"] = usage.total_tokens if usage else "unknown"

        return result

    except Exception as e:
        print(f"Error processing {image_name}: {str(e)}")
        return None


# === Setup paths and folders ===
IMAGE_FOLDER = "images"
RESULTS_FOLDER = "results"
os.makedirs(RESULTS_FOLDER, exist_ok=True)

timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
output_filename = os.path.join(RESULTS_FOLDER, f'results_{timestamp}')
processed_file_path = os.path.join(RESULTS_FOLDER, "processed_images.txt")

# === Load processed image names from file ===
if os.path.exists(processed_file_path):
    with open(processed_file_path, "r") as f:
        processed = set(line.strip() for line in f if line.strip())
else:
    processed = set()

# === Load all image files ===
all_images = {
    f for f in os.listdir(IMAGE_FOLDER)
    if f.lower().endswith(('.jpg', '.jpeg', '.png'))
}

# === Store results and newly processed files ===
results = []
newly_processed = set()

# === Main Loop with Safe Writing ===
try:
    for img_name in all_images:
        if img_name not in processed:
            print(f"Analyzing: {img_name}")
            result = analyze_image(img_name)
            if result:
                results.append(result)
                newly_processed.add(img_name)
                print(f"Processed: {img_name}")
            time.sleep(1)  # Prevent rate limit
        else:
            print(f"Skipping already processed: {img_name}")

finally:
    # Save processed image names
    if newly_processed:
        with open(processed_file_path, "a") as f:
            for name in newly_processed:
                f.write(name + "\n")
        print(f"Updated processed_images.txt with {len(newly_processed)} new entries.")

    # Save final results to CSV and Excel
    if results:
        df = pd.DataFrame(results)
        cols = df.columns.tolist()
        if "image_name" in cols:
            cols.insert(0, cols.pop(cols.index("image_name")))
            df = df[cols]

        df.to_csv(f"{output_filename}.csv", index=False)
        df.to_excel(f"{output_filename}.xlsx", index=False)
        print(f"Results saved to: {output_filename}.csv and .xlsx")
    else:
        print("No new results to save.")
        