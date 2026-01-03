import os
import dotenv
from loguru import logger
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from .cot.cot_agent import build_cot_graph
import json



app = FastAPI()
cot_graph = build_cot_graph()


@app.get("/cot")
async def cot_api(question: str):
    async def event_stream():
        # 构建初始状态
        state = {"question": question}

        # 执行图
        result = cot_graph.invoke(state)


        # 模拟逐步返回
        steps = [
            ("step1", result['step1']),
            ("step2", result['step2']),
            ("step3", result['step3'])
        ]

        for key,value in steps:
            yield f"data: {json.dumps({key: value})}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")
