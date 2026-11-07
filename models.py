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
    area_id: int
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

# =========================================================
# USER
# =========================================================

class User(BaseModel):
    username: str
    name: str
    email: str
    password_hash: str
    bio: Optional[str] = None
    profile_image_url: Optional[str] = None
    nationality: Optional[str] = None
    preferred_language: Optional[str] = None


class UserOut(User):
    user_id: int
    created_at: datetime
    updated_at: datetime


class UserDB(SQLModel, table=True):
    __tablename__ = "users"
    user_id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)  # แนะนำให้ unique
    name: str
    email: str
    password_hash: str
    bio: Optional[str] = None
    profile_image_url: Optional[str] = None
    nationality: Optional[str] = None
    preferred_language: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# =========================================================
# VIBE
# =========================================================
class Vibe(BaseModel):
    vibe_name: str
    description: Optional[str] = None

class VibeOut(Vibe):
    vibe_id: int

class VibeDB(SQLModel, table=True):
    __tablename__ = "vibes"
    vibe_id: Optional[int] = Field(default=None, primary_key=True)
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


class JournalOut(Journal):
    id: int
    created_at: datetime
    updated_at: datetime


class JournalDB(SQLModel, table=True):
    __tablename__ = "journals"
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int
    place_id: int
    title: Optional[str] = None
    rating: int
    note: Optional[str] = None
    visited_at: Optional[datetime] = None
    image_url: Optional[str] = None
    is_public: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# =========================================================
# Favorite
# =========================================================
class Favorite(BaseModel):
    user_id: int
    place_id: int


class FavoriteOut(Favorite):
    favorite_id: int
    created_at: datetime

class FavoriteDB(SQLModel, table=True):
    __tablename__ = "favorites"
    favorite_id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int
    place_id: int
    created_at: datetime = Field(default_factory=datetime.utcnow)

# =========================================================
# PLACE_VIBES
# =========================================================
class PlaceVibe(BaseModel):
    place_id: int
    vibe_id: int


class PlaceVibeOut(PlaceVibe):
    pass


class PlaceVibeDB(SQLModel, table=True):
    __tablename__ = "place_vibes" ##composite primary key
    place_id: int = Field(primary_key=True)
    vibe_id: int = Field(primary_key=True)

from sqlmodel import Field, SQLModel, UniqueConstraint

# =========================================================
# FOLLOWS (ผู้ติดตาม และ การติดตาม)
# =========================================================
class Follow(BaseModel):
    follower_id: int
    following_id: int

class FollowOut(Follow):
    follow_id: int
    created_at: datetime

class FollowDB(SQLModel, table=True):
    __tablename__ = "follows"
    # ป้องกันการกดติดตามคนเดิมซ้ำ
    __table_args__ = (UniqueConstraint("follower_id", "following_id", name="unique_follow"),)
    
    follow_id: Optional[int] = Field(default=None, primary_key=True)
    follower_id: int = Field(foreign_key="users.user_id")
    following_id: int = Field(foreign_key="users.user_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)

# =========================================================
# LISTS (Collections ของสถานที่ หรือ Playlist สถานที่)
# =========================================================
class PlaceList(BaseModel):
    user_id: int
    list_name: str
    description: Optional[str] = None
    cover_image_url: Optional[str] = None
    is_public: bool = True  # True = 1 (Public), False = 0 (Private)

class PlaceListOut(PlaceList):
    list_id: int
    created_at: datetime

class PlaceListDB(SQLModel, table=True):
    __tablename__ = "lists"
    
    list_id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.user_id")
    list_name: str
    description: Optional[str] = None
    cover_image_url: Optional[str] = None
    is_public: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)

# =========================================================
# LIST_PLACES (ความสัมพันธ์ระหว่าง List และ สถานที่)
# =========================================================
class ListPlace(BaseModel):
    list_id: int
    place_id: int
    position: int = 0

class ListPlaceOut(ListPlace):
    added_at: datetime

class ListPlaceDB(SQLModel, table=True):
    __tablename__ = "list_places"
    # ใช้ Composite Primary Key (list_id + place_id) ป้องกันการเพิ่มสถานที่เดิมซ้ำใน List เดียวกัน
    
    list_id: int = Field(foreign_key="lists.list_id", primary_key=True)
    place_id: int = Field(foreign_key="places.place_id", primary_key=True)
    position: int = 0
    added_at: datetime = Field(default_factory=datetime.utcnow)

# =========================================================
# SAVED_LISTS (รายการ List ที่ User เซฟเก็บไว้)
# =========================================================
class SavedList(BaseModel):
    user_id: int
    list_id: int

class SavedListOut(SavedList):
    saved_list_id: int
    created_at: datetime

class SavedListDB(SQLModel, table=True):
    __tablename__ = "saved_lists"
    # ป้องกันไม่ให้ User เซฟ List เดิมซ้ำหลายครั้ง
    __table_args__ = (UniqueConstraint("user_id", "list_id", name="unique_saved_list"),)
    
    saved_list_id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.user_id")
    list_id: int = Field(foreign_key="lists.list_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)