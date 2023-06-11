# -*- coding: utf-8 -*-
import os
from typing import List, Dict

import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_type = "azure"
openai.api_version = os.getenv("OPENAI_API_VERSION")
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_base = os.getenv('OPENAI_API_BASE')
OPENAI_COMPLETION_MODEL_DEPLOYMENT_NAME = os.getenv("OPENAI_COMPLETION_MODEL_DEPLOYMENT_NAME")
OPENAI_CHAT_MODEL_DEPLOYMENT_NAME = os.getenv("OPENAI_CHAT_MODEL_DEPLOYMENT_NAME")


def completion(prompt: str):
    response = openai.Completion.create(
        deployment_id=OPENAI_COMPLETION_MODEL_DEPLOYMENT_NAME,
        prompt=prompt
    )
    return response["choices"][0]["text"].strip()


def chat_completion(messages: List[Dict]):
    response = openai.ChatCompletion.create(
        deployment_id=OPENAI_CHAT_MODEL_DEPLOYMENT_NAME,
        messages=messages
    )

    return response["choices"][0]["message"]["content"].strip()


if __name__ == "__main__":
    print(completion("你是谁"))
    print(chat_completion([
        {"role": "user", "content": "你是谁？"}
    ]))
