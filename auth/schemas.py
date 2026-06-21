# In This File We Are Mentioning All Pydantic Model 
# A Pydantic Model is a Python class used to define the structure of data, validate user input, and convert data into the correct types automatically in FastAPI APIs. It helps ensure that only valid data is accepted and processed.

from pydantic import BaseModel, EmailStr

# TO Create New Users
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role :str

# To Authentication
class UserLogin(BaseModel):
    username:str
    password:str