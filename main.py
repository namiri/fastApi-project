from fastapi import FastAPI, HTTPException
from typing import Union, List
from models import User, Gender, Role,UserUpdateRequest
from uuid import uuid4, UUID

from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
from tensorflow.keras.models import load_model

# Load your trained neural network model
model = load_model('CV_similarirty.ipynb')

app= FastAPI()

class InputData(BaseModel):
    # Define your input data schema using Pydantic BaseModel
    feature1: float
    feature2: float
    # Add more features as needed


db: List[User] = [
    User(id=UUID("06805e9c-eaf1-4428-8f88-ce542ed1aa1f"), first_name="nd", last_name="am", middle_name="bh", gender=Gender.female, roles=[Role.student]),
    User(id=UUID("a64a2d23-0932-419e-9af7-c8657eae5708"), first_name="al", last_name="am", middle_name="ll", gender=Gender.male, roles=[Role.admin, Role.user])
]

@app.get("/")
async def root():
    # await foo()
    return {"Hello":"World"}


@app.get("/api/users")
async def fetch_users():
    return db;

@app.post("/api/users")
async def reg_user(user:User):
    db.append(user)
    return {"id":user.id};

@app.delete("/api/users/{user_id}")
async def delete_user(user_id:UUID):
    # loop
    for user in db:
        if user.id == user_id:
            db.remove(user)
            return {"ok"};
    raise HTTPException(
        status_code=404,
        detail=f"user {user_id} not found",
        headers={"X-Custom-Header": "foobar"}
    )

@app.put("/api/users/{user_id}")
async def update_user(user_update: UserUpdateRequest, user_id: UUID): 
    for user in db:
        if user.id == user_id:
            if user_update.first_name is not None:
                user.first_name= user_update.first_name
            if user_update.last_name is not None:
                user.last_name= user_update.last_name  
            if user_update.middle_name is not None:
                user.middle_name= user_update.middle_name 
            if user_update.roles is not None:
                user.roles= user_update.roles
            return 
    raise HTTPException(
            status_code=404,
            detail=f"user {user_id} not found",
            headers={"X-Custom-Header": "foobar"}
        )
@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}    