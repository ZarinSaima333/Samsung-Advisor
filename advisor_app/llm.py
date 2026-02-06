# llm.py

import os
import time
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

MODEL_NAME = "models/gemini-2.5-flash"

# Configure safety settings
safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE"
    }
]

generation_config = {
    "temperature": 0.7,
    "top_p": 0.8,
    "top_k": 40,
    "max_output_tokens": 1024,
}

model = genai.GenerativeModel(
    model_name=MODEL_NAME,
    safety_settings=safety_settings,
    generation_config=generation_config
)

def generate_answer(prompt: str, max_retries: int = 3) -> str:
    """
    Generates natural language output using Gemini with retry logic
    """
    for attempt in range(max_retries):
        try:
            response = model.generate_content(prompt)
            if response and hasattr(response, 'text'):
                return response.text.strip()
            elif response and hasattr(response, 'parts'):
                return "".join([part.text for part in response.parts]).strip()
            else:
                raise ValueError("Invalid response format")
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {str(e)}")
            if attempt < max_retries - 1:
                wait_time = (attempt + 1) * 2
                print(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                return "Sorry, I couldn't generate a response at this time. Please try again."

