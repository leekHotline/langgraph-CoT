import os
import dotenv
from typing import TypedDict
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage,SystemMessage
from langgraph import StateGraph, END


dotenv.load_dotenv()
API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")


# 定义状态 in 123 out
class GraphState(TypedDict):
    question: str
    step1: str
    step2: str
    step3: str
    answer: str


# 初始化模型
llm = ChatOpenAI(model="gpt-4o", base_url=BASE_URL, api_key=API_KEY, temperature=0)

# node1 思考第一步
def think_step1(state: GraphState) -> GraphState:
    messages = [
        SystemMessage(content="你是一个逻辑推理专家，擅长将复杂问题拆解为3个思考步骤。"),
        HumanMessage(content=f"问题:{state['question']}\n\n 第一步:")
    ]
    response = llm.invoke(messages)
    return {"step1": response.content.strip()}

# node2 思考第二步
def think_step2(state: GraphState) -> GraphState:
    messages = [
        SystemMessage(content="你是一个逻辑推理专家，擅长将复杂问题拆解为3个思考步骤。"),
        HumanMessage(content=f"问题:{state['question']}\n\n 第二步:")
    ]
    response = llm.invoke(messages)
    return {"step2": response.content.strip()}

# node3 思考第三步 输出最终答案
def think_step3(state: GraphState) -> GraphState:
    messages = [
        SystemMessage(content="你是一个逻辑推理专家，擅长将复杂问题拆解为3个思考步骤。"),
        HumanMessage(content=f"问题:{state['question']}\n\n 第三步:")
    ]
    response = llm.invoke(messages)
    return {"step3": response.content.strip()}

# 构建图
def build_cot_graph(GraphState):
    graph = StateGraph(GraphState)
    graph.add_node("step1", think_step1)
    graph.add_node("step2", think_step2)
    graph.add_node("step3", think_step3)

    graph.set_entry_point("step1") # in-1-2-3-out 
    graph.add_edge("step1", "step2")
    graph.add_edge("step2", "step3")
    graph.add_edge("step3", END)

    return graph.compile()