from sqlmodel import SQLModel, create_engine
from models import (
    AreaDB, PlaceDB, UserDB,
    VibeDB, JournalDB, FavoriteDB, PlaceVibeDB,
)

engine = create_engine("sqlite:///database.db")

def init_db(): ## DDL
    SQLModel.metadata.create_all(engine)