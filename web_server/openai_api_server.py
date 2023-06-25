import fastapi
import uvicorn

import openai_api_helper
from openai_api_protocol import (ChatCompletionRequest, CompletionRequest)

app = fastapi.FastAPI()


# 来源 https://github.com/lm-sys/FastChat/blob/main/fastchat/serve/openai_api_server.py
# https://github.com/tiangolo/fastapi/tree/master/fastapi
@app.post("/v1/completions")
async def create_completion(request: CompletionRequest):
    return openai_api_helper.create_completion(request)


@app.post("/v1/chat/completions")
async def create_chat_completion(request: ChatCompletionRequest):
    return openai_api_helper.openai_chat_completion(request)


if __name__ == '__main__':
    uvicorn.run(app, port=8080, log_level="info")
