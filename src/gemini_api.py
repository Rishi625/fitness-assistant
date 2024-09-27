import os
import google.generativeai as genai

genai.configure(api_key=os.environ['GEMINI_API_KEY'])


class GeminiApi:
    def __init__(self):
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def generate_response(self, prompt):
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"An error occurred while generating response: {e}")
            return None