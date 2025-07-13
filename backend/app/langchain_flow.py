from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from langgraph import StateGraph

llm = ChatOpenAI(model="gpt-4o", temperature=0.2)
graph = StateGraph()

@graph.step
def generate_steps(component_id: int):
    prompt = f"Provide step-by-step repair instructions for component #{component_id}."
    resp = llm([HumanMessage(content=prompt)])
    return resp.content

graph.compile()
