"""AIInterface: Lazy-load model implementations for different backends."""

class AIInterface:
    def __init__(self, backend, model: str):
        if backend == "ollama":
            from models import OllamaModel
            self.model = OllamaModel(model)
        elif backend == "openai":
            from models import OpenAIModel
            self.model = OpenAIModel(model)
        elif backend == "gemini":
            from models import Gemini
            self.model = Gemini(model)
        else:
            raise ValueError("Invalid backend")
        
    def get_response(self, prompt: str, text: str):
        return self.model.get_response(prompt, text)

 