from typing import TypedDict , List
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
import os

load_dotenv()

class AgentState(TypedDict):
    """
        Represents the state of the agent.
    """
    message: List[HumanMessage]
    response: str | None = None

def process_node(state: AgentState) -> AgentState:
    """
        A node that processes the agent's message and generates a response.
    """
    llm = ChatOpenAI(model="gpt-4o", temperature=0,api_key=os.getenv("OPENAIKEY"))
    response = llm.invoke(state['message'])
    state['response'] = response.content
    return state

graph = StateGraph(AgentState)
graph.add_node('processnode', process_node)
graph.add_edge(START, "processnode")
graph.add_edge("processnode",END)

simple_agent_app = graph.compile()

import matplotlib.pyplot as plt
import matplotlib.image as mpimg    

img_path = simple_agent_app.get_graph().draw_mermaid_png()  # This should return a file path or bytes
if isinstance(img_path, str):       
    img = mpimg.imread(img_path)
    plt.imshow(img)
    plt.axis('off')
    plt.show()      
else:
    from PIL import Image
    import io
    image = Image.open(io.BytesIO(img_path))
    image.show()

 