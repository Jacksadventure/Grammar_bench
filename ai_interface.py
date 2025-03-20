from models import OpenAIModel, OllamaModel, Gemini

class AIInterface:
    def __init__(self,backend,model: str):
        if backend == "ollama":
            self.model = OllamaModel(model)
        elif backend == "openai":
            self.model = OpenAIModel(model)
        elif backend == "gemini":
            self.model = Gemini(model)
        else:
            raise ValueError("Invalid backend")
        
    def get_response(self, prompt: str, text: str):
        return self.model.get_response(prompt, text)

 