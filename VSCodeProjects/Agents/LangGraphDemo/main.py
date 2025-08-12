from agent.stock_agent import StockAgent
from agent.stock_agent_openai_function_calling import FunctionCallingStockAgent as functionCallingStockAgent   
from agent.stock_memory_agent import StockMemoryAgent as stockMemoryAgent
from agent.simple_memory_agent import ConversationalAgent
from agent.simple_agent import SimpleAgent

def main():
    print("Hello, World!")

if __name__ == "__main__":
    
    # Example usage of StockAgent using ReAct Description
    #agent = StockAgent()

    # Example usage of FunctionCallingStockAgent using OpenAI Function Calling
    agent = functionCallingStockAgent()
    
    # Example usage of StockMemoryAgent using Memory
    #agent = stockMemoryAgent()

    # Example usage of ConversationalAgent with memory
    #agent = ConversationalAgent()
    
    #example usage of simpleAgent 
    #agent = SimpleAgent()  

    while True:
        question = input("Ask a question (or type 'exit' to quit): ")
        if question.lower() == 'exit':
            break
        try:
            print(f"\n--- Question: {question} ---")
            response = agent.ask(question)
            print(response)
        except Exception as e:
            print(f"An error occurred: {e}")
