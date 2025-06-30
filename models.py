from ollama import Client       # 使用官方 Ollama Python 客户端 [oai_citation:0‡pypi.org](https://pypi.org/project/ollama/?utm_source=chatgpt.com) [oai_citation:1‡github.com](https://github.com/ollama/ollama-python?utm_source=chatgpt.com)
import os
import re
from openai import OpenAI
from google import genai
import anthropic
from together import Together

class response_body:
    def __init__(self, response_text: str,
                 prompt_tokens: int,
                 completion_tokens: int,
                 total_tokens: int):
        self.response_text = response_text
        self.prompt_tokens = prompt_tokens
        self.completion_tokens = completion_tokens
        self.total_tokens = total_tokens

class OllamaModel:
    def __init__(self, model_name: str):
        self.client = Client()       
        self.model_name = model_name

    def get_response(self, prompt: str, text: str):
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user",   "content": text}
        ]
        raw = self.client.chat(
            model=self.model_name,
            messages=messages,
            stream=False
        )
        prompt_tokens     = raw.get("prompt_eval_count", 0)
        completion_tokens = raw.get("eval_count", 0)
        total_tokens      = prompt_tokens + completion_tokens

        return response_body(
            raw["message"]["content"],
            prompt_tokens,
            completion_tokens,
            total_tokens
        )

class OpenAIModel:
    def __init__(self, model):
        self.client = OpenAI()
        self.model = model

    def get_response(self, prompt: str, text: str):
        if "o1" in self.model or "o3" in self.model:
            messages = [{"role": "user", "content": prompt + "\n" + text}]
        else:
            messages = [
                {"role": "system", "content": prompt},
                {"role": "user", "content": text},
            ]
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
        )
        return response_body(
            completion.choices[0].message.content,
            completion.usage.prompt_tokens,
            completion.usage.completion_tokens,
            completion.usage.total_tokens
        )

class Gemini:
    def __init__(self, model):
        api_key = os.getenv("GOOGLE_GENAI_API_KEY")
        self.client = genai.Client(api_key=api_key)
        self.model = model

    def get_response(self, prompt: str, text: str):
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt + "\n" + text
        )
        return response_body(
            response.text,
            response.usage_metadata.prompt_token_count,
            response.usage_metadata.candidates_token_count,
            response.usage_metadata.total_token_count
        )

class ClaudeModel:
    def __init__(self, model):
        api_key = os.getenv("ANTHROPIC_API_KEY")
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model

    def get_response(self, prompt: str, text: str):
        response = self.client.messages.create(
            model=self.model,
            system=prompt,
            max_tokens=10000,
            messages=[{
                "role": "user",
                "content": [{"type": "text", "text": text}]
            }]
        )
        return response_body(
            response.content[0].text,
            response.usage.input_tokens,
            response.usage.output_tokens,
            response.usage.input_tokens + response.usage.output_tokens
        )

class TogetherModel:
    def __init__(self, model):
        api_key = os.getenv("TOGETHER_API_KEY")
        self.client = Together(api_key=api_key)
        self.model = model

    def get_response(self, prompt: str, text: str):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": text}
            ]
        )
        return response_body(
            response.choices[0].message.content,
            response.usage.prompt_tokens,
            response.usage.completion_tokens,
            response.usage.total_tokens
        )