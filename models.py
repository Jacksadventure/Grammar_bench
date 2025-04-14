from langchain_ollama import OllamaLLM
from openai import OpenAI
from google import genai
import re
import os
class OllamaModel:
    def __init__(self,model_name:str):
            self.model = OllamaLLM(model=model_name)

    def get_response(self, prompt: str, text: str):
        message = [
            {
                "role": "system",
                "content": prompt
            },
            {
                "role": "user",
                "content": text
            }
        ]
        response = self.model.invoke(message)
        return response

class OpenAIModel:
    def __init__(self, model):
        self.client = OpenAI()  
        self.model = model
    
    def get_response(self, prompt: str, text: str):
        if "o1" in self.model or "o3" in self.model:
            messages=[ 
                {"role": "user", "content": prompt+"\n"+text},
            ]
        else:
            messages=[ 
                {"role": "system", "content": prompt},
                {"role": "user", "content": text},
            ]
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
        )
        return completion.choices[0].message.content

class Gemini:
    def __init__(self, model):
        api_key = os.getenv("GOOGLE_GENAI_API_KEY")
        self.client = genai.Client(api_key=api_key)
        self.model = model
    def get_response(self, prompt: str, text: str):
        response = self.client.models.generate_content(
            model = self.model,
            contents = prompt + "\n" + text
        ).text
        return response