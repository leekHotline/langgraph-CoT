# Chain Of Thought

## HOW TO RUN
```
git clone https://github.com/leekHotline/langgraph-CoT.git
pip install uv
uv sync
.venv\Scripts\activate
uv run src.main
```
#### 克隆项目 安装依赖管理工具和依赖包 进入虚拟环境 进入src目录 启动服务



## HOW TO TEST
```
curl "http://localhost:8000/cot?question=为什么天空是蓝色的？"
```


```
修复了模块导入路径（改用相对导入 .cot.cot_agent）
将 langchain-openai 替换为原生 openai 库，解决了 API 响应格式不兼容的问题
添加了响应格式兼容处理，支持字符串和标准对象两种返回格式
```
