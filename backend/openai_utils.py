import openai
import os
from dotenv import load_dotenv
import argparse
import requests
import json
import logging
load_dotenv()  # take environment variables from .env.

openai.api_key = os.getenv("OPENAI_API_KEY")


def next_steps(prediction):
    steps = send_message_to_openai(prediction)
    return steps
def send_message_to_openai(diagnosis: str):
    message = f"I have {diagnosis}, what should my next steps of care be?"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {os.getenv("OPENAI_API_KEY")}',
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": message}],
        "temperature": 0.7
    }
    response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, data=json.dumps(data))
    response_data = response.json()
    return response_data['choices'][0]['message']['content']
