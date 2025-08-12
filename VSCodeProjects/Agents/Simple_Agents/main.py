from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn
from Controller.stock_analysis_controller import router as stock_router

app = FastAPI()
app.include_router(stock_router)

@app.get("/")
def read_root():
    return JSONResponse(content={"message": "Hello, World! This is your FastAPI placeholder endpoint."})

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
