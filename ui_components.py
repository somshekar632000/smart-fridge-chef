import gradio as gr
from image_processor import upload_and_detect
from recipe_generator import get_recipes, show_recipe_details
from food_detector import detect_food_items
from utils import parse_recipe_sections  # Added import

class FoodieTheme(gr.themes.Base):
    def _init_custom_css(self):
        return """
        body {
            background: linear-gradient(135deg, rgba(245, 247, 246, 0.9) 0%, rgba(224, 230, 226, 0.9) 100%);
            font-family: 'Roboto', sans-serif;
            position: relative;
        }
        
        body::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: url('https://images.unsplash.com/photo-1490818387583-1baba5e638af?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1632&q=80') center/cover no-repeat;
            z-index: -1;
            opacity: 0.4;
        }
        
        .btn-primary {
            background: linear-gradient(135deg, #1a3c34 0%, #2e6b4e 100%) !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 12px 24px !important;
            color: white !important;
            font-family: 'Roboto', sans-serif !important;
            transition: all 0.3s ease !important;
        }
        .btn-primary:hover {
            transform: translateY(-2px) !important;
            background: linear-gradient(135deg, #153229 0%, #265b42 100%) !important;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2) !important;
        }
        .image-container {
            border-radius: 16px !important;
            box-shadow: 0 8px 20px rgba(0,0,0,0.1) !important;
            border: 2px solid #e0e6e2 !important;
        }
        .checkbox-group {
            background: linear-gradient(135deg, #1a3c34 0%, #2e6b4e 100%) !important;
            border-radius: 12px !important;
            padding: 20px !important;
            color: #e0e0e0 !important;
            font-family: 'Roboto', sans-serif !important;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
        }
        .radio-group {
            background: linear-gradient(135deg, #1a3c34 0%, #2e6b4e 100%) !important;
            border-radius: 12px !important;
            padding: 20px !important;
            color: #e0e0e0 !important;
            font-family: 'Roboto', sans-serif !important;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
        }
        .status-success {
            background: linear-gradient(135deg, #1a3c34 0%, #2e6b4e 100%) !important;
            color: #e0e0e0 !important;
            padding: 15px !important;
            border-radius: 12px !important;
            font-family: 'Roboto', sans-serif !important;
        }
        .status-error {
            background: linear-gradient(135deg, #d9534f 0%, #e27d7a 100%) !important;
            color: white !important;
            padding: 15px !important;
            border-radius: 12px !important;
            font-family: 'Roboto', sans-serif !important;
        }
        .textbox input {
            background: linear-gradient(135deg, #1a3c34 0%, #2e6b4e 100%) !important;
            color: #e0e0e0 !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 10px !important;
            font-family: 'Roboto', sans-serif !important;
        }
        .textbox input::placeholder {
            color: rgba(255, 255, 255, 0.7) !important;
        }
        .dropdown select {
            background: linear-gradient(135deg, #1a3c34 0%, #2e6b4e 100%) !important;
            color: #e0e0e0 !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 10px !important;
            font-family: 'Roboto', sans-serif !important;
        }
        .number input {
            background: linear-gradient(135deg, #1a3c34 0%, #2e6b4e 100%) !important;
            color: #e0e0e0 !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 10px !important;
            font-family: 'Roboto', sans-serif !important;
        }
        h1, h2, h3 {
            font-family: 'Playfair Display', serif !important;
        }
        .gr-column {
            margin: 0 auto !important;
            max-width: 1200px !important;
        }
        """

def create_gradio_interface():
    css = """
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Roboto:wght@300;400;700&display=swap');
    
    /* Background setup */
    .gradio-container::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background: url('https://images.unsplash.com/photo-1490818387583-1baba5e638af?ixlib=rb-4.0.3&ixid=M3wxMJA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1632&q=80') center/cover no-repeat;
        z-index: -1;
        opacity: 0.4;
    }
    
    body {
        background: linear-gradient(135deg, rgba(245, 247, 246, 0.85) 0%, rgba(224, 230, 226, 0.85) 100%) !important;
        position: relative;
    }
    
    /* Alternative background method */
    .gradio-container {
        background: linear-gradient(135deg, rgba(245, 247, 246, 0.85) 0%, rgba(224, 230, 226, 0.85) 100%), 
                    url('https://images.unsplash.com/photo-1490818387583-1baba5e638af?ixlib=rb-4.0.3&ixid=M3wxMJA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1632&q=80') center/cover no-repeat fixed !important;
        min-height: 100vh !important;
    }
    
    .green-button {
        background: linear-gradient(135deg, #1a3c34 0%, #2e6b4e 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 24px !important;
        font-family: 'Roboto', sans-serif !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
    }
    
    .green-button:hover {
        background: linear-gradient(135deg, #153229 0%, #265b42 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2) !important;
    }
    .white-text {
        color: #333 !important;
        font-family: 'Roboto', sans-serif !important;
        font-weight: 500 !important;
    }
    .gr-form > label {
        color: white !important;
    }
    .gr-group > .gr-form > label {
        color: white !important;
    }
    .gr-box > .gr-form > label {
        color: white !important;
    }
    fieldset > legend {
        color: white !important;
    }
    .gr-panel > .gr-form > label {
        color: white !important;
    }
    .green-box {
        background: linear-gradient(135deg, rgba(26, 60, 52, 0.9) 0%, rgba(46, 107, 78, 0.9) 100%) !important;
        border-radius: 12px !important;
        padding: 20px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
        color: #e0e0e0 !important;
        backdrop-filter: blur(10px) !important;
    }
    .black-title {
        color: #1a3c34 !important;
        text-align: center !important;
        font-family: 'Playfair Display', serif !important;
        font-weight: 700 !important;
        font-size: 48px !important;
        margin-bottom: 30px !important;
        text-shadow: 2px 2px 4px rgba(255,255,255,0.8) !important;
        background: rgba(255, 255, 255, 0.9) !important;
        padding: 20px !important;
        border-radius: 16px !important;
        backdrop-filter: blur(10px) !important;
    }
    .section-header {
        color: #1a3c34 !important;
        font-family: 'Playfair Display', serif !important;
        font-size: 28px !important;
        margin-bottom: 20px !important;
        text-shadow: 1px 1px 2px rgba(255,255,255,0.8) !important;
    }
    .gr-row {
        gap: 30px !important;
        margin-bottom: 30px !important;
    }
    .gr-column {
        background: rgba(255, 255, 255, 0.95) !important;
        border-radius: 16px !important;
        padding: 25px !important;
        box-shadow: 0 8px 20px rgba(0,0,0,0.15) !important;
        backdrop-filter: blur(15px) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }
    input[type="radio"]:checked {
        accent-color: #2e6b4e !important;
    }
    input[type="radio"] {
        accent-color: #2e6b4e !important;
    }
    
    /* Additional styling for better visibility */
    .image-container {
        border-radius: 16px !important;
        box-shadow: 0 8px 20px rgba(0,0,0,0.1) !important;
        border: 2px solid rgba(224, 230, 226, 0.8) !important;
        background: rgba(255, 255, 255, 0.9) !important;
    }
    
    /* Status box styling */
    .gr-textbox {
        background: rgba(255, 255, 255, 0.9) !important;
        border-radius: 12px !important;
        backdrop-filter: blur(10px) !important;
    }
    
    /* Number input styling */
    .gr-number input {
        background: rgba(26, 60, 52, 0.9) !important;
        color: #e0e0e0 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px !important;
    }
    
    /* Additional instructions textarea styling */
    .gr-textbox textarea {
        background: rgba(26, 60, 52, 0.9) !important;
        color: #e0e0e0 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 15px !important;
        font-family: 'Roboto', sans-serif !important;
        min-height: 80px !important;
        resize: vertical !important;
    }
    
    .gr-textbox textarea::placeholder {
        color: rgba(224, 224, 224, 0.7) !important;
        font-style: italic !important;
    }
    
    /* Credits section styling */
    .credits-section {
        margin-top: 50px !important;
        padding: 30px !important;
        background: rgba(255, 255, 255, 0.95) !important;
        border-radius: 16px !important;
        box-shadow: 0 8px 20px rgba(0,0,0,0.15) !important;
        backdrop-filter: blur(15px) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        text-align: center !important;
    }
    
    .credits-title {
        color: #1a3c34 !important;
        font-family: 'Playfair Display', serif !important;
        font-size: 28px !important;
        margin-bottom: 20px !important;
        text-shadow: 1px 1px 2px rgba(255,255,255,0.8) !important;
    }
    
    .developer-card {
        display: inline-block !important;
        margin: 10px 20px !important;
        padding: 20px !important;
        background: linear-gradient(135deg, rgba(26, 60, 52, 0.9) 0%, rgba(46, 107, 78, 0.9) 100%) !important;
        border-radius: 12px !important;
        color: #e0e0e0 !important;
        text-decoration: none !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
        min-width: 200px !important;
    }
    
    .developer-card:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 6px 20px rgba(0,0,0,0.2) !important;
        background: linear-gradient(135deg, rgba(21, 50, 41, 0.9) 0%, rgba(38, 91, 66, 0.9) 100%) !important;
    }
    
    .developer-name {
        font-family: 'Roboto', sans-serif !important;
        font-weight: 600 !important;
        font-size: 18px !important;
        margin-bottom: 8px !important;
        color: #e0e0e0 !important;
    }
    
    .linkedin-icon {
        font-size: 24px !important;
        color: #0077b5 !important;
        margin-top: 8px !important;
    }
    
    .credits-description {
        color: #666 !important;
        font-family: 'Roboto', sans-serif !important;
        font-size: 16px !important;
        margin-bottom: 25px !important;
        font-style: italic !important;
    }
    """
    
    with gr.Blocks(theme=FoodieTheme(), css=css) as demo:
        # Background HTML element
        gr.HTML("""
        <div style="position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; 
                    background: url('https://images.unsplash.com/photo-1490818387583-1baba5e638af?ixlib=rb-4.0.3&ixid=M3wxMJA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1632&q=80') center/cover no-repeat;
                    z-index: -999; opacity: 0.4; pointer-events: none;"></div>
        """)
        
        with gr.Column():
            gr.Markdown("<h1 class='black-title'>🍴 Smart Fridge Chef</h1>")
            gr.Markdown(
                "<div style='text-align: center; font-family: Roboto, sans-serif; color: #333; font-size: 18px; margin-bottom: 30px; background: rgba(255, 255, 255, 0.9); padding: 15px; border-radius: 12px; backdrop-filter: blur(10px);'>"
                "Transform your ingredients into delicious meals with AI-powered recipe suggestions!</div>"
            )
            with gr.Row():
                with gr.Column():
                    gr.Markdown("<h3 class='section-header'>🖼 Upload Your Ingredients</h3>")
                    upload_btn = gr.UploadButton("📸 Upload Image", file_types=["image"], elem_classes=["green-button"])
                    status = gr.Textbox(label="Status", interactive=False, elem_classes=["green-box"])
                    gr.Markdown("<h3 class='section-header'>🔍 Detected Ingredients</h3>")
                    annotated_output = gr.Image(label="Ingredient Detection", interactive=False, elem_classes=["image-container"])
                
                with gr.Column():
                    gr.Markdown("<h3 class='section-header'>🥗 Choose Ingredients</h3>")
                    ingredients_output = gr.CheckboxGroup(label="Ingredients", choices=[], interactive=True, elem_classes=["green-box"])
                    
                    gr.Markdown("<h3 class='section-header'>🍽 Dietary Preference</h3>")
                    diet_type = gr.Radio(["Vegetarian", "Non-Vegetarian"], label="Diet Type", value="Vegetarian", elem_classes=["green-box"])
                    
                    gr.Markdown("<h3 class='section-header'>🌍 Cuisine Style</h3>")
                    cuisine_type = gr.Radio(
                        ["Italian", "Japanese", "Chinese", "Middle Eastern", "Greek", "Mexican", "French", "Thai", "North Indian", "South Indian", "East Indian", "West Indian"],
                        label="Cuisine",
                        value="Italian",
                        elem_classes=["green-box"]
                    )
                    
                    gr.Markdown("<h3 class='section-header'>👥 Serving Size</h3>")
                    serving_size = gr.Number(label="Number of People", value=4, minimum=1, maximum=20, elem_classes=["green-box"])
                    
                    # NEW: Additional Instructions Section
                    gr.Markdown("<h3 class='section-header'>✏️ Additional Instructions</h3>")
                    additional_instructions = gr.Textbox(
                        label="Special Requirements (Optional)", 
                        placeholder="e.g., Make it spicy, gluten-free, low-calorie, one-pot cooking, kid-friendly, etc.",
                        lines=3,
                        elem_classes=["green-box"]
                    )
                    
                    generate_btn = gr.Button("🍳 Discover Recipes", elem_classes=["green-button"])
                    gr.Markdown("<h3 class='section-header'>📝 Select Recipe</h3>")
                    recipe_selector = gr.Radio(label="Choose Recipe", choices=[], interactive=True, elem_classes=["green-box"])
                    show_btn = gr.Button("👩‍🍳 View Full Recipe", elem_classes=["green-button"])
            
            gr.Markdown("<h2 class='section-header'>🍽 Your Recipe</h2>")
            with gr.Column():
                recipe_header_section = gr.HTML(label="Recipe Name")
                ingredients_section = gr.HTML(label="Ingredients")
                time_section = gr.HTML(label="Time")
                equipment_section = gr.HTML(label="Equipment")
                serving_section = gr.HTML(label="Nutrition")
                instructions_section = gr.HTML(label="Instructions")
                tips_section = gr.HTML(label="Tips")
            
            # Developer Credits Section
            gr.HTML("""
            <div class="credits-section">
                <h3 class="credits-title">👨‍💻 Developed By</h3>
                <p class="credits-description">Built with passion by our talented development team</p>
                <div style="display: flex; justify-content: center; flex-wrap: wrap; gap: 20px;">
                    <a href="https://www.linkedin.com/in/somshekar-m/" target="_blank" class="developer-card">
                        <div class="developer-name">Somshekar M</div>
                        <div class="linkedin-icon">🔗 LinkedIn</div>
                    </a>
                    <a href="https://www.linkedin.com/in/varun-gambhir-903b741b0/" target="_blank" class="developer-card">
                        <div class="developer-name">Varun Gambhir</div>
                        <div class="linkedin-icon">🔗 LinkedIn</div>
                    </a>
                </div>
            </div>
            """)

        upload_btn.upload(
            fn=lambda file: upload_and_detect(file, detect_food_items),
            inputs=[upload_btn],
            outputs=[annotated_output, ingredients_output, status]
        )
        
        generate_btn.click(
            fn=get_recipes,
            inputs=[ingredients_output, diet_type, cuisine_type, serving_size, additional_instructions],
            outputs=[recipe_selector]
        )
        
        show_btn.click(
            fn=lambda *args: show_recipe_details(*args, parse_recipe_sections),
            inputs=[recipe_selector, ingredients_output, diet_type, cuisine_type, serving_size, additional_instructions],
            outputs=[recipe_header_section, ingredients_section, time_section, equipment_section, serving_section, instructions_section, tips_section]
        )
    
    return demo

# Run the interface
if __name__ == "__main__":
    demo = create_gradio_interface()
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=True,
        debug=True
    )
    