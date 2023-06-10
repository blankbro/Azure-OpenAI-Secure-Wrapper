# -*- coding: utf-8 -*-
import os
from typing import List

import openai
from dotenv import load_dotenv
from langchain.chat_models import AzureChatOpenAI
from langchain.llms import AzureOpenAI
from langchain.schema import messages_from_dict

load_dotenv()

OPENAI_API_BASE = os.getenv('OPENAI_API_BASE')
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_COMPLETION_MODEL_DEPLOYMENT_NAME = os.getenv("OPENAI_COMPLETION_MODEL_DEPLOYMENT_NAME")
OPENAI_CHAT_MODEL_DEPLOYMENT_NAME = os.getenv("OPENAI_CHAT_MODEL_DEPLOYMENT_NAME")


def completion(prompt: str):
    response = openai.Completion.create(
        api_type="azure",
        api_key=OPENAI_API_KEY,
        api_base=OPENAI_API_BASE,
        api_version="2023-03-15-preview",
        deployment_id=OPENAI_COMPLETION_MODEL_DEPLOYMENT_NAME,
        prompt=prompt
    )
    return response["choices"][0]["text"].strip()


def langchain_completion(prompt: str):
    openai.api_type = "azure"
    openai.api_version = "2023-03-15-preview"
    openai.api_base = OPENAI_API_BASE
    openai.api_key = OPENAI_API_KEY
    llm = AzureOpenAI(
        openai_api_key=OPENAI_API_KEY,
        openai_api_base=OPENAI_API_BASE,
        deployment_name=OPENAI_COMPLETION_MODEL_DEPLOYMENT_NAME,
    )
    response_text = llm(prompt)

    return response_text.strip()


def chat_completion(message: str):
    response = openai.ChatCompletion.create(
        api_type="azure",
        api_key=OPENAI_API_KEY,
        api_base=OPENAI_API_BASE,
        api_version="2023-03-15-preview",
        deployment_id=OPENAI_CHAT_MODEL_DEPLOYMENT_NAME,
        messages=[
            {"role": "user", "content": message}
        ]
    )

    return response["choices"][0]["message"]["content"].strip()


def langchain_chat_completion(messages: List[dict]):
    llm = AzureChatOpenAI(
        openai_api_key=OPENAI_API_KEY,
        openai_api_base=OPENAI_API_BASE,
        openai_api_version="2023-03-15-preview",
        deployment_name=OPENAI_CHAT_MODEL_DEPLOYMENT_NAME
    )
    response = llm(messages_from_dict(messages))

    return response.content.strip()


if __name__ == "__main__":
    # print(completion("你是谁"))
    # print(langchain_completion("你是谁"))
    print(langchain_chat_completion([{"type": "human", "data": {"content": "你是谁"}}]))
    print(chat_completion("你是谁"))
