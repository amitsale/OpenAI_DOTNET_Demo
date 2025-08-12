from typing import TypedDict, List, Union
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage , SystemMessage
from langgraph.graph import StateGraph, START, END  
from langchain_core.tools import tool
from dotenv import load_dotenv
import os

load_dotenv()

class AgentState(TypedDict):
    """
        Represents the state of the agent.
    """
    messages: List[Union[HumanMessage, AIMessage, SystemMessage]]
    lastmessage : AIMessage #stores the last AI response
    response: Union[str, AIMessage] = None
    firstmessage : bool = True  # Flag to indicate if it's the first message

#create tools for the agent
# These tools can be used by the agent to perform operations like addition, subtraction, etc.
@tool
def add(number1: int, number2: int) -> int:
    """
        Adds two numbers.
    """
    return number1 + number2

@tool
def subtract(number1: int, number2: int) -> int:    
    """
        Subtracts two numbers.
    """
    return number1 - number2

@tool
def divide(number1: int, number2: int) -> float:
    """
        Divides two numbers.
    """
    if number2 == 0:
        raise ValueError("Division by zero is not allowed.")
    return number1 / number2

@tool
def multiply(number1: int, number2: int) -> int:
    """
        Multiplies two numbers.
    """
    return number1 * number2

# List of tools that the agent can use
tools = [add, subtract, divide, multiply]

# Define the model node that processes the agent's message and generates a response
def model_node(state:AgentState) -> AgentState:
    """
        A node that processes the agent's message and generates a response.
    """
    llm      = ChatOpenAI(model="gpt-4o", temperature=0, api_key=os.getenv("OPENAIKEY"))


    if state['firstmessage']:
        # If it's the first message, set a system message
        system_message = SystemMessage(content="You are a helpful assistant.")
        state['messages'].insert(0, system_message)
        state['firstmessage'] = False
    
    # Invoke the LLM with the conversation history
    response = llm.invoke(state['messages'])

    state["messages"].append(AIMessage(content=response.content))  # Append the AI response to the messages
    state['response'] = response.content
    state['lastmessage'] = AIMessage(content=response.content)  # Store the last AI response
    print("Response from LLM:", response.content)  # Debugging output
    print("Updated conversation history:", state['messages'])  # Debugging output
    return state

def should_invoke_tool(state: AgentState)  :
    """
        A node that decides whether to invoke a tool based on the agent's response.
    """
    # Check if the response contains a tool call
    if state['response'] and "tool_calls" in state['response']:
        return True
    return False

graph = StateGraph(AgentState)
graph.add_node('modelnode', model_node)
graph.add_edge(START, "modelnode")
graph.add_edge("modelnode", END)
memory_agent_app = graph.compile()

import matplotlib.pyplot as plt
import matplotlib.image as mpimg    
img_path = memory_agent_app.get_graph().draw_mermaid_png()  # This should return a file path or bytes
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
# This code defines a memory agent that can maintain a conversation history and respond to user inputs.

