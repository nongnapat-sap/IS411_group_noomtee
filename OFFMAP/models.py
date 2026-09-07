from typing import Optional
from datetime import datetime

from pydantic import BaseModel
from sqlmodel import Field, SQLModel


# =========================================================
# AREA
# =========================================================

class Area(BaseModel):
    area_name: str
    district: str
    sub_district: Optional[str] = None
    latitude: float
    longitude: float
    description: Optional[str] = None
    cover_image_url: Optional[str] = None
    total_places: int = 0


class AreaOut(Area):
    area_id: int


class AreaDB(SQLModel, table=True):
    __tablename__ = "areas"

    area_id: Optional[int] = Field(default=None, primary_key=True)
    area_name: str
    district: str
    sub_district: Optional[str] = None
    latitude: float
    longitude: float
    description: Optional[str] = None
    cover_image_url: Optional[str] = None
    total_places: int = 0


# =========================================================
# PLACE
# =========================================================

class Place(BaseModel):
    place_name: str
    description: str
    area_id: int
    address: str
    latitude: float
    longitude: float
    price_level: str
    opening_time: str
    closing_time: str
    booking_link: Optional[str] = None
    image_url: Optional[str] = None


class PlaceOut(Place):
    place_id: int


class PlaceDB(SQLModel, table=True):
    __tablename__ = "places"

    place_id: Optional[int] = Field(default=None, primary_key=True)
    place_name: str
    description: str
    area_id: int = Field(foreign_key="areas.area_id")
    address: str
    latitude: float
    longitude: float
    price_level: str
    opening_time: str
    closing_time: str
    booking_link: Optional[str] = None
    image_url: Optional[str] = None


# =========================================================
# USER
# =========================================================

class User(BaseModel):
    name: str
    email: str
    password_hash: str
    profile_image_url: Optional[str] = None
    nationality: Optional[str] = None
    preferred_language: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class UserOut(User):
    user_id: int


class UserDB(SQLModel, table=True):
    __tablename__ = "users"

    user_id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    password_hash: str
    profile_image_url: Optional[str] = None
    nationality: Optional[str] = None
    preferred_language: Optional[str] = None
    created_at: datetime
    updated_at: datetime


# =========================================================
# VIBE
# =========================================================

class Vibe(BaseModel):
    vibe_name: str
    description: Optional[str] = None


class VibeOut(Vibe):
    id: int


class VibeDB(SQLModel, table=True):
    __tablename__ = "vibes"

    id: Optional[int] = Field(default=None, primary_key=True)
    vibe_name: str
    description: Optional[str] = None


# =========================================================
# JOURNAL
# =========================================================

class Journal(BaseModel):
    user_id: int
    place_id: int
    title: Optional[str] = None
    rating: int
    note: Optional[str] = None
    visited_at: Optional[datetime] = None
    image_url: Optional[str] = None
    is_public: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class JournalOut(Journal):
    id: int


class JournalDB(SQLModel, table=True):
    __tablename__ = "journals"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.user_id")
    place_id: int = Field(foreign_key="places.place_id")
    title: Optional[str] = None
    rating: int
    note: Optional[str] = None
    visited_at: Optional[datetime] = None
    image_url: Optional[str] = None
    is_public: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    