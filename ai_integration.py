import json
import requests
from typing import Dict, List, Optional, Union


# eventually create a wrapper
class OllamaThread:
    def __init__(
            self,
            model: str = "llama3.1",
            initial_prompt: Optional[str] = None,
            context: Optional[List[int]] = None,
            host: str = "http://localhost:11434"):
        self.model = model
        self.host = host
        self.context = context or []  # Initialize with provided context or empty list
        self.initial_prompt = initial_prompt
        self.responses = []

        # claiming a need for a lock, but I don't believe it

    # implementing streaming part myself
    def query(self, msg: str, max_tokens: int) -> str:
        data = {
            "model": self.model,
            "prompt": msg,
            "context": self.context,
            "stream": False,  # would like to use this to limit token size, but we'll see
        }
        response = requests.post(
            f"{self.host}/api/generate",
            json.dumps(data)
        )

        json_response = json.loads(response.text)
        self.context = json_response["context"]
        # print(response)
        return json_response["response"]


# tests
if __name__ == "__main__":
    pass
