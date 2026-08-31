from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlmodel import Field, Session, SQLModel, create_engine, select
from database import engine, init_DB
from models import TripDB, TripOut


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

app = FastAPI()

@app.get("/trips/{trip_id}")
async def read_trip(trip_id: int) -> TripOut:
    with Session(engine) as session:
        statement = select(TripDB).where(TripDB.id == trip_id)
        trip = session.exec(statement).first()
 
        if trip != None:
            print(trip)
            return trip
        
    raise HTTPException(
        status_code=404,
        detail="Trip not found"
    )

def get_tripdb():
    with Session(engine) as session:
        statement = select(TripDB).where(TripDB.id == 3)
        trip = session.exec(statement).first()
        print(trip)

def insert_tripdb():
    trip_1 = TripDB(name='Sea', destination='Hua Hin', duration=10, price=10000.0, group_size=90)
    trip_2 = TripDB(name='Mountain', destination='Khao yai', duration=10,price=15000.0, group_size=90)
    trip_3 = TripDB(name='Canel', destination='Amphawa', duration=90, price=8000.0, group_size=90)

    with Session(engine) as session:
        session.add(trip_1)
        session.add(trip_2)
        session.add(trip_3)
        session.commit()    




