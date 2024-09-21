import os
import google.generativeai as genai

class GeminiApi:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is not set")
        genai.configure(api_key=api_key)

    def generate_response(self, prompt):
        try:
            response = genai.generate_text(prompt=prompt)
            return response.result
        except Exception as e:
            print(f"An error occurred while generating response: {e}")
            return None