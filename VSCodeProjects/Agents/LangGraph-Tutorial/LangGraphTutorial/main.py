from FirstGraph.first_graph import app
from FirstGraph.two_node_edage_graph import two_node_app
from Entity.Employee.employee_model import EmployeeModel 

from Entity.common.request_model import ApiRequest, ApiResponse, ErrorModel
from FirstGraph.conditioanal_edge_graph import conditional_edge_app as conditional_edge_app
from FirstGraph.loop_node import loop_node_app

#importing SimpleAgent
from agent.simple_agent import simple_agent_app
from langchain_core.messages import HumanMessage

#importing Memory Agent
from agent.memory_agent import memory_agent_app  
from langchain_core.messages import AIMessage

print("Sample startup method running!")

if __name__ == "__main__":
    #result = app.invoke({"message": "Amit"})
    #print(result)
    
    '''
    print("Running two-node edge graph...")

    api_request = ApiRequest(
        tranId="12345", 
        userid="user1",
        inputdata=EmployeeModel(
            employeeId=1,
            firstName="John",
            lastName="Doe",
            email=""  ,
            phone="1234567890",
            department="Engineering",
            position="Software Engineer",
            salary=60000.0,
            isActive=True,
            startDate="2023-01-01"
        )
    )

    result = two_node_app.invoke({"api_request": api_request})
    print(result)
    '''


    '''
    Edge Node Example
    
    result = conditional_edge_app_result.invoke({
        "number1": 10,
        "number2": 20,    
        "number3": 100,
        "number4": 50,
        "operation1": "add",  
        "operation2"  : "multiply"  
    })
    print("Conditional Edge Graph Result:" + str(result))
    print(result["result1"])
    print(result["result2"])
    '''
    
    # Running Loop Node Example
    '''
    print("Running Loop Node Example...")
    loop_node_app_result = loop_node_app.invoke({
        "Numbers": [1, 2, 3, 4, 5]
        ,"counter": 0
    })
    print("Loop Node Result: " + str(loop_node_app_result))
    '''

    # Running Simple Agent Example
    '''
    print("Running Simple Agent Example...")
    
    initial_message = input("Please enter your Question :")
    result = simple_agent_app.invoke({"message": [HumanMessage(content=initial_message)]})
    print("Response from the agent:", result['response'])
    '''

    # Running MEmory Agent Example
    #create a conversation history
    print("Running Memory Agent Example...")
    conversation_history = []

    user_input = input("Enter: ")
    while user_input != "exit":
        conversation_history.append(HumanMessage(content=user_input))
        result = memory_agent_app.invoke({"messages": conversation_history})
        conversation_history = result["messages"]
       
        user_input = input("Enter: ")


    with open("logging.txt", "w") as file:
        file.write("Your Conversation Log:\n")
        
        for message in conversation_history:
            if isinstance(message, HumanMessage):
                file.write(f"You: {message.content}\n")
            elif isinstance(message, AIMessage):
                file.write(f"AI: {message.content}\n\n")
        file.write("End of Conversation")

    print("Conversation saved to logging.txt")
