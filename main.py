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

from enum import Enum
from pydantic import BaseModel
# `FastAPI` is a Python class that provides all the functionality for the API
from fastapi import FastAPI


# To declare a request body, use Pydantic models with all their power and benefits
# Usually GET operation is not suitable for receiving the request body
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


# Import Enum and create a sub-class that inherits from str and from Enum
class ModelName(str, Enum):
    alexnet = "ALEXNET"
    resnet = "RESNET"
    lenet = "LENET"


# `app` variable will be an instance of the FastAPI class.
app = FastAPI()


# Path Operation Decorator
@app.get("/")
# Path Operation Function 
# In this case, it is an async function. Refer https://fastapi.tiangolo.com/async/ for more details
async def root():
    # Return the content. You can also return Pydantic models.
    return {"message": "Hello World"}


@app.get("/items/{item_id}")
# With the type declaration, FastAPI gives you automatic request "parsing"
# With the type declaration, FastAPI gives you data validation.
# All the data validation is performed under the hood by Pydantic.
# Optional Query Parameter (which is not part of the path parameters)
async def read_item(item_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


# path operations are evaluated in order, you need to make sure that the path for `/users/me` is declared before the one for `/users/{user_id}`
# Otherwise, the path for `/users/{user_id}` would match also for `/users/me`, "thinking" that it's receiving a parameter `user_id` with a value of "me"
@app.get("/users/me")
async def read_user_me():
    return {"user_id": "I am you."}


@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}


@app.get("/models/{model_name}")
# Create a path parameter with a type annotation using the enum class, `ModelName`
async def get_model(model_name: ModelName):
    # You can compare it with the enumeration member in your created enum `ModelName`
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    # You can get the actual value using `model_name.value`
    if model_name.value == ModelName.lenet.value:
        return {"model_name": model_name, "message": "LeCNN all the images"}
    # You can return enum members from your path operation, even nested in a JSON body.
    # They will be converted to their corresponding values before returning them.
    return {"model_name": model_name, "message": "Have some residuals"}


# Path parameters containing paths
# Using an option directly from Starlette, you can declare a path parameter containing a path using a URL like: /files/{file_path:path}
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}


# Multiple path and query parameters
# no need to declare them in any specific order (detected by name)
"""
3 types of query parameters
- needy, a required parameter
- parameter with default value
- optional parameter
"""
@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: str | None = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


"""
With just that Python type declaration, FastAPI will
1. Read the body of the request as JSON
2. Convert the corresponding types (if needed)
3. Validate the data
3.1. if the data is invalid, it will return a nice and clear error
4. Give you the received data in the parameter
5. Generate JSON schema definitions for your model

[ Request body + path + query parameters ]
The function parameters will be recognized as follows
1. if the parameter is also declared in the path, it will be used as a path parameter.
2. if the parameter is of a singular type (int, float, str, bool, etc), it will be interpreted as a query parameter.
3. if the parameter is declared to be of the type of a Pydantic model, it will be interpreted as a request body.

"""
@app.put("/items/{item_id}")
# Declare class `Item` as a query parameter's data type, and it will work as a request
async def create_item(item_id: int, item: Item):
    # You can declare path parameters and request body at the same time. FastAPI will recognize that are declared to be Pydantic models should be taken from the request body.
    return {"item_id": item_id, **item.model_dump()}