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
    PlaceVibe, PlaceVibeOut, PlaceVibeDB
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
                UserDB(name="Timothee Chalamet", email="timothee.chalamet@example.com", password_hash="hashed_pw_004", profile_image_url="https://i.pravatar.cc/300?img=4", nationality="French", preferred_language="French"),
                UserDB(name="Sydney Sweeney", email="sydney.sweeney@example.com", password_hash="hashed_pw_005", profile_image_url="https://i.pravatar.cc/300?img=5", nationality="American", preferred_language="English"),
                UserDB(name="Anya Taylor-Joy", email="anya.taylorjoy@example.com", password_hash="hashed_pw_006", profile_image_url="https://i.pravatar.cc/300?img=6", nationality="British", preferred_language="English"),
                UserDB(name="Austin Butler", email="austin.butler@example.com", password_hash="hashed_pw_007", profile_image_url="https://i.pravatar.cc/300?img=7", nationality="American", preferred_language="English"),
                UserDB(name="Hoyeon Jung", email="hoyeon.jung@example.com", password_hash="hashed_pw_008", profile_image_url="https://i.pravatar.cc/300?img=8", nationality="Korean", preferred_language="Korean"),
                UserDB(name="Barry Keoghan", email="barry.keoghan@example.com", password_hash="hashed_pw_009", profile_image_url="https://i.pravatar.cc/300?img=9", nationality="Irish", preferred_language="English"),
                UserDB(name="Rosalia Vila", email="rosalia.vila@example.com", password_hash="hashed_pw_010", profile_image_url="https://i.pravatar.cc/300?img=11", nationality="Spanish", preferred_language="Spanish"),
                UserDB(name="Jung Ho-yeon", email="jung.hoyeon2@example.com", password_hash="hashed_pw_011", profile_image_url="https://i.pravatar.cc/300?img=12", nationality="Korean", preferred_language="English"),
                UserDB(name="Charles Melton", email="charles.melton@example.com", password_hash="hashed_pw_012", profile_image_url="https://i.pravatar.cc/300?img=13", nationality="American", preferred_language="English"),
                UserDB(name="Greta Lee", email="greta.lee@example.com", password_hash="hashed_pw_013", profile_image_url="https://i.pravatar.cc/300?img=14", nationality="Korean-American", preferred_language="English"),
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


init_db()
# Insert initial data
seed_data()
app = FastAPI()


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
        session.commit()
        session.refresh(new_user)
        return new_user


@app.put("/users/{user_id}", status_code=status.HTTP_200_OK)
def update_user(user_id: int, new_user: User) -> UserOut:
    with Session(engine) as session:
        user = session.get(UserDB, user_id)
        if user is not None:
            user.name = new_user.name
            user.email = new_user.email
            user.password_hash = new_user.password_hash
            user.profile_image_url = new_user.profile_image_url
            user.nationality = new_user.nationality
            user.preferred_language = new_user.preferred_language
            user.updated_at = datetime.utcnow()
            session.add(user)
            session.commit()
            session.refresh(user)
            return user

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found"
    )


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
        statement = select(JournalDB)
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
        if journal is not None:
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
        if journal is None:
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
        journal.created_at = new_journal.created_at
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
        if journal is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Journal not found"
            )
        session.delete(journal)
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
        statement = select(FavoriteDB)
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
        if favorite is not None:
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
        new_favorite = FavoriteDB(**favorite.model_dump())
        session.add(new_favorite)

        session.commit()
        session.refresh(new_favorite)
        return new_favorite


@app.delete("/favorites/{favorite_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_favorite(favorite_id: int):
    with Session(engine) as session:
        favorite = session.get(FavoriteDB, favorite_id)
        if favorite is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Favorite not found"
            )
        session.delete(favorite)
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