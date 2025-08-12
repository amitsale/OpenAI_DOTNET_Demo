from abc import ABC, abstractmethod

class StockServiceInterface(ABC):
    @abstractmethod
    def stock_information(self, userquery: str) :
        pass
    
  