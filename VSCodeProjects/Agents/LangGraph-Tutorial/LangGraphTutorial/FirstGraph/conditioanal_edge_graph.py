from typing import TypedDict
from langgraph.graph import StateGraph , START , END

class AgentState(TypedDict):
    """
        Represents the state of the agent.
    """
    number1: int 
    number2: int
    result1 : int | None = None
    operation1 : str | None = None
     
    number3: int | None = None
    number4: int | None = None
    result2 : int | None = None
    operation2 : str | None = None

def add_node(state: AgentState) -> AgentState:
    """
        A node that adds two numbers.
    """
    state['result1'] = state['number1'] + state['number2']
    state['operation1'] = 'add'
    return state

def subtract_node(state: AgentState) -> AgentState:
    """
        A node that subtracts two numbers.
    """
    state['result1'] = state['number1'] - state['number2']
    state['operation1'] = 'subtract'
    return state

def divide_node(state: AgentState) -> AgentState:
    """
        A node that divides two numbers.
    """
    if state['number2'] == 0:
        raise ValueError("Division by zero is not allowed.")
    state['result1'] = state['number1'] / state['number2']
    state['operation1'] = 'divide'
    return state

def multiply_node(state: AgentState) -> AgentState:
    """
        A node that multiplies two numbers.
    """
    state['result2'] = state['number3'] * state['number4']
    state['operation2'] = 'multiply'
    return state    

def router_add_sub_node(state: AgentState) -> AgentState:
    """
        A router node that decides which operation to perform.
    """
    if state['operation1'] == 'add':
         return "addition_operation"
    elif state['operation2'] == 'subtract': 
         return  "subtraction_operation"
     

def router_multiply_divide_node(state: AgentState) -> AgentState:
    """
        A router node that decides which operation to perform.
    """
    if state['operation2'] == 'multiply':
         return  "multiply_operation"
    elif state['operation2'] == 'divide':
         return  "divide_operation"
    else:
         raise ValueError("Invalid operation for multiplication/division.") 
     

graph = StateGraph(AgentState)
graph.add_node('addnode', add_node)
graph.add_node('subtractnode', subtract_node)
graph.add_node('multiplynode', multiply_node)
graph.add_node('dividenode', divide_node)
graph.add_node("router", lambda state: state)
graph.add_node('routermultiplydividenode', lambda state: state)

graph.add_edge(START,"router")
graph.add_conditional_edges("router",router_add_sub_node,{

    'addition_operation': 'addnode',
    'subtraction_operation': 'subtractnode' 
})

graph.add_edge('addnode', "routermultiplydividenode")
graph.add_edge('subtractnode', "routermultiplydividenode")

graph.add_conditional_edges('routermultiplydividenode', router_multiply_divide_node,{
    'multiply_operation': 'multiplynode',   
    'divide_operation': 'dividenode'
})

graph.add_edge("multiplynode", END)
graph.add_edge("dividenode", END)

conditional_edge_app = graph.compile()

