import asyncio
import random
import traceback

import fastapi
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse

import openai_api_helper
from openai_api_protocol import (
    DeltaMessage,
    ChatCompletionRequest,
    ChatCompletionStreamResponse,
    ChatCompletionResponseStreamChoice,
    CompletionRequest,
    CompletionStreamResponse,
    CompletionResponseStreamChoice,
    ErrorResponse,
    ErrorCode
)

app = fastapi.FastAPI()
# 配置允许跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源的请求，你也可以设置具体的来源
    allow_methods=["*"],  # 允许所有 HTTP 方法
    allow_headers=["*"],  # 允许所有的请求头
)


def create_error_response(code: int, message: str) -> JSONResponse:
    return JSONResponse(
        ErrorResponse(message=message, code=code).dict(), status_code=400
    )


async def generate_completion_stream_generator(ai_request: CompletionRequest):
    for chunk in openai_api_helper.create_completion(ai_request):
        choices = []
        for choice in chunk['choices']:
            choices.append(
                CompletionResponseStreamChoice(
                    index=choice.index,
                    text=choice.text,
                    logprobs=choice.logprobs,
                    finish_reason=choice.finish_reason
                )
            )

        finish_chunk = CompletionStreamResponse(
            id=chunk.id,
            object=chunk.object,
            created=chunk.created,
            model=chunk.model,
            choices=choices
        )

        yield f"data: {finish_chunk.json(exclude_unset=True, ensure_ascii=False)}\n\n"

    yield "data: [DONE]\n\n"


async def generate_chat_completion_stream_generator(ai_request: ChatCompletionRequest):
    async for chunk in openai_api_helper.create_chat_completion_stream(ai_request):
        choices = []
        for choice in chunk['choices']:
            delta = DeltaMessage()
            if 'role' in choice['delta']:
                delta.role = choice['delta']['role']
            if 'content' in choice['delta']:
                delta.content = choice['delta']['content']

            choices.append(
                ChatCompletionResponseStreamChoice(
                    index=choice.index,
                    finish_reason=choice.finish_reason,
                    delta=delta,
                )
            )

        finish_chunk = ChatCompletionStreamResponse(
            id=chunk.id,
            object=chunk.object,
            created=chunk.created,
            model=chunk.model,
            choices=choices,
        )

        yield f"data: {finish_chunk.json(exclude_unset=True, ensure_ascii=False)}\n\n"
        # await asyncio.sleep(random.uniform(0.01, 0.1))

    yield "data: [DONE]\n\n"


# 来源 https://github.com/lm-sys/FastChat/blob/main/fastchat/serve/openai_api_server.py
# https://github.com/tiangolo/fastapi/tree/master/fastapi
@app.post("/v1/completions")
async def create_completion(ai_request: CompletionRequest):
    try:
        if ai_request.stream:
            generator = generate_completion_stream_generator(ai_request)
            return StreamingResponse(generator, media_type="text/event-stream")
        else:
            return openai_api_helper.create_completion(ai_request)
    except Exception as e:
        traceback.print_stack()
        return create_error_response(ErrorCode.INTERNAL_ERROR, str(e))


@app.post("/v1/chat/completions")
async def create_chat_completion(ai_request: ChatCompletionRequest):
    try:
        if ai_request.stream:
            response = StreamingResponse(
                generate_chat_completion_stream_generator(ai_request),
                media_type="text/event-stream",
            )
            return response
        else:
            return openai_api_helper.create_chat_completion(ai_request)
    except Exception as e:
        traceback.print_stack()
        return create_error_response(ErrorCode.INTERNAL_ERROR, str(e))


if __name__ == '__main__':
    uvicorn.run("openai_api_server:app", port=8080, reload=True, log_level="info")
