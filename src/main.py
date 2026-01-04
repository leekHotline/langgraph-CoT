import os
import dotenv
from loguru import logger
import uvicorn
from fastapi import FastAPI
from typing import Optional
from fastapi.responses import StreamingResponse
from .cot.cot_agent import build_cot_graph
import json



app = FastAPI()
cot_graph = build_cot_graph()


@app.get("/cot")
async def cot_api(question: str, stream_switch: Optional[bool] = None):
    # 构建初始状态
    state = {"question": question}

    # 执行图
    result = cot_graph.invoke(state)
    
    # 如果需要流式返回，则在状态中加入标志 & stream_switch=true
    if not stream_switch:
        return result
    
    
    async def event_stream():

        # 模拟逐步返回
        steps = [
            ("step1", result['step1']),
            ("step2", result['step2']),
            ("step3", result['step3'])
        ]

        for key,value in steps:
            yield f"data: {json.dumps({key: value})}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")

# health check
@app.get("/ping")
def health_check():
    return {"message": "pong"}

if __name__ == "__main__":
    logger.info("Starting server at localhost:8000")
    uvicorn.run(
        app="src.main:app", # 需要导入模块
        host = "0.0.0.0", # 回环地址可以被外部访问
        port = 8000, # 暴露的端口
        reload = True, # 代码变动时自动重启
    )

