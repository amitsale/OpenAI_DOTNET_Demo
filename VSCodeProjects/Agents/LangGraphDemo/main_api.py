from fastapi import FastAPI, Request
from pydantic import BaseModel
from agent.stock_agent import StockAgent
from agent.stock_agent_openai_function_calling import FunctionCallingStockAgent
from agent.stock_memory_agent import StockMemoryAgent
from agent.simple_memory_agent import ConversationalAgent
from agent.simple_agent import SimpleAgent

app = FastAPI()

@app.get("/")
def root():
    return {"message": "FastAPI server is running. Available endpoints: /stock-agent, /function-calling-agent, /stock-memory-agent, /conversational-agent, /simple-agent"}


from fastapi import FastAPI, Request
from pydantic import BaseModel
from agent.stock_agent import StockAgent
from agent.stock_agent_openai_function_calling import FunctionCallingStockAgent
from agent.stock_memory_agent import StockMemoryAgent
from agent.simple_memory_agent import ConversationalAgent
from agent.simple_agent import SimpleAgent

app = FastAPI()

class QueryRequest(BaseModel):
    question: str

@app.post("/stock-agent")
def stock_agent_endpoint(request: QueryRequest):
    agent = StockAgent()
    response = agent.ask(request.question)
    return {"response": response}

@app.post("/function-calling-agent")
def function_calling_agent_endpoint(request: QueryRequest):
    agent = FunctionCallingStockAgent()
    response = agent.ask(request.question)
    return {"response": response}

@app.post("/stock-memory-agent")
def stock_memory_agent_endpoint(request: QueryRequest):
    agent = StockMemoryAgent()
    response = agent.ask(request.question)
    return {"response": response}

@app.post("/conversational-agent")
def conversational_agent_endpoint(request: QueryRequest):
    agent = ConversationalAgent()
    response = agent.ask(request.question)
    return {"response": response}

@app.post("/simple-agent")
def simple_agent_endpoint(request: QueryRequest):
    agent = SimpleAgent()
    response = agent.ask(request.question)
    return {"response": response}
