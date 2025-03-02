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
        self.cutoff_context = ""
        self.full_conversation = ""
        self.valid_context = True
        self.responses = []

        # claiming a need for a lock, but I don't believe it

    # implementing streaming part myself
    def query(self, msg: str, max_tokens: int) -> str:
        self.full_conversation += " " + msg
        data = {
            "model": self.model,
            # there may be a better solution
            "prompt": msg if self.valid_context else self.cutoff_context + " " + msg,
            # can't use the real context vector with streaming api and cutoff
            "context": self.context,
            "stream": True,
        }

        generated_text = ""
        token_count = 0
        # generated with gemini
        with requests.post(f"{self.host}/api/generate", json.dumps(data)) as response:
            response.raise_for_status()  # raise error for bad resp

            for line in response.iter_lines():
                if line:  # Ignore keep-alive new lines
                    try:
                        json_data = json.loads(line.decode('utf-8'))
                        token = json_data.get('response', '')
                        generated_text += token
                        token_count += 1

                        if token_count >= max_tokens:
                            self.valid_context = False
                            self.cutoff_context = generated_text
                            break  # Exit the loop to stop processing the stream

                        if json_data.get('done', False):
                            self.valid_context = True
                            self.context = json_data.get('context')
                            break

                    except json.JSONDecodeError:
                        print(f"Error decoding JSON: {line}")
                        continue  # Skip to the next line
        self.full_conversation += " " + generated_text

        return generated_text


# tests
if __name__ == "__main__":
    pass
