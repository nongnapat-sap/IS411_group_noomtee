from fastapi import FastAPI, HTTPException, status
from sqlmodel import Session, select

from database import engine, init_db
from models import (
    AreaDB, Area, AreaOut,
    PlaceDB, Place, PlaceOut,
    UserDB, User, UserOut,
    VibeDB, Vibe, VibeOut,
    JournalDB, Journal, JournalOut
)


init_db()
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
# PLACE
# =========================================================

@app.get("/places/", status_code=status.HTTP_200_OK)
def read_places() -> list[PlaceOut]:
    with Session(engine) as session:
        return session.exec(select(PlaceDB)).all()


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

        area = session.get(AreaDB, new_place.area_id)

        if area is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Area not found"
            )

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
            user.created_at = new_user.created_at
            user.updated_at = new_user.updated_at

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
# JOURNAL
# =========================================================

@app.get("/journals/", status_code=status.HTTP_200_OK)
def read_journals() -> list[JournalOut]:
    with Session(engine) as session:
        return session.exec(select(JournalDB)).all()


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
        journal.updated_at = new_journal.updated_at

        session.add(journal)
        session.commit()
        session.refresh(journal)
        return journal