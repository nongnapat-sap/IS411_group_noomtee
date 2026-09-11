from sqlmodel import SQLModel, create_engine
from models import AreaDB, PlaceDB, UserDB

engine = create_engine("sqlite:///database.db")

def init_db():
    SQLModel.metadata.create_all(engine)