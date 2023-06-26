import traceback

import fastapi
import uvicorn
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


def create_error_response(code: int, message: str) -> JSONResponse:
    return JSONResponse(
        ErrorResponse(message=message, code=code).dict(), status_code=400
    )


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
        traceback.print_exc()
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
            return StreamingResponse(generator, media_type="text/event-stream")
        else:
            return openai_api_helper.create_chat_completion(ai_request)
    except Exception as e:
        traceback.print_exc()
        return create_error_response(ErrorCode.INTERNAL_ERROR, str(e))


async def generate_chat_completion_stream_generator(ai_request: ChatCompletionRequest):
    async for chunk in openai_api_helper.create_chat_completion_stream(ai_request):
        choices = []
        for choice in chunk['choices']:
            choices.append(
                ChatCompletionResponseStreamChoice(
                    index=choice.index,
                    delta=DeltaMessage(
                        role=choice['delta']['role'] if 'role' in choice['delta'] else None,
                        content=choice['delta']['content'] if 'content' in choice['delta'] else None,
                    ),
                    finish_reason=choice.finish_reason
                )
            )

        finish_chunk = ChatCompletionStreamResponse(
            id=chunk.id,
            object=chunk.object,
            created=chunk.created,
            model=chunk.model,
            choices=choices
        )

        yield f"data: {finish_chunk.json(exclude_unset=True, ensure_ascii=False)}\n\n"

    yield "data: [DONE]\n\n"


if __name__ == '__main__':
    uvicorn.run("openai_api_server:app", port=8080, reload=True, log_level="info")
