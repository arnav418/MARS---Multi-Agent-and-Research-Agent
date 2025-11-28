import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure the Gemini API client
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("Error: GEMINI_API_KEY not found in .env file.")
else:
    genai.configure(api_key=api_key)

    print("Checking for available Gemini models...")
    print("-" * 30)
    
    found_models = False
    for m in genai.list_models():
      if 'generateContent' in m.supported_generation_methods:
        print(f"- {m.name}")
        found_models = True
    
    if not found_models:
        print("No models found that support 'generateContent'.")
        print("Please check your API key and ensure the Generative Language API is enabled.")

    print("-" * 30)
