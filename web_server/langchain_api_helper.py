# -*- coding: utf-8 -*-
import os
from typing import List

from dotenv import load_dotenv
from langchain.chat_models import AzureChatOpenAI
from langchain.llms import AzureOpenAI
from langchain.schema import messages_from_dict

load_dotenv()

os.environ["OPENAI_API_TYPE"] = "azure"
os.environ["OPENAI_API_VERSION"] = os.getenv("OPENAI_API_VERSION")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_BASE"] = os.getenv("OPENAI_API_BASE")
OPENAI_COMPLETION_MODEL_DEPLOYMENT_NAME = os.getenv("OPENAI_COMPLETION_MODEL_DEPLOYMENT_NAME")
OPENAI_CHAT_MODEL_DEPLOYMENT_NAME = os.getenv("OPENAI_CHAT_MODEL_DEPLOYMENT_NAME")


def create_completion(prompt: str):
    llm = AzureOpenAI(deployment_name=OPENAI_COMPLETION_MODEL_DEPLOYMENT_NAME, verbose=True)
    response_text = llm(prompt)

    return response_text.strip()


def create_chat_completion(messages: List[dict]):
    llm = AzureChatOpenAI(deployment_name=OPENAI_CHAT_MODEL_DEPLOYMENT_NAME)
    response = llm(messages_from_dict(messages))

    return response.content.strip()


if __name__ == "__main__":
    print(create_completion("你是谁"))
    print(create_chat_completion([
        {"type": "human", "data": {"content": "你是谁"}}
    ]))
