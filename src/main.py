import os
import dotenv
from loguru import logger
import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from typing import Optional
from fastapi.responses import StreamingResponse
from .cot.cot_agent import build_cot_graph
import json

# render默认端口加载于环境变量 默认10000

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

# 默认跟路由
@app.get("/")
def root_router():
    return JSONResponse(content={
        "message" : "Welcome to the CoT API Service, which is powered by Render!",
    })

if __name__ == "__main__":
    logger.info("Starting server at localhost:8000")
    port = int(os.getenv("PORT", "8000")) # 环境变量没有 端口就为8000 字符串转整数
    uvicorn.run(
        app="src.main:app", # 需要导入模块
        host = "0.0.0.0", # 回环地址可以被外部访问
        port = port, # 暴露的端口
        reload = True, # 代码变动时自动重启
    )

