# -*- coding: utf-8 -*-
import os
from typing import List, Dict

import openai
from dotenv import load_dotenv

from openai_api_protocol import ChatCompletionRequest, CompletionRequest

load_dotenv()

openai.api_type = "azure"
openai.api_version = os.getenv("OPENAI_API_VERSION")
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_base = os.getenv('OPENAI_API_BASE')
OPENAI_COMPLETION_MODEL_DEPLOYMENT_NAME = os.getenv("OPENAI_COMPLETION_MODEL_DEPLOYMENT_NAME")
OPENAI_CHAT_MODEL_DEPLOYMENT_NAME = os.getenv("OPENAI_CHAT_MODEL_DEPLOYMENT_NAME")


def create_completion(request: CompletionRequest):
    return openai.Completion.create(
        deployment_id=OPENAI_COMPLETION_MODEL_DEPLOYMENT_NAME,
        prompt=request.prompt,
        max_tokens=request.max_tokens,
        temperature=request.temperature,
        top_p=request.top_p,
        n=request.n
    )


def openai_chat_completion(request: ChatCompletionRequest):
    response = openai.ChatCompletion.create(
        deployment_id=OPENAI_CHAT_MODEL_DEPLOYMENT_NAME,
        messages=request.messages,
        max_tokens=request.max_tokens,
        temperature=request.temperature,
        top_p=request.top_p,
        n=request.n
    )
    return response


if __name__ == "__main__":
    print(create_completion(CompletionRequest(prompt="你是谁？")))
    print(openai_chat_completion(ChatCompletionRequest(
        messages=[
            {"role": "user", "content": "你是谁？"}
        ]))
    )
