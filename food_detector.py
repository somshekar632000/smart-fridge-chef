import json
import os
import re
import traceback
from google.generativeai import GenerativeModel, configure

# Retrieve Gemini API key from environment variable
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("❌ GEMINI_API_KEY environment variable not set")
    exit(1)

try:
    configure(api_key=GEMINI_API_KEY)
except Exception as e:
    print(f"❌ Failed to configure Gemini API: {e}")
    exit(1)

def detect_food_items(image_path):
    try:
        print(f"🔍 Detecting food items in: {image_path}")
        
        if not os.path.exists(image_path):
            print(f"❌ Image file not found: {image_path}")
            return []
        
        with open(image_path, 'rb') as img_file:
            img_data = img_file.read()
        
        model = GenerativeModel('gemini-2.5-pro')
        
        prompt = """
        Detect all prominent food ingredients in the image. For each item, provide:
        - label: Name of the fruit/vegetable
        - box_2d: Bounding box coordinates [ymin, xmin, ymax, xmax] normalized to 0-1000
        Return the response as a JSON array of objects, e.g.:
        [
            {"label": "apple", "box_2d": [100, 200, 300, 400]},
            {"label": "banana", "box_2d": [150, 250, 350, 450]}
        ]
        """
        response = model.generate_content([prompt, {"mime_type": "image/jpeg", "data": img_data}])
        
        print("✅ Gemini response received")
        print(f"Raw response: {response.text[:200]}...")
        
        try:
            json_str = re.search(r'\[\s*{.*?}\s*\]', response.text, re.DOTALL)
            if json_str:
                annotations = json.loads(json_str.group(0))
                print(f"✅ Parsed {len(annotations)} annotations")
                return annotations
            else:
                print("❌ No JSON array found in response")
                print(f"Full response: {response.text}")
                return []
        except json.JSONDecodeError as e:
            print(f"❌ JSON decode error: {e}")
            print(f"Raw response: {response.text}")
            return []
        
    except Exception as e:
        print(f"❌ Detection error: {e}")
        traceback.print_exc()
        return []