from typing import TypedDict , List , Union     
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage , AIMessage
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv
import os

class AgentState(TypedDict):
    """
        Represents the state of the agent.
    """
    messages : List[Union[HumanMessage,AIMessage]]
    response : Union[str, AIMessage] = None


def process_node(state:AgentState) -> AgentState:
    """
        A node that processes the agent's message and generates a response.
    """
    llm      = ChatOpenAI(model="gpt-4o", temperature=0, api_key=os.getenv("OPENAIKEY"))
    response = llm.invoke(state['messages'])
    state["messages"].append(AIMessage(content=response.content))  # Append the AI response to the messages
    state['response'] = response.content
    print("Response from LLM:", response.content)  # Debugging output
    print("Updated conversation history:", state['messages'])  # Debugging output
    return state

graph = StateGraph(AgentState)

graph.add_node('processnode', process_node)
graph.add_edge(START, "processnode")
graph.add_edge("processnode", END)

memory_agent_app = graph.compile()

