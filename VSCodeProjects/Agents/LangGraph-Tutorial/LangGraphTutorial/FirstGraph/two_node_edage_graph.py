from typing import TypedDict
from langgraph.graph import StateGraph
from Entity.Employee.employee_model import EmployeeModel
from Entity.common.request_model import ApiRequest, ApiResponse, ErrorModel
from Entity.Employee.employee_model import EmployeeModel

class StateAgent(TypedDict):
    """
        Represents the state of the agent.
    """
    employee       : EmployeeModel | None
    api_request    : ApiRequest | None
    api_response   : ApiResponse | None
    api_error      : ErrorModel | None


def handle_request_node(state: StateAgent) -> StateAgent:
    """
        A simple node that modifies the agent's state.
    """ 
    if(state['api_request'] is None):
        state['api_response'] = ApiResponse(
            tranId= "RequestError" ,
            status= "failure",
            message="Request object is None. Please send a valid request.",
            result = None,
            api_error = ErrorModdel(
                errorId= 1001,
                errorMessage= "Invalid Request",
                errorDetails= "The API request object is None.",        
                errorCode= "400 Bad Request")
        )
    else:
        state['employee'] = state['api_request'].inputdata
        state['api_response'] = ApiResponse(
            tranId= state['api_request'].tranId,
            error= None
        )
    return state

def process_employee_node(state: StateAgent) -> StateAgent:

    errorId = state['api_response'].error.errorId if state['api_response'].error else None
    if errorId == 0:    
        employee = state['employee']
        if employee:
            state['api_response'].result = employee
            state['api_response'].status = "success"
            state['api_response'].message = "Employee processed successfully."
        else:
            state['api_response'].status = "failure"
            state['api_response'].message = "No employee data found."

graph = StateGraph(StateAgent)

graph.add_node('handle_request_node', handle_request_node)
graph.add_node('process_employee_node', process_employee_node)
graph.add_edge('handle_request_node', 'process_employee_node')
graph.set_entry_point('handle_request_node')
graph.set_finish_point('process_employee_node')

two_node_app = graph.compile()


