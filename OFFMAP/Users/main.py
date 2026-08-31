from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlmodel import Field, Session, SQLModel, create_engine, select
from datetime import datetime

# ---------- Database Table ----------

class UserDB(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    email: str
    password_hash: str
    profile_image_url: str | None = None
    nationality: str | None = None
    preferred_language: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

engine = create_engine("sqlite:///database.db")
SQLModel.metadata.create_all(engine)

# ---------- Pydantic Models ----------

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

# ---------- READ all users ----------
@app.get("/users/")
async def read_users() -> list[UserOut]:
    with Session(engine) as session:
        statement = select(UserDB)
        users = session.exec(statement).all()
        return users

# ---------- READ 1 user (ผ่าน SQLModel) ----------
@app.get("/users/{user_id}")
async def read_user(user_id: int) -> UserOut:
    with Session(engine) as session:
        statement = select(UserDB).where(UserDB.id == user_id)
        user = session.exec(statement).first()

        if user != None:
            print(user)
            return user

    raise HTTPException(
        status_code=404,
        detail="User not found"
    )

# ---------- CREATE new user ----------
@app.post("/users/")
async def create_user(user: User) -> UserOut:
    new_user = UserDB(**user.model_dump())

    with Session(engine) as session:
        session.add(new_user)
        session.commit()
        session.refresh(new_user)

        return new_user

# ---------- UPDATE user ----------
@app.put("/users/{user_id}")
async def update_user(user_id: int, user: User) -> UserOut:
    with Session(engine) as session:
        statement = select(UserDB).where(UserDB.id == user_id)
        db_user = session.exec(statement).first()

        if db_user is None:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        for key, value in user.model_dump().items():
            setattr(db_user, key, value)

        session.add(db_user)
        session.commit()
        session.refresh(db_user)

        return db_user

# ---------- DELETE user ----------
@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    with Session(engine) as session:
        user = session.get(UserDB, user_id)

        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        session.delete(user)
        session.commit()

        return {"message": "User deleted successfully"}


# ---------- ฟังก์ชันช่วยเทส ----------

def get_userdb():
    with Session(engine) as session:
        statement = select(UserDB).where(UserDB.id == 3)
        user = session.exec(statement).first()
        print(user)

def insert_userdb():
    user_1 = UserDB(
        name='Kendall Jenner',
        email='kendall.jenner@example.com',
        password_hash='hashed_pw_001',
        profile_image_url='https://example.com/images/kendall.jpg',
        nationality='American',
        preferred_language='English'
    )
    user_2 = UserDB(
        name='Jacob Elordi',
        email='jacob.elordi@example.com',
        password_hash='hashed_pw_002',
        profile_image_url='https://example.com/images/jacob.jpg',
        nationality='Australian',
        preferred_language='English'
    )
    user_3 = UserDB(
        name='Zendaya Kim',
        email='zendaya.kim@example.com',
        password_hash='hashed_pw_003',
        profile_image_url='https://example.com/images/zendaya.jpg',
        nationality='Korean',
        preferred_language='Korean'
    )

    with Session(engine) as session:
        session.add(user_1)
        session.add(user_2)
        session.add(user_3)
        session.commit()