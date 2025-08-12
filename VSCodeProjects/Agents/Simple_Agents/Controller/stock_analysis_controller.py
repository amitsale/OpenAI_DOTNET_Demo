from fastapi import APIRouter, HTTPException
from Service.StockAnalysis.stock_analysis_service import StockAnalysisService
from Service.StockAnalysis.stock_analysis_interface import IStockAnalysis

router = APIRouter()

@router.get("/CheckConnection")
def check_connection():
    return "Connection to the service is successful"


@router.get("/stock/{symbol}")
def analyze_stock(symbol: str):
    service = StockAnalysisService()
    result = service.analyze(symbol)
    if not result:
        raise HTTPException(status_code=404, detail="Stock not found")
    return result
