FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies for opencv-python
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Expose port for Gradio (default is 7860)
EXPOSE 7860

# Set environment variable for Gradio to allow external access
ENV GRADIO_SERVER_NAME=0.0.0.0

# Command to run the Gradio app
CMD ["python", "main.py"]