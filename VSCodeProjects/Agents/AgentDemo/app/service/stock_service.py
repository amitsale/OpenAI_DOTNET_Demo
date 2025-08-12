from .stock_service_interface import StockServiceInterface
import os
import requests
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_openai_functions_agent , AgentExecutor
from langchain_core.tools import tool   

class StockService(StockServiceInterface):

    def __init__(self):
        load_dotenv()
        self.openAI_api_key = os.getenv("OPENAI_API_KEY")
        self.llm = ChatOpenAI(model="gpt-4o",openai_api_key=self.openAI_api_key,temperature=0.1)
        self.tools = [self.get_stock_price, self.get_stock_analysis]
            # tool(
            #     name="get_stock_price",
            #     func=self.get_stock_price,
            #     description="Get the current stock price for a given stock symbol."
            # ),
            # tool(
            #     name="get_stock_analysis",
            #     func=self.get_stock_analysis,
            #     description="Get a brief analysis of the stock performance."
            # )
        # ]

    def stock_information(self, userquery: str):
        """
        This method can be used to fetch stock information.
        It can be extended to include more functionalities in the future.
        """
        return "stock price is 100"
        # response = self.run_agent(userquery)
        # return response
    
    @tool
    def get_stock_price(self, stock: str) -> str:
        """Get the current stock price for a given stock symbol."""
        # Placeholder logic
        return f"Current stock price for {stock} is $100"

    @tool
    def get_stock_analysis(self, stock: str) -> str:
        """Get a brief analysis of the stock performance."""
        # Placeholder logic for stock analysis
        return f"Analysis for {stock}: The stock is performing well with a steady upward trend."
    
    def run_agent(self, query: str):
        agent = create_openai_functions_agent(
            llm=self.llm,
            tools=self.tools
        )
    
        agent_executor = AgentExecutor(agent=agent, tools=self.tools, verbose=True)
    
        response = agent_executor.invoke({"input": query})
    
        return response['output']
