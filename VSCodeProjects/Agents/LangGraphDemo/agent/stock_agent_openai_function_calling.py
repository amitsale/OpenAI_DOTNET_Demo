import os 
from dotenv import load_dotenv
from langchain.agents import Tool , initialize_agent, AgentType
from langchain.tools import tool
from langchain_experimental.tools.python.tool import PythonREPLTool
from langchain_openai.chat_models import ChatOpenAI as OpenAI
from langchain.prompts import PromptTemplate

import yfinance as yf

load_dotenv()

class FunctionCallingStockAgent:

    def __init__(self):
        self.OPENAI_API_KEY = os.getenv("OPENAIKEY")
        self.llm = OpenAI(temperature=0, model="gpt-4o", openai_api_key=self.OPENAI_API_KEY)        
        self.tools = self.initialize_tools()
        self.agent = self.initialize_agent()

    @tool
    def get_stock_news(stock_symbol: str) -> str:
        """Get the latest news for a given stock symbol."""
        stock = yf.Ticker(stock_symbol)
        news = stock.news
        if not news:
            return f"No recent news found for {stock_symbol}."
        latest_news = ", ".join(item['content']['title'] for item in news)
        return f"Latest news for {stock_symbol}: {latest_news}"

    @tool
    def get_stock_price(stock_symbol: str) -> str:
        """Get the current stock price for a given stock symbol."""        
        stock = yf.Ticker(stock_symbol)
        price = stock.history(period="1d")['Close'].iloc[-1]
        return f"The current price of {stock_symbol} is ${price:.2f}."

    def initialize_tools(self):
        calculator_tool = PythonREPLTool()
        return [
            Tool.from_function(self.get_stock_price
                                , name="get_stock_price"
                                , description="Get the current stock price for a given stock symbol.")
                                ,
            Tool(
                name="calculator",
                func=calculator_tool.run,
                description="A calculator tool that can perform basic arithmetic operations."
            )
            , 
            Tool(
                name="get_stock_news",
                func=self.get_stock_news,
                description="Get the latest news for a given stock symbol."
            )
        ]
    
    def initialize_agent(self):
        return initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent_type=AgentType.OPENAI_FUNCTIONS,
            verbose=True,
            promot=self.get_stock_prompt() 
        )   
    
    def ask(self, question: str):
        """Ask a question to the agent and get a response."""
        response = self.agent.run(question)
        return response

    def get_stock_prompt(self):
        """Get a prompt for the stock symbol."""
 
        prompt = PromptTemplate(                    
            input_variables=["input", "agent_scratchpad", "chat_history"],
            template=("""
                    
                    Please prepare your response as per the below structudec format for every request that you get 
                    You may need to use the tools to get the required information.

                    
                    Reponse Format:
                    
                    Title : create a right title as per the user question
                    
                    Stock Information 
                                              
                    Stock Name : name of the stock    
                    Stock Price: current price of the stock
                    Stock News : latest news related to the stock

                    Next Steps:
                    - Show Additional questions which can be asked to the user in next step.

                    example:
                        Title : Analysis for AAPL Stock
                    
                        Stock Information 
                                                
                        Stock Name : Appl   
                        Stock Price: 120.23
                        Stock News : Apple is launching new products this fall, including the iPhone 15 and Apple Watch Series 9.
                      
                        Next Steps:
                        - Would you like to know about Apple's recent financial performance?
                                                   
                    Also,use chat history to answer the question
                    Chat history:{chat_history}                                                    
                    
                    Begin!
                    User Question : {input}
                      
                    {agent_scratchpad}
                    """))
        return prompt