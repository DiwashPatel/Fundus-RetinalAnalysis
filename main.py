import os
import base64
import json
import time
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


#Processed keeps tracks of images that are successfully analysed
processed = set() 
results = []       # Stores all results

#Getting all the images
IMAGE_FOLDER = "images"
all_images = {
    f for f in os.listdir(IMAGE_FOLDER) 
    if f.lower().endswith(('.jpg', '.jpeg', '.png'))
}

def encode_image(image_name):
    """Convert image to base64 string"""
    img_path = os.path.join(IMAGE_FOLDER, image_name)
    with open(img_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def analyze_image(image_name):
    """Analyze single image and return result"""
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
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
        
        if not response.choices or not hasattr(response.choices[0], "message"):
            print(f"No choices/message returned for {image_name}")
            return None
        
        generated_content = response.choices[0].message.content

        if not generated_content:
            print(f"No content returned for {image_name}")
            return None
        
        result = json.loads(generated_content)
        result["image_name"] = image_name
        return result
    
    except Exception as e:
        print(f"Error processing {image_name}: {str(e)}")
        return None


# Process each image
for img_name in all_images:
    if img_name not in processed:
        result = analyze_image(img_name)
        if result:
            results.append(result)
            processed.add(img_name)
            print(f"Processed: {img_name}")

            #Saves after reach result (In case the script stops unexpectedly)
            pd.DataFrame(results).to_csv("results.csv", index=False)
        time.sleep(1)  # Avoid rate limits

# Save to Excel
if results:
    df = pd.DataFrame(results)
    # Move 'image_name' to the first column
    cols = df.columns.tolist()
    if "image_name" in cols:
        cols.insert(0, cols.pop(cols.index("image_name")))
        df = df[cols]
    df.to_excel("results.xlsx", index=False)
    print("Saved results to results.xlsx")

