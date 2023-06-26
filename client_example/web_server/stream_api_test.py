import asyncio

import fastapi
import uvicorn
from fastapi.responses import StreamingResponse

app = fastapi.FastAPI()


async def generate_large_data():
    # 模拟生成大量数据
    for i in range(10):
        yield f"Data Chunk {i}\n"
        await asyncio.sleep(1)


@app.get("/stream")
async def stream_response():
    async def stream_generator():
        async for chunk in generate_large_data():
            yield chunk.encode("utf-8")

    return StreamingResponse(stream_generator(), media_type="text/event-stream")


if __name__ == '__main__':
    uvicorn.run("openai_api_server:app", port=8080, reload=True, log_level="info")
