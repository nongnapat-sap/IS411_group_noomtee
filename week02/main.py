from fastapi import FastAPI
from pydantic import BaseModel

class Ticket(BaseModel):
    name:str
    description: str | None = None
    price: float
    tax: float | None = None

app = FastAPI()

fake_user_db = [
        {'username': 'Karina'},
        {'username': 'Winter'},
        {'username': 'Ningning'},
        {'username': 'Giselle'},
    ]

@app.get("/")
def read_item():
    return {"Hello": "Chanyapak"}

@app.get("/users/")
def get_user(skip: int = 0, limit: int = 10):
    return fake_user_db[skip : skip + limit]


@app.get('/user/{user_id}')
def get_user(user_id: int):
    return {'user_id': user_id}

@app.post("/ticket/")
def create_ticket(ticket: Ticket) -> Ticket:
    ticket.tax = ticket.price * 0.7
    return ticket 