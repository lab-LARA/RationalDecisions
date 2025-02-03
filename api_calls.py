from openai import OpenAI
from keys import api_key
import os
from dotenv import load_dotenv
import base64
import requests
import json


load_dotenv()

API_KEY = os.getenv("API_KEY")





headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
  }

payload = {
    "model": "gpt-4o",
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": "Given a country, return the type of government in the country and a list of one word actions they can take to solve a conflict with another country based on their past decisions, for example, withold trade. No extra words in the answer."
          },
          {
              "type":"text",
              "text":" China."
          }
        ]
      }
    ],
    "max_tokens": 500
}
response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
print(response.json())

