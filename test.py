import requests
import os
from dotenv import load_dotenv

def main():
    load_dotenv()
    API_URL = "https://api-inference.huggingface.co/models/meta-llama/Llama-3.1-8B-Instruct"
    hf_token = os.getenv("hf_token")
    headers = {"Authorization": f"Bearer {hf_token}"}
    payload = {
        "inputs": "Today is a great day",
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    print(response.json())

if __name__ == "__main__":
    main()