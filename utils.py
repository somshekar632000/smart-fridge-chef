import re
from collections import Counter

def count_food_items(annotations):
    food_counts = Counter()
    for ann in annotations:
        if "label" in ann:
            label = ann["label"].strip().lower()
            food_counts[label] += 1
    return food_counts

def parse_recipe_sections(recipe_text):
    sections = {
        'ingredients': '',
        'prep_time': '',
        'cook_time': '',
        'equipment': '',
        'serving_size': '',
        'calories': '',
        'instructions': '',
        'tips': ''
    }
    
    current_section = None
    lines = recipe_text.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        line = re.sub(r'\*+', '', line)
        
        if 'INGREDIENTS:' in line.upper():
            current_section = 'ingredients'
            continue
        elif 'PREP TIME:' in line.upper():
            current_section = 'prep_time'
            continue
        elif 'COOK TIME:' in line.upper():
            current_section = 'cook_time'
            continue
        elif 'EQUIPMENT NEEDED:' in line.upper():
            current_section = 'equipment'
            continue
        elif 'SERVING SIZE:' in line.upper():
            current_section = 'serving_size'
            continue
        elif 'CALORIES:' in line.upper():
            current_section = 'calories'
            continue
        elif 'INSTRUCTIONS:' in line.upper():
            current_section = 'instructions'
            continue
        elif 'TIPS FOR SUCCESS:' in line.upper():
            current_section = 'tips'
            continue
        elif current_section:
            if sections[current_section]:
                sections[current_section] += '\n' + line
            else:
                sections[current_section] = line
    
    return sections