# Smart Fridge Chef 🍳

An AI-powered web application that transforms your kitchen ingredients into delicious, personalized recipes. Simply upload an image of your ingredients, and let Smart Fridge Chef suggest tailored recipes based on your dietary preferences, cuisine style, and serving size.

## ✨ Features

- **🔍 Intelligent Ingredient Detection**: Upload an image and leverage Google's Gemini API to automatically identify ingredients with precise bounding box annotations
- **📝 Personalized Recipe Suggestions**: Generate up to 5 recipe recommendations based on:
  - Detected ingredients
  - Cuisine preferences (Italian, Japanese, Mexican, etc.)
  - Dietary requirements (Vegetarian/Non-Vegetarian)
  - Serving size
- **📖 Comprehensive Recipe Details**: Get complete recipes with:
  - Full ingredient lists
  - Prep and cook times
  - Required equipment
  - Nutritional information (calories per serving)
  - Step-by-step instructions
  - Pro tips for success
- **🎯 Custom Requirements**: Add special instructions like "spicy", "gluten-free", or "kid-friendly"
- **🖼️ Visual Annotations**: View your uploaded image with labeled ingredient bounding boxes
- **💫 Modern UI**: Sleek, responsive interface with food-themed design

## 🏗️ Project Structure

```
smart-fridge-chef/
│
├── food_detector.py      # Ingredient detection using Gemini API
├── image_processor.py    # Image processing and annotation creation
├── main.py               # Gradio application launcher
├── recipe_generator.py   # Recipe suggestion and detail generation
├── ui_components.py      # Gradio UI components and custom theming
├── utils.py              # Utility functions for parsing and data processing
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variables template
├── README.md            # Project documentation
└── LICENSE              # MIT License file
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))
- Stable internet connection

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/smart-fridge-chef.git
   cd smart-fridge-chef
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   Edit the `.env` file and add your Gemini API key:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

5. **Launch the application**
   ```bash
   python main.py
   ```

6. **Access the app**
   Open your browser and navigate to `http://localhost:7860`

## 📖 Usage Guide

### Step 1: Upload Your Ingredients
- Click the **"Upload Image"** button
- Select a clear photo of your available ingredients
- Ensure good lighting and visibility of items

### Step 2: Review Detected Ingredients
- View the annotated image with labeled bounding boxes
- Check the list of automatically detected ingredients
- Manually select/deselect ingredients as needed

### Step 3: Set Your Preferences
- **Dietary Type**: Choose Vegetarian or Non-Vegetarian
- **Cuisine Style**: Select from Italian, Japanese, Mexican, Indian, etc.
- **Serving Size**: Specify number of people (1-8)
- **Special Instructions**: Add requirements like "make it spicy", "gluten-free", "low-carb", etc.

### Step 4: Generate Recipes
- Click **"Discover Recipes"** to get 5 personalized suggestions
- Browse through the recipe titles and descriptions

### Step 5: View Full Recipe Details
- Select your preferred recipe
- Click **"View Full Recipe"** for complete instructions
- Get ingredient quantities, cooking steps, and helpful tips

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GEMINI_API_KEY` | Your Google Gemini API key | Yes |

### Supported Image Formats

- JPEG (.jpg, .jpeg)
- PNG (.png)
- WebP (.webp)
- Maximum file size: 20MB

## ⚠️ Known Limitations

- **Camera Support**: Direct camera capture not supported on Windows systems
- **API Dependency**: Requires active internet connection and valid Gemini API key
- **Detection Accuracy**: Ingredient identification depends on image quality and lighting conditions
- **Cuisine Options**: Limited to predefined cuisine types
- **Dietary Categories**: Currently supports only Vegetarian/Non-Vegetarian classifications

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/

# Format code
black .
flake8 .
```

## 🐛 Bug Reports & Feature Requests

Please use the [GitHub Issues](https://github.com/your-username/smart-fridge-chef/issues) page to:
- Report bugs
- Request new features
- Ask questions
- Suggest improvements

## 📊 Roadmap

- [ ] Support for more dietary restrictions (Vegan, Keto, Paleo)
- [ ] Recipe rating and favorites system
- [ ] Shopping list generation
- [ ] Nutritional analysis improvements
- [ ] Mobile app development
- [ ] Multi-language support
- [ ] Recipe sharing community

## 🙏 Acknowledgments

- Google Gemini API for powerful AI capabilities
- Gradio team for the excellent UI framework
- OpenCV community for image processing tools
- All contributors and users of Smart Fridge Chef

## 👥 Authors

**Built with passion by:**
- **Somshekar M**
- **Varun Gambhir**

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.