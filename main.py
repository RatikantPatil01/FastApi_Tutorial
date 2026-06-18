from fastapi import FastAPI
from typing import Optional

app = FastAPI() # This is The Object Or Instance Of Fast Api Class So At First We Need To Create Its Intance

@app.get("/") # This is simply defining the route for our project @app Means FastApi .get Means Api Type And ("/") Means Route Location
def root_page(): # In This def Stands For Function and After that root_page is nothing but function name you use whatever you want
    # This is the main box here you write all your logical code and do the calculations or the operations 
    return {"Message":"First Work Broo !!"} # This Was the part to return value to an user or frontend

@app.get("/greet") # Here is Nothing But i just defined route that is ("/greet") you use whatever you want depending upon your model okayy ..
def greet():
    return {"Message":"This is greet Message !!"}

# Path Parameter
@app.get("/path-parameter/{name}") # This Is Path Parameter Where You Can Send One Value Dynamically From url and it would accept it .
def path_parameter(name :str): # For Accepting The Values From Route Or Sending Any Value To Function You Have To Write Key And It's Data-Type
    return {"Message":f"This is {name}"}  # Using f you can show or call any value in string ...

# Query Parameter
@app.get("/query-parameter")
def query_parameter(name:str , age:int): # Here You Have To Mention Which Keys Are You Accepting And Its Datatypes if wrong key and datatype receive then it throw error
    return {"Message":f"Heyy its {name} And i am {age} Year Old "}

# Path And Query Parameter One Value Goes From Url And Another From Body 
@app.get("/path-query-parameter/{name}")
def path_query_parameter(name:str , age:int):
    return {"Message":f"Heyy Its Path And Query Mix It Work For Both Okayy name = {name} , age = {age}"}

# Path And Query One Optional Parameter But From Both Value Some Value Is Optional 
@app.get("/path-optional-query-parameter/{name}")
def path_query_parameter(name:str , age: Optional[int] = None):
    return {"Message":f"Heyy Its Path And Query Mix It Work For Both Okayy name = {name} , age = {age}"}

# Path And Query Both Optional Parameter But From Both Value Are Optional 
@app.get("/path-optional-query-optional-parameter")
def path_query_parameter(name:Optional[str]=None , age: Optional[int] = None):
    return {"Message":f"Heyy Its Path And Query Mix It Work For Both Okayy name = {name} , age = {age}"}