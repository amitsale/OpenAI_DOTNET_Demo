import os 
from dotenv import load_dotenv
from langchain.agents import Tool , initialize_agent, AgentType
from langchain.tools import tool
from langchain_experimental.tools.python.tool import PythonREPLTool
from langchain_openai.chat_models import ChatOpenAI as OpenAI
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
import pickle
import os 

import yfinance as yf

load_dotenv()

class StockMemoryAgent:

    def __init__(self):
        self.OPENAI_API_KEY = os.getenv("OPENAIKEY")
        self.llm = OpenAI(temperature=0, model="gpt-4",openai_api_key=self.OPENAI_API_KEY)
        
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        '''
        # Step 1: Load or initialize memory
        self.memory_file = "chat_memory.pkl"

        if os.path.exists(self.memory_file):
            with open(self.memory_file, "rb") as f:
                self.memory = pickle.load(f)
        else:
            self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        '''
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
            #agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,           
            agent_type=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,            
            verbose=True,
            memory = self.memory,
            PromptTemplate = self.get_stock_prompt()
        )   
    
    def ask(self, question: str):
        """Ask a question to the agent and get a response."""
        response = self.agent.run(question)

        # Step 3: Save memory after use
        # with open(self.memory_file, "wb") as f:
        #     pickle.dump(self.memory, f)

        return response

    def get_stock_prompt(self):
        """Get a prompt for the stock symbol."""
        prompt = PromptTemplate(
                input_variables = ["chat_history", "input", "agent_scratchpad"],
                template="""
                    You are a financial assistant agent who can help users with:
                    - Looking up stock prices
                    - Performing calculations
                    - Fetching stock-related news
                    
                    Always provide relevant, context-aware answers using the conversation history.                                              
                    Always respond in a concise and professional tone.
                    If you're unsure or the tool returns nothing, let the user know politely.

                    Use below format to respond:

                    Title : create a right title as per the user question
                    
                    Stock Information 
                                              
                    Stock Name : name of the stock    Stock Price: current price of the stock
                    Stock News : latest news related to the stock

                    Next Steps:
                    - Prepare these question which can be asked to the user in next step.
                                                   
                    Chat history:
                    {chat_history}                                                    
                  

                    Current Question: {input}
                    {agent_scratchpad}

                    your response:
                    """)    
        #return f"What is the current price of {stock_symbol}?"
        return prompt