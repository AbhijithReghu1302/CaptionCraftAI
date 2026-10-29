# CaptionCraft AI ✨

**An AI-powered social media caption generator built with Python, Streamlit, and Gemma 3.**

## About the Project

CaptionCraft AI helps users generate engaging social media captions based on uploaded images. Users can choose a mood, caption style, length, and language to create captions suited to their posts.

## Features

- Upload images in JPG, JPEG, and PNG formats.
- Generate captions based on image content using a vision-language model.
- Choose from different moods, including aesthetic, funny, savage, poetic, romantic, motivational, and casual.
- Generate simple, creative, or mixed caption styles.
- Select caption length and language.
- Generate relevant hashtags.
- Download generated captions as a text file.

## Technologies Used

- Python
- Streamlit
- Ollama
- Gemma 3 4B
- Pillow

## How It Works

1. The user uploads an image.
2. The user selects caption preferences.
3. Gemma 3 analyzes the image and generates captions.
4. The application displays caption options and hashtags.
5. The user can copy or download the generated results.

## Installation and Setup

### Prerequisites

- Python installed on your computer
- Ollama installed
- The `gemma3:4b` model downloaded locally

### Steps

1. Clone this repository:

   ```bash
   git clone YOUR_REPOSITORY_URL
   cd CaptionCraftAI
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   ```

   On Windows PowerShell:

   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Download the model if it is not already installed:

   ```bash
   ollama pull gemma3:4b
   ```

5. Start the application:

   ```bash
   python -m streamlit run app.py
   ```

6. Open the local URL displayed in your terminal, usually `http://localhost:8501`.

## AI Model

CaptionCraft AI uses Gemma 3 4B through Ollama for local image understanding and text generation. The application is designed to run without a paid AI API.

## Academic Project

Developed as a mini project for the AI Tools subject.

**Note:** Generated captions may occasionally be inaccurate and should be reviewed before posting.