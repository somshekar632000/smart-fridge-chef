from google.generativeai import GenerativeModel
import re
import gradio as gr

def generate_recipe_suggestions(selected_ingredients, diet_type, cuisine_type, serving_size):
    if not selected_ingredients:
        return []
    
    ingredients_list = [f"{count} {item}{'s' if count > 1 else ''}" 
                       for item, count in selected_ingredients.items()]
    ingredients_text = ", ".join(ingredients_list)
    
    diet_specification = ""
    if diet_type == "Vegetarian":
        diet_specification = "strictly vegetarian (no meat, fish, or poultry)"
    elif diet_type == "Non-Vegetarian":
        diet_specification = "can include meat, fish, or poultry"
    
    prompt = f"""
    Suggest exactly 5 {diet_specification} {cuisine_type} recipe names using these ingredients: {ingredients_text}.
    The recipes should serve {serving_size} people.
    
    Requirements:
    - Recipes must be {diet_specification}
    - Must follow {cuisine_type} cuisine style and flavors
    - Should use 2-3 main detected ingredients
    - Assume common pantry staples are available
    - Be practical for home cooking
    - Suitable for serving {serving_size} people
    - ONLY provide recipe names, no descriptions or explanations
    
    Format as a simple numbered list with only recipe names:
    1. Recipe Name 1
    2. Recipe Name 2
    3. Recipe Name 3
    4. Recipe Name 4
    5. Recipe Name 5
    """
    try:
        model = GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(prompt)
        
        recipe_names = []
        for line in response.text.strip().split('\n'):
            line = line.strip()
            if line and re.match(r'^\d+\.\s', line):
                name = re.sub(r'^\d+\.\s*', '', line).strip()
                recipe_names.append(name)
        return recipe_names[:5]
    except Exception as e:
        print(f"❌ Recipe suggestion error: {e}")
        return []

def generate_detailed_recipe(recipe_name, selected_ingredients, diet_type, cuisine_type, serving_size):
    ingredients_list = [f"{count} {item}{'s' if count > 1 else ''}" 
                       for item, count in selected_ingredients.items()]
    ingredients_text = ", ".join(ingredients_list)
    
    diet_specification = ""
    if diet_type == "Vegetarian":
        diet_specification = "strictly vegetarian (no meat, fish, or poultry)"
    elif diet_type == "Non-Vegetarian":
        diet_specification = "can include meat, fish, or poultry"
    
    time_adjustment = ""
    if serving_size > 6:
        time_adjustment = "Increase cooking time by 15-25% for larger quantities."
    elif serving_size < 3:
        time_adjustment = "Reduce cooking time by 10-15% for smaller quantities."
    else:
        time_adjustment = "Standard cooking times apply."
    
    prompt = f"""
    Create a detailed {diet_specification} {cuisine_type} recipe for "{recipe_name}" using: {ingredients_text}.
    The recipe should serve {serving_size} people.
    
    Structure the response with these exact sections using simple text formatting (NO asterisks, NO markdown symbols):
    
    INGREDIENTS:
    List all ingredients with quantities scaled for {serving_size} servings, marking which are from detected ingredients and which are additional. Follow {cuisine_type} cuisine traditions.
    
    PREP TIME:
    Just the number of minutes for preparation (adjust for serving {serving_size} people)
    
    COOK TIME:
    Just the number of minutes for cooking (adjust for serving {serving_size} people - {time_adjustment})
    
    EQUIPMENT NEEDED:
    List all kitchen tools and equipment needed for {cuisine_type} cooking
    
    SERVING SIZE:
    Confirm this recipe serves {serving_size} people
    
    CALORIES:
    Approximate calories per single serving (not total)
    
    INSTRUCTIONS:
    Numbered step-by-step cooking instructions following {cuisine_type} cooking techniques and methods (timing adjusted for {serving_size} servings)
    
    TIPS FOR SUCCESS:
    Helpful tips and variations specific to {cuisine_type} cuisine
    
    Requirements:
    - Recipe must be {diet_specification}
    - Follow authentic {cuisine_type} flavors and techniques
    - Scale all ingredients and timing for {serving_size} servings
    - Provide nutrition information per single serving only
    - Do not use any asterisks, bold formatting, or markdown symbols
    - Use plain text formatting only
    """
    try:
        model = GenerativeModel('gemini-2.5-pro')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ Error generating recipe: {e}"

def mark_additional_ingredients(ingredients_text, selected_ingredients):
    """
    Mark ingredients that are not in the original selected ingredients list with (Additional)
    """
    # Create a set of original ingredient names (normalized to lowercase)
    original_ingredients = set()
    for ingredient in selected_ingredients.keys():
        # Remove common plurals and normalize
        normalized = ingredient.lower().strip()
        original_ingredients.add(normalized)
        # Also add singular/plural variants
        if normalized.endswith('s'):
            original_ingredients.add(normalized[:-1])
        else:
            original_ingredients.add(normalized + 's')
    
    # Process each line of ingredients
    lines = ingredients_text.split('\n')
    processed_lines = []
    
    for line in lines:
        if line.strip():
            # Skip if already marked as additional ingredient
            if "(additional ingredient)" in line.lower():
                # Replace "(additional ingredient)" with just "(Additional)"
                processed_line = re.sub(r'\s*\(additional ingredient\)', ' (Additional)', line, flags=re.IGNORECASE)
                processed_lines.append(processed_line)
                continue
            
            # Skip if already has (Additional) marker
            if "(Additional)" in line:
                processed_lines.append(line)
                continue
            
            # Extract ingredient name from the line (after quantity and before any description)
            # This regex tries to match common ingredient line patterns
            ingredient_match = re.search(r'(?:\d+\s*(?:cups?|tbsp|tsp|tablespoons?|teaspoons?|lbs?|oz|cloves?|pieces?|medium|large|small)?\s+)([a-zA-Z\s]+?)(?:\s*[\(,]|$)', line)
            
            if ingredient_match:
                ingredient_name = ingredient_match.group(1).strip().lower()
                
                # Check if this ingredient (or its variants) is in original ingredients
                is_original = False
                for orig_ingredient in original_ingredients:
                    # More precise matching
                    if (ingredient_name in orig_ingredient or 
                        orig_ingredient in ingredient_name or
                        # Check for key words matching
                        any(word in orig_ingredient for word in ingredient_name.split() if len(word) > 2) or
                        any(word in ingredient_name for word in orig_ingredient.split() if len(word) > 2)):
                        is_original = True
                        break
                
                # If not found in original ingredients and doesn't already have parentheses, mark as additional
                if not is_original and "(" not in line:
                    line = line + " (Additional)"
                elif not is_original and "(" in line:
                    # If ingredient is not original but already has parentheses, add (Additional) before the last closing parenthesis
                    line = re.sub(r'\)([^)]*$)', r') (Additional)\1', line)
            
            processed_lines.append(line)
        else:
            processed_lines.append(line)
    
    return '\n'.join(processed_lines)

def get_recipes(selected_ingredients, diet_type, cuisine_type, serving_size):
    if not selected_ingredients:
        return gr.Radio(choices=[], value=None, label="⚠ Please select ingredients first")
    
    if not serving_size or serving_size <= 0:
        return gr.Radio(choices=[], value=None, label="⚠ Please enter a valid serving size")
    
    counts = {}
    for item in selected_ingredients:
        name = re.sub(r'\s*\(\d+\)$', '', item).lower()
        counts[name] = counts.get(name, 0) + 1
    
    recipes = generate_recipe_suggestions(counts, diet_type, cuisine_type, serving_size)
    if not recipes:
        return gr.Radio(choices=[], value=None, label="⚠ No recipes generated")
    
    return gr.Radio(choices=recipes, value=None, label="Choose Recipe", interactive=True)

def show_recipe_details(recipe_name, selected_ingredients, diet_type, cuisine_type, serving_size, parse_recipe_sections):
    if not recipe_name:
        return (
            gr.HTML(""), gr.HTML(""), gr.HTML(""), 
            gr.HTML(""), gr.HTML(""), gr.HTML(""), gr.HTML("")
        )
    
    if not serving_size or serving_size <= 0:
        return (
            gr.HTML("<div style='color: red;'>⚠ Please enter a valid serving size.</div>"), 
            gr.HTML(""), gr.HTML(""), gr.HTML(""), gr.HTML(""), gr.HTML(""), gr.HTML("")
        )
    
    counts = {}
    for item in selected_ingredients:
        name = re.sub(r'\s*\(\d+\)$', '', item).lower()
        counts[name] = counts.get(name, 0) + 1
    
    detailed_recipe = generate_detailed_recipe(recipe_name, counts, diet_type, cuisine_type, serving_size)
    sections = parse_recipe_sections(detailed_recipe)
    
    # Mark additional ingredients that weren't in the original selection
    sections['ingredients'] = mark_additional_ingredients(sections['ingredients'], counts)
    
    recipe_header_html = f"""
    <div style='background: linear-gradient(135deg, #1a3c34 0%, #2e6b4e 100%); color: white; padding: 30px; border-radius: 20px; box-shadow: 0 6px 20px rgba(0,0,0,0.15); margin-bottom: 25px; text-align: center;'>
        <h2 style='margin: 0; font-size: 32px; font-family: "Playfair Display", serif; display: flex; align-items: center; justify-content: center; color: white;'>
            <span style='margin-right: 15px; font-size: 40px;'>🍴</span>{recipe_name}
        </h2>
        <p style='margin: 10px 0 0 0; font-size: 18px; font-family: "Roboto", sans-serif; color: #e0e0e0;'>
            {diet_type} • {cuisine_type} • Serves {serving_size}
        </p>
    </div>
    """
    
    ingredients_html = f"""
    <div style='background: linear-gradient(135deg, #1a3c34 0%, #2e6b4e 100%); color: white; padding: 25px; border-radius: 20px; box-shadow: 0 6px 20px rgba(0,0,0,0.15); margin-bottom: 20px;'>
        <h3 style='margin: 0 0 15px 0; font-size: 24px; font-family: "Playfair Display", serif; display: flex; align-items: center; color: white;'>
            <span style='margin-right: 10px; font-size: 28px;'>🥗</span>Ingredients
        </h3>
        <div style='line-height: 1.8; font-size: 16px; font-family: "Roboto", sans-serif; color: #e0e0e0;'>{sections['ingredients'].replace('\n', '<br>')}</div>
    </div>
    """
    
    time_html = f"""
    <div style='background: linear-gradient(135deg, #1a3c34 0%, #2e6b4e 100%); color: white; padding: 25px; border-radius: 20px; box-shadow: 0 6px 20px rgba(0,0,0,0.15); margin-bottom: 20px;'>
        <h3 style='margin: 0 0 15px 0; font-size: 24px; font-family: "Playfair Display", serif; display: flex; align-items: center; color: white;'>
            <span style='margin-right: 10px; font-size: 28px; color: #e0e0e0;'>⏱</span>Time
        </h3>
        <div style='line-height: 1.8; font-size: 16px; font-family: "Roboto", sans-serif; color: #e0e0e0;'>
            <strong style='color: #e0e0e0;'>Prep:</strong> {sections['prep_time']} minutes<br>
            <strong style='color: #e0e0e0;'>Cook:</strong> {sections['cook_time']} minutes
        </div>
    </div>
    """
    
    equipment_html = f"""
    <div style='background: linear-gradient(135deg, #1a3c34 0%, #2e6b4e 100%); color: white; padding: 25px; border-radius: 20px; box-shadow: 0 6px 20px rgba(0,0,0,0.15); margin-bottom: 20px;'>
        <h3 style='margin: 0 0 15px 0; font-size: 24px; font-family: "Playfair Display", serif; display: flex; align-items: center; color: white;'>
            <span style='margin-right: 10px; font-size: 28px;'>🔧</span>Equipment
        </h3>
        <div style='line-height: 1.8; font-size: 16px; font-family: "Roboto", sans-serif; color: #e0e0e0;'>{sections['equipment'].replace('\n', '<br>')}</div>
    </div>
    """
    
    serving_html = f"""
    <div style='background: linear-gradient(135deg, #1a3c34 0%, #2e6b4e 100%); color: white; padding: 25px; border-radius: 20px; box-shadow: 0 6px 20px rgba(0,0,0,0.15); margin-bottom: 20px;'>
        <h3 style='margin: 0 0 15px 0; font-size: 24px; font-family: "Playfair Display", serif; display: flex; align-items: center; color: white;'>
            <span style='margin-right: 10px; font-size: 28px; color: #e0e0e0;'>🍽</span>Nutrition (Per Serving)
        </h3>
        <div style='line-height: 1.8; font-size: 16px; font-family: "Roboto", sans-serif; color: #e0e0e0;'>
            <strong style='color: #e0e0e0;'>Cook:</strong> {sections['cook_time']} minutes
            <strong style='color: #e0e0e0;'>Calories per serving:</strong> {sections['calories']}
        </div>
    </div>
    """
    
    instructions_html = f"""
    <div style='background: linear-gradient(135deg, #1a3c34 0%, #2e6b4e 100%); color: white; padding: 30px; border-radius: 20px; box-shadow: 0 6px 20px rgba(0,0,0,0.15); margin-bottom: 20px;'>
        <h3 style='margin: 0 0 20px 0; font-size: 24px; font-family: "Playfair Display", serif; display: flex; align-items: center; color: white;'>
            <span style='margin-right: 10px; font-size: 28px;'>📝</span>Instructions
        </h3>
        <div style='line-height: 1.9; font-size: 16px; font-family: "Roboto", sans-serif; color: #e0e0e0;'>{sections['instructions'].replace('\n', '<br>')}</div>
    </div>
    """
    
    tips_html = f"""
    <div style='background: linear-gradient(135deg, #1a3c34 0%, #2e6b4e 100%); color: white; padding: 25px; border-radius: 20px; box-shadow: 0 6px 20px rgba(0,0,0,0.15);'>
        <h3 style='margin: 0 0 15px 0; font-size: 24px; font-family: "Playfair Display", serif; display: flex; align-items: center; color: white;'>
            <span style='margin-right: 10px; font-size: 28px;'>💡</span>Tips for Success
        </h3>
        <div style='line-height: 1.8; font-size: 16px; font-family: "Roboto", sans-serif; color: #e0e0e0;'>{sections['tips'].replace('\n', '<br>')}</div>
    </div>
    """
    
    return recipe_header_html, ingredients_html, time_html, equipment_html, serving_html, instructions_html, tips_html