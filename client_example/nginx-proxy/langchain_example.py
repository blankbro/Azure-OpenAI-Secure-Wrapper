# -*- coding: utf-8 -*-
import os

from dotenv import load_dotenv
from langchain.chat_models import AzureChatOpenAI
from langchain.llms import AzureOpenAI
from langchain.schema import messages_from_dict

load_dotenv()

os.environ["OPENAI_API_VERSION"] = "..."
os.environ["OPENAI_API_KEY"] = "..."
os.environ["OPENAI_API_TYPE"] = "azure"
os.environ["OPENAI_API_BASE"] = os.getenv("OPENAI_API_BASE_PROXY")
OPENAI_COMPLETION_MODEL_DEPLOYMENT_NAME = os.getenv("OPENAI_COMPLETION_MODEL_DEPLOYMENT_NAME")
OPENAI_CHAT_MODEL_DEPLOYMENT_NAME = os.getenv("OPENAI_CHAT_MODEL_DEPLOYMENT_NAME")


def completion():
    llm = AzureOpenAI(deployment_name=OPENAI_COMPLETION_MODEL_DEPLOYMENT_NAME)
    response_text = llm(prompt="你是谁").strip()

    print(response_text)


def chat_completion():
    llm = AzureChatOpenAI(deployment_name=OPENAI_CHAT_MODEL_DEPLOYMENT_NAME)
    response = llm(
        messages=messages_from_dict([
            {
                "type": "system",
                "data": {
                    "content": "You are ChatGPT, a large language model trained by OpenAI. Follow the user's instructions carefully. Respond using markdown."
                }
            },
            {
                "type": "human",
                "data": {
                    "content": "你是谁"
                }
            }
        ])
    )

    response_text = response.content.strip()
    print(response_text)


if __name__ == "__main__":
    completion()
    chat_completion()
