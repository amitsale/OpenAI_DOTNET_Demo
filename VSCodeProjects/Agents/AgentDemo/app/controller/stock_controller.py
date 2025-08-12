from fastapi import APIRouter
from app.service.stock_service import StockService

router = APIRouter()

class StockController:
    def __init__(self):
        self.stock_service = StockService()

    def stock_information(self, userquery: str) :
        print(f"Received userquery 1 : {userquery}", flush=True)  # Add flush=True for immediate output
        return self.stock_service.stock_information(userquery)

stock_controller = StockController()

@router.get("/V1/Api/Stock")
def stock_information(userquery: str) :
    raise Exception("debug test")
    print(f"Received userquery: {userquery}", flush=True)  # Add flush=True for immediate output
    return stock_controller.stock_information(userquery)

@router.get("/V1/Api/Stock/check_connection")
def check_connection():
    """
    Endpoint to check the connection status of the stock service.
    """
    print("Checking connection to stock service", flush=True)  # Add flush=True for immediate output
    return "Connected successfully to stock service"