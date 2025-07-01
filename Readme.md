Smart Fridge Chef
Overview
Smart Fridge Chef is an AI-powered web application that transforms your kitchen ingredients into delicious, personalized recipes. By uploading an image of your ingredients, the app uses advanced computer vision to detect food items and suggests tailored recipes based on your dietary preferences, cuisine style, and serving size. Built with a sleek Gradio interface, it offers an intuitive user experience for home cooks looking to create meals from what’s in their fridge.
Features

Ingredient Detection: Upload an image, and the app uses Google’s Gemini API to identify prominent ingredients with bounding box annotations.
Recipe Suggestions: Generate up to five recipe names based on detected ingredients, cuisine type (e.g., Italian, Japanese, Mexican), dietary preferences (Vegetarian or Non-Vegetarian), and serving size.
Detailed Recipes: View comprehensive recipe details, including ingredients, prep/cook times, equipment needed, calories per serving, step-by-step instructions, and tips for success.
Custom Instructions: Add special requirements like "spicy," "gluten-free," or "kid-friendly" to tailor recipes.
Visual Annotations: Display detected ingredients with labeled bounding boxes on the uploaded image.
User-Friendly Interface: A modern, responsive UI with a food-themed design, built using Gradio and custom CSS.

Directory Structure
├── food_detector.py       # Handles ingredient detection using Gemini API
├── image_processor.py     # Processes images and creates annotated outputs
├── main.py               # Launches the Gradio interface
├── recipe_generator.py    # Generates recipe suggestions and details
├── ui_components.py       # Defines the Gradio UI and custom theme
└── utils.py              # Utility functions for parsing and counting

Installation

Clone the Repository:
git clone https://github.com/your-repo/smart-fridge-chef.git
cd smart-fridge-chef


Install Dependencies:Ensure Python 3.8+ is installed, then install the required packages:
pip install -r requirements.txt

Required packages include:

google-generativeai
opencv-python
gradio
python-dotenv


Set Up Environment Variables:Create a .env file in the project root and add your Gemini API key:
GEMINI_API_KEY=your_api_key_here


Run the Application:Launch the Gradio interface:
python main.py

The app will be available at http://0.0.0.0:7860.


Usage

Upload an Image: Use the "Upload Image" button to upload a photo of your ingredients.
View Detected Ingredients: The app displays an annotated image with labeled bounding boxes and a list of detected ingredients.
Select Preferences: Choose ingredients, dietary type, cuisine style, serving size, and add optional instructions (e.g., "make it spicy").
Generate Recipes: Click "Discover Recipes" to get a list of five recipe suggestions.
View Recipe Details: Select a recipe and click "View Full Recipe" to see detailed instructions, ingredients, and more.

Limitations

Camera Support: Camera capture is not supported on Windows; users must upload images manually.
API Dependency: Requires a valid Gemini API key and internet connection.
Image Quality: Ingredient detection accuracy depends on image clarity and lighting.
Cuisine and Diet: Limited to predefined cuisine types and Vegetarian/Non-Vegetarian diets.

Developers
Built with passion by:

Somshekar M
Varun Gambhir

License
This project is licensed under the MIT License. See the LICENSE file for details.