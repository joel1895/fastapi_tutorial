from pydantic import BaseModel,EmailStr

class EmployeeBase(BaseModel):
    name: str
    email: EmailStr


class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(EmployeeBase):
    pass

class EmpoloyeeOut(EmployeeBase):
    id: int

    class config:
        orm_mode = True
