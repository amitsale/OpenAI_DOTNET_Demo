from pydantic import BaseModel

class EmployeeModel(BaseModel):
    """
    Represents the model for an employee.
    """
    employeeId : int 
    firstName  : str
    lastName   : str
    email      : str
    phone      : str
    department : str
    position   : str
    salary     : float
    isActive   : bool
    startDate  : str
    endDate    : str | None = None

