# -*- coding: utf-8 -*-
import os

import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_type = "azure"
openai.api_version = "..."
openai.api_key = "..."
openai.api_base = os.getenv("OPENAI_API_BASE_PROXY")
OPENAI_COMPLETION_MODEL_DEPLOYMENT_NAME = os.getenv("OPENAI_COMPLETION_MODEL_DEPLOYMENT_NAME")
OPENAI_CHAT_MODEL_DEPLOYMENT_NAME = os.getenv("OPENAI_CHAT_MODEL_DEPLOYMENT_NAME")


def completion():
    response = openai.Completion.create(
        deployment_id=OPENAI_COMPLETION_MODEL_DEPLOYMENT_NAME,
        prompt="你是谁？"
    )
    response_text = response["choices"][0]["text"].strip()
    print(response_text)


def chat_completion():
    response = openai.ChatCompletion.create(
        deployment_id=OPENAI_CHAT_MODEL_DEPLOYMENT_NAME,
        messages=[
            {
                "role": "system",
                "content": "You are ChatGPT, a large language model trained by OpenAI. Follow the user's instructions carefully. Respond using markdown."
            },
            {
                "role": "user",
                "content": "你是谁？"
            }
        ]
    )

    response_text = response["choices"][0]["message"]["content"].strip()
    print(response_text)


if __name__ == "__main__":
    completion()
    chat_completion()
