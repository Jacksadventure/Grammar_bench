from langchain_ollama import OllamaLLM
from openai import OpenAI
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
    def __init__(model,self):
        self.client =  OpenAI(model)
        self.model = model
    
    def get_response(self, prompt: str, text: str):
        completion = self.client().complete(
             model=self.model,
             messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": text},
             ]
        )
        return completion.choices[0].message['content']
      