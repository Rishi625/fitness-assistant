from src.gemini_api import GeminiApi

gemini = GeminiApi()
response = gemini.generate_response("tell me about kamla harris")
print(f"Gemini's response: {response}")