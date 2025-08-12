from pydantic import BaseModel
from Entity.Employee.employee_model import EmployeeModel
 
class ApiRequest(BaseModel):
    """
    Represents the API request structure.
    """
    tranId : str
    userid : str
    inputdata : EmployeeModel
class ErrorModel(BaseModel):
    """
    Represents the error model for API responses.
    """
    errorId : int 
    errorMessage : str
    errorDetails : str | None = None
    errorCode : str | None = None
    
class ApiResponse(BaseModel):
    """
    Represents the API response structure.
    """
    tranId : str
    status : str
    message : str
    result : EmployeeModel | None = None
    error : ErrorModel  | None = None  

