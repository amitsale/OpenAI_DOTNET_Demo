from langgraph.graph import StateGraph, START, END
from typing import TypedDict

class AgentState(TypedDict):
    """
        Represents the state of the agent.
    """
    Numbers : list[int]
    counter : int
    result  : int | None = None

def process_node(state: AgentState) -> AgentState:
    """
        A node that sums a list of numbers.
    """
    counter = state['counter']
    if( counter == 0 ):
        state['result'] = 0

    state['result'] = int(state['result']) + int(state['Numbers'][counter])
    state['counter'] = counter + 1 
    return state

def loop_node(state: AgentState) -> AgentState:
    """
        A node that loops through a list of numbers.
    """
    if state['counter'] < len(state['Numbers']):
        return "loop"
    else:
        return "exit"
    
graph = StateGraph(AgentState)
graph.add_node('processnode', process_node)
#graph.add_node('loopnode', loop_node)   Loop node is not needed as a separate node   
graph.add_edge(START, 'processnode')
graph.add_conditional_edges('processnode', loop_node, {
    "loop": "processnode",
    "exit": END
})



loop_node_app = graph.compile()

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

img_path = loop_node_app.get_graph().draw_mermaid_png()  # This should return a file path or bytes
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