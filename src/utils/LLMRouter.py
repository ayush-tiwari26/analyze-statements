import enum
import json
import requests
import os
from datetime import datetime


class Model(enum.Enum):

    LLAMA_SM = "llama2-uncensored:latest"
    LLAMA_LG = "llama3.3:latest"
    LLAMA_VISION = "llama3.2-vision:90b"
    LLAMA_CODE = "codellama:7b"
    DEEPSEEK = "deepseek-r1:70b"

    @property
    def id(self):
        return self.value


class LLMRouter:
    API_URL = 'http://localhost:3000/api/chat/completions'
    AUTH_TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImNkYzA3ZjY3LTRiMWItNDAzYi04MWVkLTgzNzMzOGEwZGFlZiJ9.QE2TvCjwHphtaEdhGV12waTf6t5G612CTXxk1Av2amg'
    LOG_DIR = 'logs'

    def __init__(self):
        os.makedirs(self.LOG_DIR, exist_ok=True)

    def hit(self, model: Model, prompt: str) -> str:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        log_path = os.path.join(self.LOG_DIR, f'{timestamp}.json')

        headers = {
            'Authorization': f'Bearer {self.AUTH_TOKEN}',
            'Content-Type': 'application/json'
        }

        payload = {
            "model": model.id,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }

        request_raw = f"curl --location '{self.API_URL}' \\\n--header 'Authorization: Bearer {self.AUTH_TOKEN}' \\\n--header 'Content-Type: application/json' \\\n--data '{json.dumps(payload)}'"

        try:
            response = requests.post(self.API_URL, headers=headers, json=payload)
            response_text = response.text
            response_json = response.json()
            content = response_json['choices'][0]['message']['content']
        except Exception as e:
            content = f"Error: {str(e)}"
            response_text = str(e)
            response_json = {}

        log_data = {
            "timestamp": timestamp,
            "request": {
                "raw": request_raw,
                "payload": payload
            },
            "response": {
                "raw": response_text,
                "payload": response_json,
                "status": response.status_code if 'response' in locals() else 'error'
            }
        }

        with open(log_path, 'w') as f:
            json.dump(log_data, f, indent=2)

        return content
