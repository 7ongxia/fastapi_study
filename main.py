# `FastAPI` is a Python class that provides all the functionality for the API
from fastapi import FastAPI

# `app` variable will be an instance of the FastAPI class.
app = FastAPI()

# Path Operation Decorator
@app.get("/")
# Path Operation Function 
# In this case, it is an async function. Refer https://fastapi.tiangolo.com/async/ for more details
async def root():
    # Return the content. You can also return Pydantic models.
    return {"message": "Hello World"}

"""
run the server
> uvicorn main:app --reload
> main: the file `main.py`
> app: the object created inside of `main.py` with the line `app = FastAPI()`
> --reload: make the server restart after code changes. Only use for development

Interactive API Docs
> http://127.0.0.1:8000/docs
> http://127.0.0.1:8000/redoc

OpenAPI
> FastAPI generates a schema with all the API using the OpenAPI standard for defining APIs.
> API schema and Data schema (JSON schema format)
> The OpenAPI schema is what powers the two interactive documentation systems included.
"""