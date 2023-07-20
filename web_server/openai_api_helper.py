# -*- coding: utf-8 -*-
import os

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
        n=request.n,
        stop=request.stop,
        stream=request.stream
    )


def create_chat_completion(request: ChatCompletionRequest):
    return openai.ChatCompletion.create(
        deployment_id=OPENAI_CHAT_MODEL_DEPLOYMENT_NAME,
        messages=request.messages,
        max_tokens=request.max_tokens,
        temperature=request.temperature,
        top_p=request.top_p,
        n=request.n,
        stop=request.stop,
        stream=request.stream
    )


async def create_chat_completion_stream(request: ChatCompletionRequest):
    response = await openai.ChatCompletion.acreate(
        deployment_id=OPENAI_CHAT_MODEL_DEPLOYMENT_NAME,
        messages=request.messages,
        max_tokens=request.max_tokens,
        temperature=request.temperature,
        top_p=request.top_p,
        n=request.n,
        stop=request.stop,
        stream=request.stream
    )

    async for chunk in response:
        yield chunk
        # await asyncio.sleep(0.2)


def test():
    from datetime import datetime
    print("当前时间：", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print(create_completion(CompletionRequest(prompt="你是谁？")))
    print("当前时间：", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


if __name__ == "__main__":
    test()
    # print(create_completion(CompletionRequest(prompt="你是谁？")))

    # 流式输出结果
    # response = create_completion(CompletionRequest(prompt="你是谁？", stream=True))
    # for chunk in response:
    #     text = chunk['choices'][0]['text']
    #     print(text)

    # response = create_chat_completion(
    #     ChatCompletionRequest(
    #         messages=[
    #             {"role": "user", "content": "你是谁？"}
    #         ],
    #         stream=True
    #     )
    # )
    #
    # for chunk in response:
    #     choices_0 = chunk['choices'][0]
    #     if choices_0['finish_reason'] and choices_0['finish_reason'] == 'stop':
    #         print("end")
    #     delta = choices_0['delta']
    #     if "content" in delta:
    #         print(delta['content'])
