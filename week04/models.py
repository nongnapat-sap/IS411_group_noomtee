from sqlmodel import SQLModel, Field
from pydantic import BaseModel

engine = create_engine("sqlite:///database.db")

def init_db():
    SQLModel.metadata.create_all(engine)


class TripDB(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    destination: str
    duration: int
    price: float
    group_size: int

class TravellerDB(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    first_name : str
    last_name: str
    age: int

engine = create_engine("sqlite:///database.db")
SQLModel.metadata.create_all(engine)

class Trip(BaseModel):
    name: str
    destination: str
    duration: int
    price: float
    group_size: int

class TripOut(Trip):
    id: int