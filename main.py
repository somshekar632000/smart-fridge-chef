import gradio as gr
from ui_components import FoodieTheme, create_gradio_interface
from image_processor import process_image, upload_and_detect
from recipe_generator import get_recipes, show_recipe_details
from utils import parse_recipe_sections

if __name__ == "__main__":
    try:
        demo = create_gradio_interface()
        demo.launch(server_name="0.0.0.0", server_port=7860, share=False)
    except Exception as e:
        print(f"❌ Failed to launch Gradio: {e}")
        print("Try running on localhost with: demo.launch()")