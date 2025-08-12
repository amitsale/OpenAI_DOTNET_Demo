from typing import TypedDict
from langgraph.graph import StateGraph

class AgentState(TypedDict):
    """
        Represents the state of the agent.
    """
    message        : str
            
def simple_node(state: AgentState) -> AgentState:
    """
        A simple node that modifies the agent's state.
    """
    state['message']           = "Hi " + state['message'] + " Welcome to LangGraph!"
    return state

graph =StateGraph(AgentState)

graph.add_node('simple_node', simple_node)
graph.set_entry_point('simple_node')
graph.set_finish_point('simple_node')

app = graph.compile()

 