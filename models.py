from langchain_ollama import OllamaLLM
from openai import OpenAI
import re

def remove_think_tags(text):
    return re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)

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
        if self.model == "deepseek-r1:70b":
            response = remove_think_tags(response)
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
      