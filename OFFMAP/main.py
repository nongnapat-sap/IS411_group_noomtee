from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
    name: str
    email: str
    password_hash: str
    profile_image_url: str | None = None
    nationality: str | None = None
    preferred_language: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

class UserOut(User):
    id: int

app = FastAPI()

user_db = []

@app.get("/users/")
async def read_users() -> list[UserOut]:
    return user_db

@app.get("/users/{user_id}")
async def read_user(user_id: int) -> UserOut:
    for user in user_db:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

@app.post("/users/")
async def create_user(user: User) -> UserOut:
    new_user = UserOut(id=len(user_db) + 1, **user.model_dump())
    user_db.append(new_user)
    return new_user

@app.put("/users/{user_id}")
async def update_user(user_id: int, user: User) -> UserOut:
    for index, existing_user in enumerate(user_db):
        if existing_user.id == user_id:
            updated_user = UserOut(id=user_id, **user.model_dump())
            user_db[index] = updated_user
            return updated_user
    raise HTTPException(status_code=404, detail="User not found")

@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    for index, existing_user in enumerate(user_db):
        if existing_user.id == user_id:
            del user_db[index]
            return {"message": "User deleted"}
    raise HTTPException(status_code=404, detail="User not found")