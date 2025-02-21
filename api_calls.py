from openai import OpenAI
import os
from dotenv import load_dotenv
import base64
import requests
import json


load_dotenv()

def call_openAI(actions, country_name):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('API_KEY')}"
    }

    payload = {
        "model": "gpt-4o",
        "messages": [
            {"role": "user", "content": [
                {"type": "text", "text": "Imagine you're playing a two player game where each person heads a country. The other country's actions will be attached to this message. Your task is to take an action from the given list of actions, and the action as a single word answer. You are encouraged to refer to the country's past actions and how they take decisions based on the type of government. Pick a single action out of the provided list, and return ONLY that word."},
                {"type": "text", "text": f"{actions}"},
                {"type": "text", "text": f"{country_name}"}
            ]}
        ],
        "max_tokens": 500
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    response_data = response.json()
    print(response_data)
    with open('part1.json', 'w') as file:
        file.write(json.dumps(response.json(), indent=4))
    with open('part1.json', 'r') as file:
        data = json.load(file)
        action2 = (data['choices'][0]['message']['content'])
    return action2
    #print(response.json())

