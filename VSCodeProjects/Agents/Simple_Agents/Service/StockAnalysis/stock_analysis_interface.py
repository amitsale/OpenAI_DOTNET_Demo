from abc import ABC, abstractmethod

class IStockAnalysis(ABC):
    @abstractmethod
    def analyze(self, symbol: str) -> dict:
        pass
