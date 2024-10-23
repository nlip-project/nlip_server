"""
The genAI interface defines a way to interact with any genAI model in the raw. 

GenAI models can support the following interfaces: 

1. Given a prompt template and a template value, return a 
response to that template prompt

2. Given a prompt template, generate the embedding for that prompt. 

3. An interactive chat interface -- 

"""

from typing import Literal

import httpx

from app.utils import errors as err


class GenAI:

    def generate(self, prompt: str, **kwargs) -> str:
        raise err.UnImplementedError("generate", self.__class__.__name__)

    def generate_templated(
        self, prompt_template: str, prompt_args: dict, **kwargs
    ) -> str:
        prompt = prompt_template.format(**prompt_args)
        return self.generate(prompt, **kwargs)

    def get_embeddings(self, prompt: str, **kwargs) -> list[float]:
        raise err.UnImplementedError("get_embeddings", self.__class__.__name__)


class OllamaClient(GenAI):
    def __init__(self, host: str = "localhost", port: int = 11434, model="mistral"):
        self.host = host
        self.port = port
        self.model = model

    def __str__(self):
        return f"{self.model} at http://{self.host}:{self.port}/  "

    def _base_httpx_call(
        self,
        apicall: Literal["generate", "embeddings", "chat"],
        priority_data: dict,
        **kwargs,
    ):
        url = f"http://{self.host}:{self.port}/api/{apicall}"
        data = kwargs
        data.update(priority_data)
        resp = httpx.post(url, json=data, timeout=120.0)
        return resp.raise_for_status().json()

    def generate(self, prompt: str, **kwargs) -> str:
        data = {"model": self.model, "prompt": prompt, "stream": False}
        results = self._base_httpx_call("generate", data)
        return results["response"]

    def get_embeddings(self, prompt: str, **kwargs) -> list[float]:
        data = {"model": self.model, "prompt": prompt, "stream": False}

        results = self._base_httpx_call("embeddings", data)
        return results["embedding"]

    def chat(self, this_message, history=list(), **kwargs):
        llama_message = history + [this_message]
        data = {"model": self.model, "messages": llama_message, "stream": False}
        results = self._base_httpx_call("chat", data, **kwargs)
        return results.get("message", None)


"""
A convenience class for single request-response interaction. 

"""


class SimpleGenAI:
    def __init__(self, host: str = "localhost", port: int = 11434):
        self.host = host
        self.port = port

    def generate(self, model, prompt: str) -> str:
        server = OllamaClient(host=self.host, port=self.port, model=model)
        return server.generate(prompt)

    def generate_templated(
        self, model: str, prompt_template: str, prompt_args: dict, **kwargs
    ) -> str:
        prompt = prompt_template.format(**prompt_args)
        return self.generate(model, prompt)

    def get_embeddings(self, model: str, prompt: str) -> list[float]:
        server = OllamaClient(host=self.host, port=self.port, model=model)
        return server.get_embeddings(prompt)


"""
A Convenience class which remembers previous interactions as context.
"""


class StatefulGenAI:
    def __init__(
        self, host: str = "localhost", port: int = 11434, model: str = "mistral"
    ):
        self.server = OllamaClient(host=host, port=port, model=model)
        self.history = list()

    def chat(self, message: str):
        this_message = {"role": "user", "content": message}
        response = self.server.chat(this_message, self.history)
        self.history.append(this_message)
        self.history.append(response)
        return response.get("content")
