import os
from flask import Flask, request, jsonify, send_from_directory
from base64 import b64decode
from openai import OpenAI
from dotenv import load_dotenv
import json
import base64
import re
import requests
from datetime import datetime

load_dotenv()

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

app = Flask(__name__)

def getCompletion(text, image_path, detail='auto'):
    
    
    # OpenAI API Key
    api_key = os.environ.get("OPENAI_API_KEY")

    # Function to encode the image
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    # Path to your image
    image_path = "path_to_your_image.jpg"

    # Getting the base64 string
    base64_image = encode_image(image_path)

    headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
    }

    payload = {
    "model": "gpt-4-vision-preview",
    "messages": [
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": text
            },
            {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}",
                "detail": detail,
            }
            }
        ]
        }
    ],
    "max_tokens": 500
    }
    
    
    response = requests.post(
        "https://api.openai.com/v1/chat/completions", headers=headers, json=payload
    )

    json_data = response.json()

    print(json_data)

    input_str = json_data["choices"][0]["message"]["content"]
    
    print("*" * 100)
    print(input_str)
    print("*" * 100)

    return input_str





if __name__ == "__main__":
    app.run(debug=True, port=5006)
