from sqlalchemy import func
from contextlib import asynccontextmanager
from sqlalchemy.exc import IntegrityError
from fastapi import FastAPI, HTTPException, status
from sqlmodel import Session, select
from database import engine, init_db
from datetime import datetime
from models import (
    AreaDB, Area, AreaOut,
    PlaceDB, Place, PlaceOut,
    UserDB, User, UserOut,
    VibeDB, Vibe, VibeOut,
    JournalDB, Journal, JournalOut,
    Favorite, FavoriteOut, FavoriteDB,
    PlaceVibe, PlaceVibeOut, PlaceVibeDB,
    FollowDB, Follow, FollowOut,
    PlaceListDB, PlaceList, PlaceListOut,
    ListPlaceDB, ListPlace, ListPlaceOut,
    SavedListDB, SavedList, SavedListOut
)


def seed_data():
    with Session(engine) as session:

        # =========================
        # AREA
        # =========================
        existing_area = session.exec(select(AreaDB)).first()

        if not existing_area:
            areas = [
                AreaDB(area_name="Ratchathewi", district="Ratchathewi", sub_district="Thanon Phaya Thai", latitude=13.7563, longitude=100.5330, description="Home to Victory Monument and classic live-music venues", cover_image_url="https://example.com/images/ratchathewi.jpg"),
                AreaDB(area_name="Sukhumvit", district="Watthana", sub_district="Khlong Toei Nuea", latitude=13.7400, longitude=100.5600, description="Bangkok's nightlife hub with speakeasies and rooftop bars", cover_image_url="https://example.com/images/sukhumvit.jpg"),
                AreaDB(area_name="Thonglor", district="Watthana", sub_district="Khlong Tan Nuea", latitude=13.7300, longitude=100.5800, description="Trendy district known for upscale clubs and cocktail bars", cover_image_url="https://example.com/images/thonglor.jpg"),
                AreaDB(area_name="Ari", district="Phaya Thai", sub_district="Sam Sen Nai", latitude=13.7797, longitude=100.5445, description="Hip cafe and craft-beer neighborhood", cover_image_url="https://example.com/images/ari.jpg"),
                AreaDB(area_name="Ekkamai", district="Watthana", sub_district="Khlong Tan Nuea", latitude=13.7195, longitude=100.5850, description="Laid-back bars and late-night eats", cover_image_url="https://example.com/images/ekkamai.jpg"),
                AreaDB(area_name="Silom", district="Bang Rak", sub_district="Silom", latitude=13.7248, longitude=100.5340, description="Business district by day, nightlife strip by night", cover_image_url="https://example.com/images/silom.jpg"),
                AreaDB(area_name="Sathorn", district="Sathon", sub_district="Thung Wat Don", latitude=13.7180, longitude=100.5290, description="Rooftop bars and skyline views", cover_image_url="https://example.com/images/sathorn.jpg"),
                AreaDB(area_name="Chinatown", district="Samphanthawong", sub_district="Chakkrawat", latitude=13.7398, longitude=100.5088, description="Historic street-food and neon-lit alleys", cover_image_url="https://example.com/images/chinatown.jpg"),
            ]
            session.add_all(areas)
            session.commit()

        # =========================
        # PLACE
        # =========================
        existing_place = session.exec(select(PlaceDB)).first()

        if not existing_place:
            places = [
                PlaceDB(place_name="Saxophone Pub & Restaurant", description="A legendary live jazz music venue", area_id=1, address="3/8 Soi Ratchawithi 11, Ratchathewi, Bangkok 10400", latitude=13.7500, longitude=100.5000, price_level="200-1000 THB", opening_time="18:00", closing_time="02:00", booking_link=None, image_url=None),
                PlaceDB(place_name="Havana Social", description="A hidden 1940s pre-revolutionary Cuban-themed speakeasy", area_id=2, address="341 Sukhumvit Soi 11, Bangkok 10110", latitude=13.7400, longitude=100.5600, price_level="400-1200 THB", opening_time="18:00", closing_time="02:00", booking_link=None, image_url=None),
                PlaceDB(place_name="Upper House", description="A high-energy nightclub and bar", area_id=3, address="2nd floor of 24 BLVD at 88 Sukhumvit 24 Alley, Bangkok", latitude=13.7500, longitude=100.5700, price_level="400-1200 THB", opening_time="21:00", closing_time="03:30", booking_link=None, image_url=None),
                PlaceDB(place_name="Coco Walk", description="A popular hangout spot with multiple bars and live music", area_id=1, address="Phaya Thai Rd, Ratchathewi, Bangkok", latitude=13.7505, longitude=100.5315, price_level="200-800 THB", opening_time="17:00", closing_time="01:00", booking_link=None, image_url=None),
                PlaceDB(place_name="Ari Beer Garden", description="Outdoor craft-beer taproom with live acoustic sets", area_id=4, address="Soi Ari 4, Phaya Thai, Bangkok", latitude=13.7800, longitude=100.5440, price_level="150-500 THB", opening_time="17:00", closing_time="00:00", booking_link=None, image_url=None),
                PlaceDB(place_name="Ekkamai Rooftop", description="Open-air rooftop with city skyline views", area_id=5, address="Soi Ekkamai 10, Watthana, Bangkok", latitude=13.7200, longitude=100.5855, price_level="300-900 THB", opening_time="18:00", closing_time="01:00", booking_link=None, image_url=None),
                PlaceDB(place_name="Ekkamai Late Bites", description="24-hour street food spot popular after clubbing", area_id=5, address="Soi Ekkamai 4, Watthana, Bangkok", latitude=13.7190, longitude=100.5845, price_level="80-300 THB", opening_time="20:00", closing_time="06:00", booking_link=None, image_url=None),
                PlaceDB(place_name="Silom Soi Speakeasy", description="Unmarked bar tucked in a narrow Silom alley", area_id=5, address="Silom Soi 4, Bang Rak, Bangkok", latitude=13.7250, longitude=100.5335, price_level="350-1000 THB", opening_time="19:00", closing_time="02:00", booking_link=None, image_url=None),
                PlaceDB(place_name="Sky High Sathorn", description="Rooftop bar with panoramic Chao Phraya views", area_id=7, address="Sathorn Rd, Sathon, Bangkok", latitude=13.7185, longitude=100.5285, price_level="500-1500 THB", opening_time="17:30", closing_time="01:00", booking_link=None, image_url=None),
                PlaceDB(place_name="Chinatown Neon Bar", description="Retro neon-lit bar serving Thai-Chinese fusion cocktails", area_id=8, address="Yaowarat Rd, Samphanthawong, Bangkok", latitude=13.7400, longitude=100.5090, price_level="250-700 THB", opening_time="18:00", closing_time="01:00", booking_link=None, image_url=None),
            ]
            session.add_all(places)
            session.commit()

        # =========================
        # UPDATE TOTAL PLACES
        # =========================
        for area in session.exec(select(AreaDB)).all():
            area.total_places = len(
                session.exec(
                    select(PlaceDB).where(PlaceDB.area_id == area.area_id)
                ).all()
            )
            session.add(area)
        session.commit()

        # =========================
        # VIBE
        # =========================
        existing_vibe = session.exec(select(VibeDB)).first()
        if not existing_vibe:
            vibes = [
                VibeDB(vibe_name="High Energy & Clubbing", description="Loud beats, DJ sets, dancing, and late-night party vibes"),
                VibeDB(vibe_name="Rooftop & Skyline", description="Open-air scenic views of the Bangkok skyline and riverfront"),
                VibeDB(vibe_name="Craft Beer & Taproom", description="Artisan beers on tap, casual brewing culture, and relaxed outdoor yards"),
                VibeDB(vibe_name="Street Food & Late Bites", description="Late-night hunger cures, bustling street stalls, and affordable comfort eats"),
                VibeDB(vibe_name="Retro & Neon", description="Nostalgic aesthetics, neon lights, and cultural fusion flair"),
                VibeDB(vibe_name="Waterfront & Chill", description="Breezy riverside settings perfect for calm drinks and conversations"),
            ]
            session.add_all(vibes)
            session.commit()

        # =========================
        # PLACE VIBE
        # =========================
        existing_place_vibe = session.exec(select(PlaceVibeDB)).first()
        if not existing_place_vibe:
            place_vibes = [
                PlaceVibeDB(place_id=1, vibe_id=1),
                PlaceVibeDB(place_id=2, vibe_id=2),
                PlaceVibeDB(place_id=3, vibe_id=3),
                PlaceVibeDB(place_id=5, vibe_id=5),
                PlaceVibeDB(place_id=6, vibe_id=4),
                PlaceVibeDB(place_id=7, vibe_id=6),
            ]
            session.add_all(place_vibes)
            session.commit()

        # =========================
        # USER
        # =========================
        existing_user = session.exec(select(UserDB)).first()
        if not existing_user:
            users = [
                UserDB(username="timothee_c", name="Timothee Chalamet", email="timothee.chalamet@example.com", password_hash="hashed_pw_004", profile_image_url="https://i.pravatar.cc/300?img=4", nationality="French", preferred_language="French"),
                UserDB(username="sydney_s", name="Sydney Sweeney", email="sydney.sweeney@example.com", password_hash="hashed_pw_005", profile_image_url="https://i.pravatar.cc/300?img=5", nationality="American", preferred_language="English"),
                UserDB(username="anya_tj", name="Anya Taylor-Joy", email="anya.taylorjoy@example.com", password_hash="hashed_pw_006", profile_image_url="https://i.pravatar.cc/300?img=6", nationality="British", preferred_language="English"),
                UserDB(username="austin_b", name="Austin Butler", email="austin.butler@example.com", password_hash="hashed_pw_007", profile_image_url="https://i.pravatar.cc/300?img=7", nationality="American", preferred_language="English"),
                UserDB(username="hoyeon_j", name="Hoyeon Jung", email="hoyeon.jung@example.com", password_hash="hashed_pw_008", profile_image_url="https://i.pravatar.cc/300?img=8", nationality="Korean", preferred_language="Korean"),
                UserDB(username="barry_k", name="Barry Keoghan", email="barry.keoghan@example.com", password_hash="hashed_pw_009", profile_image_url="https://i.pravatar.cc/300?img=9", nationality="Irish", preferred_language="English"),
                UserDB(username="rosalia_v", name="Rosalia Vila", email="rosalia.vila@example.com", password_hash="hashed_pw_010", profile_image_url="https://i.pravatar.cc/300?img=11", nationality="Spanish", preferred_language="Spanish"),
                UserDB(username="jung_hy", name="Jung Ho-yeon", email="jung.hoyeon2@example.com", password_hash="hashed_pw_011", profile_image_url="https://i.pravatar.cc/300?img=12", nationality="Korean", preferred_language="English"),
                UserDB(username="charles_m", name="Charles Melton", email="charles.melton@example.com", password_hash="hashed_pw_012", profile_image_url="https://i.pravatar.cc/300?img=13", nationality="American", preferred_language="English"),
                UserDB(username="greta_l", name="Greta Lee", email="greta.lee@example.com", password_hash="hashed_pw_013", profile_image_url="https://i.pravatar.cc/300?img=14", nationality="Korean-American", preferred_language="English"),
            ]
            session.add_all(users)
            session.commit()

        # =========================
        # JOURNAL
        # =========================
        existing_journal = session.exec(select(JournalDB)).first()
        if not existing_journal:
            journals = [
                JournalDB(user_id=4, place_id=1, title="Acoustic & Soulful Jazz Night", rating=5, note="The live saxophone solo was breathtaking. Truly an iconic music haven.", visited_at=datetime(2026, 9, 1, 21, 30), image_url="https://images.unsplash.com/photo-1511192336575-5a79af67a629", is_public=True),
                JournalDB(user_id=5, place_id=2, title="Secret Cuban Phone Booth Adventure", rating=5, note="Loved dialing the hidden code to enter! The rum cocktails and vintage decor were spot on.", visited_at=datetime(2026, 9, 2, 22, 0), image_url="https://images.unsplash.com/photo-1514933651103-005eec06c04b", is_public=True),
                JournalDB(user_id=6, place_id=3, title="Electrifying Beats in Sukhumvit", rating=4, note="Incredible sound system and light show. Packed and loud, great for late-night partying.", visited_at=datetime(2026, 9, 4, 23, 45), image_url="https://images.unsplash.com/photo-1492684223066-81342ee5ff30", is_public=True),
                JournalDB(user_id=7, place_id=5, title="Relaxing Outdoor Craft Pours", rating=4, note="Super chilled vibe under the fairy lights. Great local IPA on tap.", visited_at=datetime(2026, 9, 5, 19, 15), image_url="https://images.unsplash.com/photo-1575037614876-c38a4d44f5b8", is_public=True),
                JournalDB(user_id=8, place_id=6, title="Sunset Cocktails with Skyline Views", rating=5, note="Unbeatable panorama of Bangkok during golden hour. Friendly staff and delicious tapas.", visited_at=datetime(2026, 9, 6, 18, 30), image_url="https://images.unsplash.com/photo-1519671482749-fd09be7ccebf", is_public=True),
            ]
            session.add_all(journals)
            session.commit()

        # =========================
        # FAVORITE
        # =========================
        existing_favorite = session.exec(select(FavoriteDB)).first()
        if not existing_favorite:
            favorites = [
                FavoriteDB(user_id=2, place_id=2),
                FavoriteDB(user_id=3, place_id=3),
                FavoriteDB(user_id=4, place_id=4),
                FavoriteDB(user_id=5, place_id=1),
                FavoriteDB(user_id=6, place_id=2),
                FavoriteDB(user_id=7, place_id=3),
            ]
            session.add_all(favorites)
            session.commit()

        # =========================
        # FOLLOWS
        # =========================
        existing_follow = session.exec(select(FollowDB)).first()
        if not existing_follow:
            follows = [
                FollowDB(follower_id=1, following_id=2),
                FollowDB(follower_id=1, following_id=3),
                FollowDB(follower_id=2, following_id=1),
                FollowDB(follower_id=3, following_id=1),
                FollowDB(follower_id=4, following_id=5),
                FollowDB(follower_id=5, following_id=4),
                FollowDB(follower_id=6, following_id=7),
                FollowDB(follower_id=7, following_id=8),
                FollowDB(follower_id=8, following_id=9),
                FollowDB(follower_id=9, following_id=10),
                FollowDB(follower_id=10, following_id=1),
                FollowDB(follower_id=2, following_id=4),
                FollowDB(follower_id=3, following_id=5),
                FollowDB(follower_id=6, following_id=2),
                FollowDB(follower_id=8, following_id=3),
            ]
            session.add_all(follows)
            session.commit()

        # =========================
        # LISTS (Collections)
        # =========================
        existing_list = session.exec(select(PlaceListDB)).first()
        if not existing_list:
            lists = [
                PlaceListDB(user_id=1, list_name="Ultimate Bangkok Rooftops", description="Best views in the city", cover_image_url="https://images.unsplash.com/photo-1519671482749-fd09be7ccebf", is_public=True),
                PlaceListDB(user_id=2, list_name="Jazz & Chill Night", description="Top live music spots", cover_image_url="https://images.unsplash.com/photo-1511192336575-5a79af67a629", is_public=True),
                PlaceListDB(user_id=3, list_name="Late Night Eats", description="Where to go after clubbing", cover_image_url="https://images.unsplash.com/photo-1575037614876-c38a4d44f5b8", is_public=True),
                PlaceListDB(user_id=4, list_name="Speakeasy Hunt", description="Hidden bars and secret passwords", cover_image_url="https://images.unsplash.com/photo-1514933651103-005eec06c04b", is_public=True),
                PlaceListDB(user_id=5, list_name="My Secret Spots", description="Private list only for me", cover_image_url="https://images.unsplash.com/photo-1492684223066-81342ee5ff30", is_public=False),
            ]
            session.add_all(lists)
            session.commit()

        # =========================
        # LIST_PLACES (Places in Lists)
        # =========================
        existing_list_place = session.exec(select(ListPlaceDB)).first()
        if not existing_list_place:
            list_places = [
                # List 1 (Rooftops)
                ListPlaceDB(list_id=1, place_id=6, position=1),
                ListPlaceDB(list_id=1, place_id=9, position=2),
                ListPlaceDB(list_id=1, place_id=3, position=3),
                ListPlaceDB(list_id=1, place_id=2, position=4),
                # List 2 (Jazz & Chill)
                ListPlaceDB(list_id=2, place_id=1, position=1),
                ListPlaceDB(list_id=2, place_id=4, position=2),
                ListPlaceDB(list_id=2, place_id=5, position=3),
                # List 3 (Late Night Eats)
                ListPlaceDB(list_id=3, place_id=7, position=1),
                ListPlaceDB(list_id=3, place_id=4, position=2),
                ListPlaceDB(list_id=3, place_id=10, position=3),
                # List 4 (Speakeasy)
                ListPlaceDB(list_id=4, place_id=2, position=1),
                ListPlaceDB(list_id=4, place_id=8, position=2),
                ListPlaceDB(list_id=4, place_id=1, position=3),
                ListPlaceDB(list_id=4, place_id=5, position=4),
                # List 5 (Private)
                ListPlaceDB(list_id=5, place_id=10, position=1),
            ]
            session.add_all(list_places)
            session.commit()

        # =========================
        # SAVED_LISTS
        # =========================
        existing_saved = session.exec(select(SavedListDB)).first()
        if not existing_saved:
            saved_lists = [
                SavedListDB(user_id=2, list_id=1),
                SavedListDB(user_id=3, list_id=1),
                SavedListDB(user_id=4, list_id=1),
                SavedListDB(user_id=8, list_id=1),
                
                SavedListDB(user_id=1, list_id=2),
                SavedListDB(user_id=5, list_id=2),
                SavedListDB(user_id=6, list_id=2),
                SavedListDB(user_id=9, list_id=2),
                
                SavedListDB(user_id=1, list_id=3),
                SavedListDB(user_id=8, list_id=3),
                SavedListDB(user_id=9, list_id=3),
                SavedListDB(user_id=10, list_id=3),
                
                SavedListDB(user_id=10, list_id=4),
                SavedListDB(user_id=2, list_id=4),
                SavedListDB(user_id=7, list_id=4),
            ]
            session.add_all(saved_lists)
            session.commit()    

@asynccontextmanager
async def lifespan(app: FastAPI):
    # ทำงานตอนที่เซิร์ฟเวอร์เริ่มรัน (Startup)
    init_db()
    seed_data()
    yield
    # หากมีโค้ดที่ต้องทำงานตอนปิดเซิร์ฟเวอร์ (Shutdown) ให้ใส่หลัง yield

# ประกาศ FastAPI app โดยผูก lifespan เข้าไป
app = FastAPI(lifespan=lifespan)

# =========================================================
# AREA
# =========================================================
@app.get("/areas/", status_code=status.HTTP_200_OK)
def read_areas() -> list[AreaOut]:
    with Session(engine) as session:
        return session.exec(select(AreaDB)).all()


@app.get("/areas/{area_id}", status_code=status.HTTP_200_OK)
def read_area(area_id: int) -> AreaOut:
    with Session(engine) as session:
        area = session.get(AreaDB, area_id)
        if area is not None:
            return area
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Area not found"
    )


# <-- เพิ่มใหม่: ดูว่า area นี้มี place อะไรบ้าง
@app.get("/areas/{area_id}/places", status_code=status.HTTP_200_OK)
def read_places_in_area(area_id: int) -> list[PlaceOut]:
    with Session(engine) as session:
        area = session.get(AreaDB, area_id)
        if area is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Area not found"
            )
        statement = select(PlaceDB).where(PlaceDB.area_id == area_id)
        return session.exec(statement).all()


@app.post("/areas/", status_code=status.HTTP_201_CREATED)
def create_area(area: Area) -> AreaOut:
    new_area = AreaDB(**area.model_dump())
    with Session(engine) as session:
        session.add(new_area)
        session.commit()
        session.refresh(new_area)
        return new_area


@app.put("/areas/{area_id}", status_code=status.HTTP_200_OK)
def update_area(area_id: int, new_area: Area) -> AreaOut:
    with Session(engine) as session:
        area = session.get(AreaDB, area_id)
        if area is not None:
            area.area_name = new_area.area_name
            area.district = new_area.district
            area.sub_district = new_area.sub_district
            area.latitude = new_area.latitude
            area.longitude = new_area.longitude
            area.description = new_area.description
            area.cover_image_url = new_area.cover_image_url
            session.add(area)
            session.commit()
            session.refresh(area)
            return area
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Area not found"
    )


# =========================================================
# PLACE  (จัดการ 2 entities: Place <-> Area)
# =========================================================
@app.get("/places/", status_code=status.HTTP_200_OK)
def read_places(
    area_id: int | None = None,
    offset: int = 0,
    limit: int = 100
) -> list[PlaceOut]:
    with Session(engine) as session:
        statement = select(PlaceDB)
        if area_id is not None:
            statement = statement.where(PlaceDB.area_id == area_id)
        statement = statement.offset(offset).limit(limit)
        return session.exec(statement).all()


@app.get("/places/{place_id}", status_code=status.HTTP_200_OK)
def read_place(place_id: int) -> PlaceOut:
    with Session(engine) as session:
        place = session.get(PlaceDB, place_id)
        if place is not None:
            return place

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Place not found"
    )


@app.post("/places/", status_code=status.HTTP_201_CREATED)
def create_place(place: Place) -> PlaceOut:
    with Session(engine) as session:
        area = session.get(AreaDB, place.area_id)
        if area is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Area not found"
            )
        new_place = PlaceDB(**place.model_dump())
        session.add(new_place)

        area.total_places += 1
        session.add(area)

        session.commit()
        session.refresh(new_place)
        return new_place


@app.put("/places/{place_id}", status_code=status.HTTP_200_OK)
def update_place(place_id: int, new_place: Place) -> PlaceOut:
    with Session(engine) as session:
        place = session.get(PlaceDB, place_id)
        if place is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Place not found"
            )

        new_area = session.get(AreaDB, new_place.area_id)
        if new_area is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Area not found"
            )

        # <-- เพิ่มใหม่: ถ้าย้าย place ไป area อื่น ให้ sync total_places ทั้งสองฝั่ง
        if place.area_id != new_place.area_id:
            old_area = session.get(AreaDB, place.area_id)
            if old_area is not None:
                old_area.total_places -= 1
                session.add(old_area)

            new_area.total_places += 1
            session.add(new_area)

        place.place_name = new_place.place_name
        place.description = new_place.description
        place.area_id = new_place.area_id
        place.address = new_place.address
        place.latitude = new_place.latitude
        place.longitude = new_place.longitude
        place.price_level = new_place.price_level
        place.opening_time = new_place.opening_time
        place.closing_time = new_place.closing_time
        place.booking_link = new_place.booking_link
        place.image_url = new_place.image_url

        session.add(place)
        session.commit()
        session.refresh(place)
        return place


from sqlalchemy.exc import IntegrityError # ตรวจสอบให้แน่ใจว่า import ตัวนี้ไว้ด้านบนไฟล์ด้วย

# =========================================================
# USER
# =========================================================
@app.get("/users/", status_code=status.HTTP_200_OK)
def read_users() -> list[UserOut]:
    with Session(engine) as session:
        return session.exec(select(UserDB)).all()


@app.get("/users/{user_id}", status_code=status.HTTP_200_OK)
def read_user(user_id: int) -> UserOut:
    with Session(engine) as session:
        user = session.get(UserDB, user_id)
        if user is not None:
            return user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found"
    )


@app.post("/users/", status_code=status.HTTP_201_CREATED)
def create_user(user: User) -> UserOut:
    new_user = UserDB(**user.model_dump())
    with Session(engine) as session:
        session.add(new_user)
        try:
            session.commit()
            session.refresh(new_user)
            return new_user
        except IntegrityError:
            session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username or email already exists"
            )


@app.put("/users/{user_id}", status_code=status.HTTP_200_OK)
def update_user(user_id: int, new_user: User) -> UserOut:
    with Session(engine) as session:
        user = session.get(UserDB, user_id)
        if user is not None:
            user.username = new_user.username # <-- เพิ่มฟิลด์ username
            user.name = new_user.name
            user.email = new_user.email
            user.password_hash = new_user.password_hash
            user.profile_image_url = new_user.profile_image_url
            user.nationality = new_user.nationality
            user.preferred_language = new_user.preferred_language
            user.updated_at = datetime.utcnow()
            
            session.add(user)
            try:
                session.commit()
                session.refresh(user)
                return user
            except IntegrityError:
                session.rollback()
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username or email already exists"
                )

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found"
    )


# ---------------------------------------------------------
# วางโค้ด Block 1 (read_user_followers และ read_user_following)
# ---------------------------------------------------------

@app.get("/users/{user_id}/followers", status_code=status.HTTP_200_OK)
def read_user_followers(user_id: int) -> list[UserOut]:
    with Session(engine) as session:
        statement = select(UserDB).join(FollowDB, FollowDB.follower_id == UserDB.user_id).where(FollowDB.following_id == user_id)
        return session.exec(statement).all()

@app.get("/users/{user_id}/following", status_code=status.HTTP_200_OK)
def read_user_following(user_id: int) -> list[UserOut]:
    with Session(engine) as session:
        statement = select(UserDB).join(FollowDB, FollowDB.following_id == UserDB.user_id).where(FollowDB.follower_id == user_id)
        return session.exec(statement).all()

# =========================================================
# VIBE
# =========================================================
@app.get("/vibes/", status_code=status.HTTP_200_OK)
def read_vibes() -> list[VibeOut]:
    with Session(engine) as session:
        return session.exec(select(VibeDB)).all()


@app.get("/vibes/{vibe_id}", status_code=status.HTTP_200_OK)
def read_vibe(vibe_id: int) -> VibeOut:
    with Session(engine) as session:
        vibe = session.get(VibeDB, vibe_id)
        if vibe is not None:
            return vibe

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Vibe not found"
    )


@app.post("/vibes/", status_code=status.HTTP_201_CREATED)
def create_vibe(vibe: Vibe) -> VibeOut:
    new_vibe = VibeDB(**vibe.model_dump())
    with Session(engine) as session:
        session.add(new_vibe)
        session.commit()
        session.refresh(new_vibe)
        return new_vibe


@app.put("/vibes/{vibe_id}", status_code=status.HTTP_200_OK)
def update_vibe(vibe_id: int, new_vibe: Vibe) -> VibeOut:
    with Session(engine) as session:
        vibe = session.get(VibeDB, vibe_id)
        if vibe is not None:
            vibe.vibe_name = new_vibe.vibe_name
            vibe.description = new_vibe.description
            session.add(vibe)
            session.commit()
            session.refresh(vibe)
            return vibe
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Vibe not found"
    )


# =========================================================
# JOURNAL  (จัดการ 2 entities: Journal <-> User + Place)
# =========================================================
@app.get("/journals/", status_code=status.HTTP_200_OK)
def read_journals(
    user_id: int | None = None,
    place_id: int | None = None,
    offset: int = 0,
    limit: int = 100
) -> list[JournalOut]:
    with Session(engine) as session:
        statement = select(JournalDB).where(JournalDB.is_deleted == False)   # [ASM6] ซ่อนที่ถูกลบ
        if user_id is not None:
            statement = statement.where(JournalDB.user_id == user_id)
        if place_id is not None:
            statement = statement.where(JournalDB.place_id == place_id)
        statement = statement.offset(offset).limit(limit)
        return session.exec(statement).all()


@app.get("/journals/{journal_id}", status_code=status.HTTP_200_OK)
def read_journal(journal_id: int) -> JournalOut:
    with Session(engine) as session:
        journal = session.get(JournalDB, journal_id)
        if journal is not None and not journal.is_deleted:   # [ASM6] ที่ถูกลบถือว่าไม่มี
            return journal
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Journal not found"
    )


@app.post("/journals/", status_code=status.HTTP_201_CREATED)
def create_journal(journal: Journal) -> JournalOut:
    with Session(engine) as session:
        user = session.get(UserDB, journal.user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        place = session.get(PlaceDB, journal.place_id)
        if place is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Place not found"
            )
        new_journal = JournalDB(**journal.model_dump())
        session.add(new_journal)
        session.commit()
        session.refresh(new_journal)
        return new_journal


@app.put("/journals/{journal_id}", status_code=status.HTTP_200_OK)
def update_journal(journal_id: int, new_journal: Journal) -> JournalOut:
    with Session(engine) as session:
        journal = session.get(JournalDB, journal_id)
        if journal is None or journal.is_deleted:   # [ASM6] แก้ journal ที่ถูกลบแล้วไม่ได้
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Journal not found"
            )
        user = session.get(UserDB, new_journal.user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        place = session.get(PlaceDB, new_journal.place_id)
        if place is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Place not found"
            )
        journal.user_id = new_journal.user_id
        journal.place_id = new_journal.place_id
        journal.title = new_journal.title
        journal.rating = new_journal.rating
        journal.note = new_journal.note
        journal.visited_at = new_journal.visited_at
        journal.image_url = new_journal.image_url
        journal.is_public = new_journal.is_public
        journal.is_deleted = new_journal.is_deleted   # [ASM6] ให้ PUT ใช้ทำ soft delete ได้
        journal.updated_at = datetime.utcnow()
        session.add(journal)
        session.commit()
        session.refresh(journal)
        return journal


# <-- เพิ่มใหม่: user ลบ journal ของตัวเองได้
@app.delete("/journals/{journal_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_journal(journal_id: int):
    with Session(engine) as session:
        journal = session.get(JournalDB, journal_id)
        if journal is None or journal.is_deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Journal not found"
            )
        # [ASM6] soft delete: ไม่ลบแถวจริง แค่ทำเครื่องหมายว่าถูกลบ
        journal.is_deleted = True
        journal.updated_at = datetime.utcnow()
        session.add(journal)
        session.commit()
        return


# =========================================================
# FAVORITE  (จัดการ 2 entities: Favorite <-> User + Place)
# =========================================================
@app.get("/favorites/", status_code=status.HTTP_200_OK)
def read_favorites(
    user_id: int | None = None,
    place_id: int | None = None,
    offset: int = 0,
    limit: int = 100
) -> list[FavoriteOut]:
    with Session(engine) as session:
        statement = select(FavoriteDB).where(FavoriteDB.is_deleted == False)   # [ASM6]
        if user_id is not None:
            statement = statement.where(FavoriteDB.user_id == user_id)
        if place_id is not None:
            statement = statement.where(FavoriteDB.place_id == place_id)
        statement = statement.offset(offset).limit(limit)
        return session.exec(statement).all()


@app.get("/favorites/{favorite_id}", status_code=status.HTTP_200_OK)
def read_favorite(favorite_id: int) -> FavoriteOut:
    with Session(engine) as session:
        favorite = session.get(FavoriteDB, favorite_id)
        if favorite is not None and not favorite.is_deleted:   # [ASM6]
            return favorite
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Favorite not found"
    )


@app.post("/favorites/", status_code=status.HTTP_201_CREATED)
def create_favorite(favorite: Favorite) -> FavoriteOut:
    with Session(engine) as session:
        user = session.get(UserDB, favorite.user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        place = session.get(PlaceDB, favorite.place_id)
        if place is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Place not found"
            )
        # [ASM6] validation: ห้าม favorite ซ้ำ / ถ้าเคยลบไว้ให้กู้คืนแถวเดิม
        existing = session.exec(
            select(FavoriteDB).where(
                FavoriteDB.user_id == favorite.user_id,
                FavoriteDB.place_id == favorite.place_id
            )
        ).first()
        if existing is not None and not existing.is_deleted:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This place is already in your favorites"
            )
        if existing is not None:
            existing.is_deleted = False
            session.add(existing)
            session.commit()
            session.refresh(existing)
            return existing

        new_favorite = FavoriteDB(**favorite.model_dump(exclude={"is_deleted"}))
        session.add(new_favorite)
        session.commit()
        session.refresh(new_favorite)
        return new_favorite


# [ASM6] update favorite (ใช้ทำ soft delete: ส่ง is_deleted = true)
@app.put("/favorites/{favorite_id}", status_code=status.HTTP_200_OK)
def update_favorite(favorite_id: int, new_favorite: Favorite) -> FavoriteOut:
    with Session(engine) as session:
        favorite = session.get(FavoriteDB, favorite_id)
        if favorite is None or favorite.is_deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Favorite not found"
            )
        if new_favorite.user_id != favorite.user_id or new_favorite.place_id != favorite.place_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="user_id and place_id cannot be changed"
            )
        favorite.is_deleted = new_favorite.is_deleted
        session.add(favorite)
        session.commit()
        session.refresh(favorite)
        return favorite


@app.delete("/favorites/{favorite_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_favorite(favorite_id: int):
    with Session(engine) as session:
        favorite = session.get(FavoriteDB, favorite_id)
        if favorite is None or favorite.is_deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Favorite not found"
            )
        favorite.is_deleted = True   # [ASM6] soft delete
        session.add(favorite)
        session.commit()
        return


# =========================================================
# PLACE_VIBES
# =========================================================
@app.get("/place-vibes/", status_code=status.HTTP_200_OK)
def read_place_vibes(
    place_id: int | None = None,
    vibe_id: int | None = None,
    offset: int = 0,
    limit: int = 100
) -> list[PlaceVibeOut]:
    with Session(engine) as session:
        statement = select(PlaceVibeDB)
        if place_id is not None:
            statement = statement.where(PlaceVibeDB.place_id == place_id)
        if vibe_id is not None:
            statement = statement.where(PlaceVibeDB.vibe_id == vibe_id)
        statement = statement.offset(offset).limit(limit)
        return session.exec(statement).all()


@app.get("/place-vibes/{place_id}/{vibe_id}", status_code=status.HTTP_200_OK)
def read_place_vibe(place_id: int, vibe_id: int) -> PlaceVibeOut:
    with Session(engine) as session:
        place_vibe = session.get(
            PlaceVibeDB,
            (place_id, vibe_id)
        )
        if place_vibe is not None:
            return place_vibe
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Place-Vibe relationship not found"
    )


@app.post("/place-vibes/", status_code=status.HTTP_201_CREATED)
def create_place_vibe(place_vibe: PlaceVibe) -> PlaceVibeOut:
    with Session(engine) as session:
        place = session.get(PlaceDB, place_vibe.place_id)
        if place is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Place not found"
            )
        vibe = session.get(VibeDB, place_vibe.vibe_id)
        if vibe is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Vibe not found"
            )
        new_place_vibe = PlaceVibeDB(
            place_id=place_vibe.place_id,
            vibe_id=place_vibe.vibe_id
        )
        session.add(new_place_vibe)

        session.commit()
        session.refresh(new_place_vibe)
        return PlaceVibeOut(
            place_id=new_place_vibe.place_id,
            vibe_id=new_place_vibe.vibe_id
        )
@app.delete("/places/{place_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_place(place_id: int):
    with Session(engine) as session:
        place = session.get(PlaceDB, place_id)
        if place is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Place not found"
            )
        # ลบข้อมูลที่ผูกกับ place นี้ก่อน
        for model in (PlaceVibeDB, FavoriteDB, JournalDB):
            for row in session.exec(select(model).where(model.place_id == place_id)).all():
                session.delete(row)
        # sync total_places ของ area
        area = session.get(AreaDB, place.area_id)
        if area is not None and area.total_places > 0:
            area.total_places -= 1
            session.add(area)
        session.delete(place)
        session.commit()
        return

# =========================================================
# FOLLOWS (ผู้ติดตาม และ การติดตาม)
# =========================================================

@app.get("/follows/", status_code=status.HTTP_200_OK)
def read_follows(
    follower_id: int | None = None,
    following_id: int | None = None,
    offset: int = 0,
    limit: int = 100
) -> list[FollowOut]:
    with Session(engine) as session:
        statement = select(FollowDB)
        if follower_id is not None:
            statement = statement.where(FollowDB.follower_id == follower_id)
        if following_id is not None:
            statement = statement.where(FollowDB.following_id == following_id)
        statement = statement.offset(offset).limit(limit)
        return session.exec(statement).all()

@app.post("/follows/", status_code=status.HTTP_201_CREATED)
def create_follow(follow: Follow) -> FollowOut:
    if follow.follower_id == follow.following_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Users cannot follow themselves"
        )
    with Session(engine) as session:
        follower = session.get(UserDB, follow.follower_id)
        following = session.get(UserDB, follow.following_id)
        if follower is None or following is None:
             raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Follower or Following user not found"
            )
            
        new_follow = FollowDB(**follow.model_dump())
        session.add(new_follow)
        try:
            session.commit()
            session.refresh(new_follow)
            return new_follow
        except IntegrityError:
            session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Follow relationship already exists"
            )

@app.delete("/follows/{follow_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_follow(follow_id: int):
    with Session(engine) as session:
        follow = session.get(FollowDB, follow_id)
        if follow is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Follow relationship not found"
            )
        session.delete(follow)
        session.commit()
        return

# =========================================================
# LISTS (Collections ของสถานที่)
# =========================================================
@app.get("/lists/", status_code=status.HTTP_200_OK)
def read_lists(
    user_id: int | None = None,
    is_public: bool | None = None,
    offset: int = 0,
    limit: int = 100
) -> list[PlaceListOut]:
    with Session(engine) as session:
        statement = select(PlaceListDB)
        if user_id is not None:
            statement = statement.where(PlaceListDB.user_id == user_id)
        if is_public is not None:
             statement = statement.where(PlaceListDB.is_public == is_public)
        statement = statement.offset(offset).limit(limit)
        return session.exec(statement).all()

@app.get("/lists/popular", status_code=status.HTTP_200_OK)
def read_popular_lists(days: int = 7, limit: int = 10) -> list[PlaceListOut]:
    with Session(engine) as session:
        statement = (
            select(PlaceListDB)
            .join(
                SavedListDB,
                (SavedListDB.list_id == PlaceListDB.list_id) & (SavedListDB.is_deleted == False),   # [ASM6]
                isouter=True
            )
            .where(PlaceListDB.is_public == True)
            .group_by(PlaceListDB.list_id)
            .order_by(func.count(SavedListDB.saved_list_id).desc())
            .limit(limit)
        )
        return session.exec(statement).all()

@app.get("/lists/{list_id}", status_code=status.HTTP_200_OK)
def read_list(list_id: int) -> PlaceListOut:
     with Session(engine) as session:
        place_list = session.get(PlaceListDB, list_id)
        if place_list is not None:
            return place_list
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="List not found"
        )

@app.post("/lists/", status_code=status.HTTP_201_CREATED)
def create_list(place_list: PlaceList) -> PlaceListOut:
    with Session(engine) as session:
        user = session.get(UserDB, place_list.user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        new_list = PlaceListDB(**place_list.model_dump())
        session.add(new_list)
        session.commit()
        session.refresh(new_list)
        return new_list

@app.put("/lists/{list_id}", status_code=status.HTTP_200_OK)
def update_list(list_id: int, new_list: PlaceList) -> PlaceListOut:
    with Session(engine) as session:
        db_list = session.get(PlaceListDB, list_id)
        if db_list is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="List not found"
            )
        
        # User owner check (Optional, depending on your auth logic later)
        if db_list.user_id != new_list.user_id:
             raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot change the owner of the list"
            )

        db_list.list_name = new_list.list_name
        db_list.description = new_list.description
        db_list.cover_image_url = new_list.cover_image_url
        db_list.is_public = new_list.is_public
        
        session.add(db_list)
        session.commit()
        session.refresh(db_list)
        return db_list

@app.delete("/lists/{list_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_list(list_id: int):
    with Session(engine) as session:
        db_list = session.get(PlaceListDB, list_id)
        if db_list is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="List not found"
            )
            
        # 1. ลบความสัมพันธ์ (ListPlace) ออกจาก list นี้ก่อน
        for list_place in session.exec(select(ListPlaceDB).where(ListPlaceDB.list_id == list_id)).all():
            session.delete(list_place)
            
        # 2. ลบ SavedList ที่คนอื่นกดเซฟไว้
        for saved_list in session.exec(select(SavedListDB).where(SavedListDB.list_id == list_id)).all():
             session.delete(saved_list)
             
        # 3. ลบ List ตัวมันเอง
        session.delete(db_list)
        session.commit()
        return


# =========================================================
# LIST_PLACES (เพิ่มสถานที่เข้าไปใน List)
# =========================================================

@app.get("/list-places/{list_id}", status_code=status.HTTP_200_OK)
def read_places_in_list(list_id: int) -> list[ListPlaceOut]:
     with Session(engine) as session:
         statement = select(ListPlaceDB).where(ListPlaceDB.list_id == list_id).order_by(ListPlaceDB.position)
         return session.exec(statement).all()

@app.post("/list-places/", status_code=status.HTTP_201_CREATED)
def add_place_to_list(list_place: ListPlace) -> ListPlaceOut:
    with Session(engine) as session:
        db_list = session.get(PlaceListDB, list_place.list_id)
        place = session.get(PlaceDB, list_place.place_id)
        
        if db_list is None or place is None:
             raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="List or Place not found"
            )
            
        new_list_place = ListPlaceDB(**list_place.model_dump())
        session.add(new_list_place)
        
        try:
            session.commit()
            session.refresh(new_list_place)
            return ListPlaceOut(
                list_id=new_list_place.list_id,
                place_id=new_list_place.place_id,
                position=new_list_place.position,
                added_at=new_list_place.added_at
            )
        except IntegrityError:
             session.rollback()
             raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Place is already in this list"
            )

@app.delete("/list-places/{list_id}/{place_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_place_from_list(list_id: int, place_id: int):
    with Session(engine) as session:
        list_place = session.get(ListPlaceDB, (list_id, place_id))
        if list_place is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Place not found in this list"
            )
        session.delete(list_place)
        session.commit()
        return

# =========================================================
# SAVED_LISTS (User เซฟ List ของคนอื่น)
# =========================================================

@app.get("/saved-lists/", status_code=status.HTTP_200_OK)
def read_saved_lists(
    user_id: int | None = None,
    offset: int = 0,
    limit: int = 100
) -> list[SavedListOut]:
    with Session(engine) as session:
        statement = select(SavedListDB).where(SavedListDB.is_deleted == False)   # [ASM6]
        if user_id is not None:
            statement = statement.where(SavedListDB.user_id == user_id)
        statement = statement.offset(offset).limit(limit)
        return session.exec(statement).all()


@app.post("/saved-lists/", status_code=status.HTTP_201_CREATED)
def create_saved_list(saved_list: SavedList) -> SavedListOut:
    with Session(engine) as session:
        user = session.get(UserDB, saved_list.user_id)
        target_list = session.get(PlaceListDB, saved_list.list_id)
        
        if user is None or target_list is None:
             raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User or Target List not found"
            )
            
        # Optional: Prevent user from saving their own list
        if user.user_id == target_list.user_id:
             raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot save your own list"
            )
            
        # [ASM6] เคย save แล้วกดเลิก (soft delete) → กู้คืนแถวเดิม เพราะตารางห้าม user_id+list_id ซ้ำ
        existing = session.exec(
            select(SavedListDB).where(
                SavedListDB.user_id == saved_list.user_id,
                SavedListDB.list_id == saved_list.list_id
            )
        ).first()
        if existing is not None and existing.is_deleted:
            existing.is_deleted = False
            session.add(existing)
            session.commit()
            session.refresh(existing)
            return existing

        new_saved_list = SavedListDB(**saved_list.model_dump(exclude={"is_deleted"}))
        session.add(new_saved_list)
        try:
            session.commit()
            session.refresh(new_saved_list)
            return new_saved_list
        except IntegrityError:
             session.rollback()
             raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You have already saved this list"
            )

@app.delete("/saved-lists/{saved_list_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_saved_list(saved_list_id: int):
    with Session(engine) as session:
        saved_list = session.get(SavedListDB, saved_list_id)
        if saved_list is None or saved_list.is_deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Saved List record not found"
            )
        saved_list.is_deleted = True   # [ASM6] soft delete
        session.add(saved_list)
        session.commit()
        return


# [ASM6] update saved list (ใช้ทำ soft delete: ส่ง is_deleted = true)
@app.put("/saved-lists/{saved_list_id}", status_code=status.HTTP_200_OK)
def update_saved_list(saved_list_id: int, new_saved_list: SavedList) -> SavedListOut:
    with Session(engine) as session:
        saved_list = session.get(SavedListDB, saved_list_id)
        if saved_list is None or saved_list.is_deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Saved List record not found"
            )
        if new_saved_list.user_id != saved_list.user_id or new_saved_list.list_id != saved_list.list_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="user_id and list_id cannot be changed"
            )
        saved_list.is_deleted = new_saved_list.is_deleted
        session.add(saved_list)
        session.commit()
        session.refresh(saved_list)
        return saved_list