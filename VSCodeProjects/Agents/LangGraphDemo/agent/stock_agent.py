import os 
from dotenv import load_dotenv
from langchain.agents import Tool , initialize_agent, AgentType
from langchain.tools import tool
from langchain_experimental.tools.python.tool import PythonREPLTool
from langchain_openai.chat_models import ChatOpenAI as OpenAI
from langchain.prompts import PromptTemplate

import yfinance as yf

load_dotenv()

class StockAgent:

    def __init__(self):
        self.OPENAI_API_KEY = os.getenv("OPENAIKEY")
        self.llm = OpenAI(temperature=0, model="gpt-4o",openai_api_key=self.OPENAI_API_KEY)
        self.tools = self.initialize_tools()
        self.agent = self.initialize_agent()

    @tool
    def get_stock_news(stock_symbol: str) -> str:
        """Get the latest news for a given stock symbol."""
        
        try:
            stock = yf.Ticker(stock_symbol)
            
            news = stock.news
            if not news:
                return f"No recent news found for {stock_symbol}."
            latest_news = ", ".join(item['content']['title'] for item in news)
        except Exception as e:
            return f"Error fetching news for {stock_symbol}: {str(e)}"
            latest_news = "Jeff Bezos Once Said Great Leaders Need More Sleep, Not More Hours — Amazon Founder Then Explained His Point Using This Warren Buffett Rule, Circle Internet Stock Is Going Gangbusters. Earnings Are Its Next Test., Why IonQ (IONQ) Stock Is Up Today, Jeff Bezos' space tech company makes surprising Bitcoin bet, Affirm Stock Revisits This Place As 'Buy Now, Pay Later' Delights Shoppers, Amazon's Starlink Competitor Tops 100 Satellites. What Project Kuiper Means For Amazon Stock., Goldman Sachs revamps Nvidia stock price target ahead of earnings, Pinterest Faces Slowdown in Advertiser Spend in APAC Region, UBS Says, Mag 7 stocks deliver earnings beats but results get mixed market response, SK hynix Sees HBM Growing 30% Annually"

        return f"Latest news for {stock_symbol}: {latest_news}"

    @tool
    def get_stock_price(stock_symbol: str) -> str:
        """Get the current stock price for a given stock symbol."""        
        try:
            stock = yf.Ticker(stock_symbol)
            price = stock.history(period="1d")['Close'].iloc[-1]
        except Exception as e:
            print(f"Error fetching price for {stock_symbol}: {str(e)}")
            price = 221.30
        
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
            #agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            agent_type=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True
        )   
    
    def ask(self, question: str):
        """Ask a question to the agent and get a response."""
        response = self.agent.run(question)
        return response

    def get_stock_prompt(self, stock_symbol: str):
        """Get a prompt for the stock symbol."""
        prompt = PromptTemplate.from_template("""
                    You are a financial assistant agent who can help users with:
                    - Looking up stock prices
                    - Performing calculations
                    - Fetching stock-related news
                    
                                              
                    Always respond in a concise and professional tone.
                    If you're unsure or the tool returns nothing, let the user know politely.

                    Use below format to respond:

                    Title : create a right title as per the user question
                    
                    Stock Information 
                                              
                    Stock Name : name of the stock    Stock Price: current price of the stock
                    Stock News : latest news related to the stock

                    Next Steps:
                    - Prepare these question which can be asked to the user in next step.
                                                   
                                                                        
                    Begin!

                    Question: {input}
                    {agent_scratchpad}
                    """)
        return f"What is the current price of {stock_symbol}?"