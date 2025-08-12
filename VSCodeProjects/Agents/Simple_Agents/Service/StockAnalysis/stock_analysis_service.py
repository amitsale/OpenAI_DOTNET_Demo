from langchain.agents import Tool, initialize_agent
from langchain_community.chat_models import ChatOpenAI
from langchain.agents.agent_types import AgentType
from Service.StockAnalysis.stock_analysis_interface import IStockAnalysis
import os
from dotenv import load_dotenv


load_dotenv()

class StockAnalysisService(IStockAnalysis):
    
    def __init__(self):
        openai_key = os.getenv("OPENAIKEY")
        self.llm    = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, openai_api_key=openai_key)
        self.tools  = [Tool(name="StockAnalysis", func=self.get_symbol_Price, description="This Tool help get the current price of the Stock Symbol and get the recent news analysis done. ")]
        
    def analyze(self, query: str) -> dict: 

        # Placeholder logic for stock analysis
        self.agent  = initialize_agent(self.tools, self.llm, agent_type=AgentType.OPENAI_FUNCTIONS, verbose=True)
        return self.agent.run(query)
        
    def get_symbol_Price(self, symbol: str):
        
        # Placeholder logic for stock analysis
        return {
            "symbol": symbol,
            "analysis": f"Price of the symbol : {symbol}. is $100.00"
        }