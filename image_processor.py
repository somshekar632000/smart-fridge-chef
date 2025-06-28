import cv2
import os
import shutil
from collections import Counter
import traceback
import gradio as gr

def capture_image(output_path="data/captured.jpg", width=1640, height=1232):
    print("⚠ Camera capture not supported on Windows. Please upload an image.")
    return False

def create_annotated_image(image_path, annotations):
    try:
        image = cv2.imread(image_path)
        if image is None:
            print(f"❌ Could not load image: {image_path}")
            return None
            
        height, width, _ = image.shape
        food_counts = Counter()
        
        print(f"📸 Creating annotated image for {len(annotations)} annotations")
        
        for ann in annotations:
            if "box_2d" not in ann or "label" not in ann:
                print(f"⚠ Skipping annotation missing box_2d or label: {ann}")
                continue
                
            ymin, xmin, ymax, xmax = ann["box_2d"]
            label = ann["label"].strip().lower()
            food_counts[label] += 1
            count = food_counts[label]
            
            # Scale coordinates
            x1 = int((xmin / 1000) * width)
            y1 = int((ymin / 1000) * height)
            x2 = int((xmax / 1000) * width)
            y2 = int((ymax / 1000) * height)
            
            # Draw bounding box in green (BGR format: Green = 0, 255, 0)
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 3)
            
            # Draw label background in green
            display_label = f"{label} ({count})" if food_counts[label] > 1 else label
            text_size = cv2.getTextSize(display_label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)[0]
            cv2.rectangle(image, (x1, y1 - text_size[1] - 10), 
                        (x1 + text_size[0], y1), (0, 255, 0), -1)
            
            # Draw label text in black for better visibility
            cv2.putText(image, display_label, (x1, y1 - 5), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
        
        # Save annotated image
        annotated_path = "data/annotated.jpg"
        cv2.imwrite(annotated_path, image)
        print(f"✅ Annotated image saved to: {annotated_path}")
        return annotated_path
        
    except Exception as e:
        print(f"❌ Error creating annotated image: {e}")
        traceback.print_exc()
        return None

def process_image(image_path, detect_food_items):
    print("🔍 Starting food detection...")
    
    annotations = detect_food_items(image_path)
    print(f"📊 Received {len(annotations)} annotations")
    
    if not annotations:
        error_msg = "⚠ No ingredients detected. Try another image."
        print(error_msg)
        return image_path, gr.CheckboxGroup(choices=[], value=[]), error_msg
    
    food_counts = Counter()
    for ann in annotations:
        if "label" in ann:
            label = ann["label"].strip().lower()
            food_counts[label] += 1
    print(f"📊 Food counts: {food_counts}")
    
    if not food_counts:
        error_msg = "⚠ No valid ingredients found."
        print(error_msg)
        return image_path, gr.CheckboxGroup(choices=[], value=[]), error_msg
    
    choices = [f"{item.title()} ({count})" for item, count in food_counts.items()]
    print(f"✅ Created {len(choices)} ingredient choices: {choices}")
    
    annotated_path = create_annotated_image(image_path, annotations)
    if not annotated_path:
        annotated_path = image_path
    
    success_msg = f"✅ Found {len(choices)} different items. Select below."
    print(success_msg)
    
    return annotated_path, gr.CheckboxGroup(choices=choices, value=[], label="Select Ingredients", interactive=True), success_msg

def upload_and_detect(file, detect_food_items):
    if file is None:
        return None, gr.CheckboxGroup(choices=[], value=[]), "⚠ Please upload an image."
    
    # Ensure the data directory exists
    os.makedirs("data", exist_ok=True)
    
    image_path = "data/uploaded.jpg"
    shutil.copy(file.name, image_path)
    return process_image(image_path, detect_food_items)