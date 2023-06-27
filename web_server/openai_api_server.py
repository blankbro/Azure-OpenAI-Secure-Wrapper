import asyncio
import logging
import random
import uuid
from datetime import datetime

import fastapi
import uvicorn
from fastapi import Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
from starlette.middleware.base import RequestResponseEndpoint

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

logging.basicConfig(datefmt="%Y-%m-%d %H:%M:%S", level=logging.INFO, encoding="utf-8")
console_handler = logging.StreamHandler()
logging.getLogger().addHandler(console_handler)

logger = logging.getLogger(__name__)
app = fastapi.FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_methods="*",
    allow_headers="*",
)


def create_error_response(code: int, message: str) -> JSONResponse:
    return JSONResponse(
        ErrorResponse(message=message, code=code).dict(), status_code=400
    )


def now_date_time_str():
    return datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')


# @app.middleware("http")
async def log_requests(request: Request, call_next: RequestResponseEndpoint) -> Response:
    trace_id = str(uuid.uuid4()).replace("-", "")
    logger.info(f"{now_date_time_str()} {trace_id} Request received: {request.method} {request.url}?{request.path_params if request.path_params else ''} {await request.body()}")

    start_time = datetime.utcnow()
    response = await call_next(request)
    process_time = (datetime.utcnow() - start_time).total_seconds()

    logger.info(f"{now_date_time_str()} {trace_id} Response sent: {response.status_code} ({process_time} seconds)")

    return response


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
        logger.error(str(e), e)
        return create_error_response(ErrorCode.INTERNAL_ERROR, str(e))


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


@app.post("/v1/chat/completions")
async def create_chat_completion(ai_request: ChatCompletionRequest):
    try:
        if ai_request.stream:
            generator = generate_chat_completion_stream_generator(ai_request)
            response = StreamingResponse(generator, media_type="text/event-stream", headers={
                "Cache-Control": "no-cache, must-revalidate",
                "Connection": "keep-alive"
            })
            return response
        else:
            return openai_api_helper.create_chat_completion(ai_request)
    except Exception as e:
        logger.error(str(e), e)
        return create_error_response(ErrorCode.INTERNAL_ERROR, str(e))


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
        await asyncio.sleep(random.uniform(0.01, 0.1))

    yield "data: [DONE]\n\n"


if __name__ == '__main__':
    uvicorn.run("openai_api_server:app", port=8080, reload=True, log_level="info")
