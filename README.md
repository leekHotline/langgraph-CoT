# Chain Of Thought

## HOW TO RUN
```
git clone 
uv sync
.\.venv\Scripts\activate
cd src
uvicorn main:app --reload
```
#### 克隆项目 安装依赖 进入虚拟环境 进入src目录 启动服务



## HOW TO TEST
```
curl "http://localhost:8000/cot?question=为什么天空是蓝色的？"
```