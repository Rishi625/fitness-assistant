import google.generativeai as genai
import os

class GeminiApi:
    def gemini_api(self):
        genai.configure(api_key=os.environ["API_Key"])
        response = genai.generate_text(prompt="write a story about andrej karpathy")
        return response.result

gemini_api_instance = GeminiApi()
output = gemini_api_instance.gemini_api()
print(output)