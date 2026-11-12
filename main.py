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


# =========================================================
# [FINAL] ข้อมูลตัวอย่างชุดใหญ่ (ใช้เมื่อ database ยังว่าง)
# ถ้าแก้ข้อมูลในนี้ ต้องลบ database.db แล้วรัน uvicorn ใหม่ ข้อมูลถึงจะเปลี่ยน
# รูปทั้งหมดเป็นลิงก์จาก Unsplash ถ้ารูปไหนโหลดไม่ได้ หน้าเว็บจะแสดงพื้นสีแทนให้อัตโนมัติ
# =========================================================
def img(photo_id):
    return f"https://images.unsplash.com/{photo_id}?auto=format&fit=crop&w=900&q=70"

IMG = {
    "jazz": img("photo-1511192336575-5a79af67a629"),
    "concert": img("photo-1501386761578-eac5c94b800a"),
    "stage": img("photo-1493225457124-a3eb161ffa5f"),
    "crowd": img("photo-1429962714451-bb934ecdc4ec"),
    "club": img("photo-1492684223066-81342ee5ff30"),
    "club2": img("photo-1516450360452-9312f5e86fc7"),
    "speakeasy": img("photo-1514933651103-005eec06c04b"),
    "bar": img("photo-1470337458703-46ad1756a187"),
    "cocktail": img("photo-1514362545857-3bc16c4c7d1b"),
    "cocktail2": img("photo-1551024709-8f23befc6f87"),
    "bar2": img("photo-1566417713940-fe7c737a9ef2"),
    "beer": img("photo-1575037614876-c38a4d44f5b8"),
    "beer2": img("photo-1543007630-9710e4a00a20"),
    "beer3": img("photo-1535958636474-b021ee887b13"),
    "rooftop": img("photo-1519671482749-fd09be7ccebf"),
    "skyline": img("photo-1477959858617-67f85cf4f1df"),
    "skyline2": img("photo-1519501025264-65ba15a82390"),
    "citynight": img("photo-1514565131-fce0801e5785"),
    "citynight2": img("photo-1480714378408-67cf0d13bc1b"),
    "streetfood": img("photo-1555939594-58d7cb561ad1"),
    "food": img("photo-1504674900247-0877df9cc836"),
    "noodles": img("photo-1559314809-0d155014e29e"),
    "food2": img("photo-1567620905732-2d1ec7ab7445"),
    "restaurant": img("photo-1555396273-367ea4eb4db5"),
    "restaurant2": img("photo-1517248135467-4c7edcad34c4"),
    "restaurant3": img("photo-1559339352-11d035aa65de"),
    "cafe": img("photo-1554118811-1e0d58224f24"),
    "cafe2": img("photo-1501339847302-ac426a4a7cbb"),
    "coffee": img("photo-1495474472287-4d71bcdd2085"),
    "bangkok": img("photo-1508009603885-50cf7c579365"),
    "bangkok2": img("photo-1563492065599-3520f775eeed"),
    "temple": img("photo-1528181304800-259b08848526"),
}


def seed_data():
    with Session(engine) as session:
        # มีข้อมูลอยู่แล้ว → ไม่ต้อง seed ซ้ำ
        if session.exec(select(AreaDB)).first() is not None:
            return

        # ---------------- AREAS (10) ----------------
        areas = [
            AreaDB(area_name="Ratchathewi", district="Ratchathewi", sub_district="Thanon Phaya Thai", latitude=13.7563, longitude=100.5330, description="Victory Monument, classic live-music pubs and cheap late-night noodles", cover_image_url=IMG["concert"]),
            AreaDB(area_name="Sukhumvit", district="Watthana", sub_district="Khlong Toei Nuea", latitude=13.7400, longitude=100.5600, description="Bangkok's nightlife spine: speakeasies, clubs and street-side noodle lanes", cover_image_url=IMG["citynight"]),
            AreaDB(area_name="Thonglor", district="Watthana", sub_district="Khlong Tan Nuea", latitude=13.7300, longitude=100.5800, description="Trendy cocktail bars, vinyl rooms and craft-beer taprooms", cover_image_url=IMG["bar"]),
            AreaDB(area_name="Ari", district="Phaya Thai", sub_district="Sam Sen Nai", latitude=13.7797, longitude=100.5445, description="Leafy cafe neighbourhood with relaxed garden bars", cover_image_url=IMG["cafe"]),
            AreaDB(area_name="Ekkamai", district="Watthana", sub_district="Khlong Tan Nuea", latitude=13.7195, longitude=100.5850, description="Basement clubs, rooftops and food stalls open until sunrise", cover_image_url=IMG["club2"]),
            AreaDB(area_name="Silom", district="Bang Rak", sub_district="Silom", latitude=13.7248, longitude=100.5340, description="Business district by day, sky lounges and night markets after dark", cover_image_url=IMG["skyline2"]),
            AreaDB(area_name="Sathorn", district="Sathon", sub_district="Thung Wat Don", latitude=13.7180, longitude=100.5290, description="Garden bistros and rooftop bars with river views", cover_image_url=IMG["rooftop"]),
            AreaDB(area_name="Chinatown", district="Samphanthawong", sub_district="Chakkrawat", latitude=13.7398, longitude=100.5088, description="Yaowarat's neon signs, seafood stalls and hidden gin bars", cover_image_url=IMG["streetfood"]),
            AreaDB(area_name="Riverside", district="Bang Rak", sub_district="Si Phraya", latitude=13.7290, longitude=100.5130, description="Chao Phraya piers, jazz boats and old warehouse cafes", cover_image_url=IMG["bangkok2"]),
            AreaDB(area_name="Old Town", district="Phra Nakhon", sub_district="Chana Songkhram", latitude=13.7590, longitude=100.4960, description="Temple-view terraces, Phra Athit live houses and Khao San late kitchens", cover_image_url=IMG["temple"]),
        ]
        session.add_all(areas)
        session.commit()

        # ---------------- PLACES (30) ----------------
        def place(name, desc, area_id, address, price, open_t, close_t, image_key, lat, lng):
            return PlaceDB(place_name=name, description=desc, area_id=area_id, address=address,
                           latitude=lat, longitude=lng, price_level=price, opening_time=open_t,
                           closing_time=close_t, booking_link=None, image_url=IMG[image_key])

        places = [
            place("Saxophone Pub & Restaurant", "A legendary live jazz venue with a band every night", 1, "3/8 Soi Ratchawithi 11, Ratchathewi", "200-1000 THB", "18:00", "02:00", "jazz", 13.7650, 100.5375),
            place("Havana Social", "A hidden 1940s Cuban-themed speakeasy behind a phone booth", 2, "341 Sukhumvit Soi 11, Watthana", "400-1200 THB", "18:00", "02:00", "speakeasy", 13.7430, 100.5560),
            place("Upper House", "A high-energy nightclub with big-name DJs", 2, "88 Sukhumvit Soi 24, Khlong Toei", "400-1200 THB", "21:00", "03:30", "club", 13.7280, 100.5680),
            place("Coco Walk", "Open-air strip of small bars with live acoustic bands", 1, "Phaya Thai Rd, Ratchathewi", "200-800 THB", "17:00", "01:00", "stage", 13.7505, 100.5315),
            place("Ari Beer Garden", "Outdoor craft-beer taproom with acoustic sets on weekends", 4, "Soi Ari 4, Phaya Thai", "150-500 THB", "17:00", "00:00", "beer", 13.7800, 100.5440),
            place("Ekkamai Rooftop", "Open-air rooftop with a wide city skyline view", 5, "Soi Ekkamai 10, Watthana", "300-900 THB", "18:00", "01:00", "skyline", 13.7200, 100.5855),
            place("Ekkamai Late Bites", "Street food stalls that stay open until sunrise", 5, "Soi Ekkamai 4, Watthana", "80-300 THB", "20:00", "06:00", "streetfood", 13.7190, 100.5845),
            place("Silom Soi Speakeasy", "Unmarked cocktail bar in a narrow alley — knock twice", 6, "Silom Soi 4, Bang Rak", "350-1000 THB", "19:00", "02:00", "cocktail", 13.7250, 100.5335),
            place("Sky High Sathorn", "Rooftop bar with panoramic Chao Phraya views", 7, "Sathorn Rd, Sathon", "500-1500 THB", "17:30", "01:00", "rooftop", 13.7185, 100.5285),
            place("Chinatown Neon Bar", "Retro neon-lit bar serving Thai-Chinese fusion cocktails", 8, "Yaowarat Rd, Samphanthawong", "250-700 THB", "18:00", "01:00", "bar2", 13.7400, 100.5090),
            place("Thonglor Vinyl Room", "Record bar where DJs play only vinyl", 3, "Thonglor Soi 10, Watthana", "300-900 THB", "19:00", "02:00", "bar", 13.7320, 100.5820),
            place("Taproom 55", "Twenty Thai craft beers on tap and a small kitchen", 3, "Sukhumvit Soi 55, Watthana", "200-600 THB", "16:00", "00:00", "beer3", 13.7300, 100.5790),
            place("Victory Boat Noodles", "Tiny bowls of rich boat noodles, stacked by the dozen", 1, "Victory Monument, Ratchathewi", "50-150 THB", "10:00", "23:00", "noodles", 13.7650, 100.5380),
            place("Ari Slow Bar Cafe", "Coffee by day, natural wine by night", 4, "Soi Ari 1, Phaya Thai", "120-400 THB", "08:00", "22:00", "cafe", 13.7790, 100.5450),
            place("Ari Garden Jazz", "Garden bar with a small jazz trio under string lights", 4, "Soi Ari 5, Phaya Thai", "200-700 THB", "18:00", "00:00", "concert", 13.7810, 100.5430),
            place("Ekkamai Basement Club", "Underground techno club with a heavy sound system", 5, "Ekkamai Rd, Watthana", "400-1200 THB", "22:00", "04:00", "club2", 13.7210, 100.5860),
            place("Silom Soi 2 Dance Hall", "Colourful dance club with pop and house nights", 6, "Silom Soi 2, Bang Rak", "300-900 THB", "22:00", "04:00", "crowd", 13.7290, 100.5340),
            place("Patpong Night Eats", "Night-market grills and noodles next to Patpong", 6, "Patpong Rd, Bang Rak", "60-250 THB", "18:00", "03:00", "food", 13.7280, 100.5330),
            place("Sathorn Garden Bistro", "Leafy bistro for long dinners and wine", 7, "Soi Sathorn 12, Sathon", "400-1200 THB", "11:00", "23:00", "restaurant", 13.7210, 100.5280),
            place("Yaowarat Seafood Stalls", "Grilled prawns and crab curry right on the street", 8, "Yaowarat Rd Soi 11, Samphanthawong", "100-500 THB", "17:00", "01:00", "streetfood", 13.7410, 100.5100),
            place("Nana Lane Gin Bar", "Shophouse gin bar hidden in an old Chinatown lane", 8, "Soi Nana, Pom Prap", "300-800 THB", "19:00", "01:00", "cocktail2", 13.7390, 100.5110),
            place("Riverside Jazz Boat", "Dinner cruise with live jazz on the Chao Phraya", 9, "Si Phraya Pier, Bang Rak", "600-1800 THB", "19:00", "23:00", "bangkok2", 13.7300, 100.5140),
            place("Riverfront Terrace", "Old warehouse terrace with drinks by the water", 9, "Charoen Krung Rd, Bang Rak", "300-1000 THB", "16:00", "00:00", "citynight2", 13.7280, 100.5120),
            place("Charoen Krung Coffee House", "Old-town cafe in a 100-year-old shophouse", 9, "Charoen Krung Soi 32, Bang Rak", "100-350 THB", "08:00", "18:00", "coffee", 13.7270, 100.5150),
            place("Phra Athit Live House", "Small live house with Thai indie bands", 10, "Phra Athit Rd, Phra Nakhon", "150-500 THB", "19:00", "01:00", "stage", 13.7620, 100.4950),
            place("Khao San Late Kitchen", "Pad thai and fried rice until the bars close", 10, "Khao San Rd, Phra Nakhon", "60-200 THB", "18:00", "04:00", "food2", 13.7590, 100.4970),
            place("Old Town Temple Terrace", "Rooftop terrace facing the temples at sunset", 10, "Maha Rat Rd, Phra Nakhon", "350-1000 THB", "17:00", "00:00", "temple", 13.7470, 100.4920),
            place("Sukhumvit 38 Noodle Lane", "Late-night noodle and mango sticky rice lane", 2, "Sukhumvit Soi 38, Khlong Toei", "50-200 THB", "17:00", "02:00", "noodles", 13.7210, 100.5790),
            place("Retro Arcade Bar", "Cocktails, old arcade machines and 80s music", 1, "Soi Rang Nam, Ratchathewi", "200-600 THB", "18:00", "02:00", "bar2", 13.7600, 100.5360),
            place("Silom Sky Lounge", "Glass-walled lounge on the 50th floor", 6, "Silom Rd, Bang Rak", "500-1600 THB", "17:00", "01:00", "skyline2", 13.7260, 100.5300),
        ]
        session.add_all(places)
        session.commit()

        # นับจำนวนสถานที่ในแต่ละย่านให้ตรงกับข้อมูลจริง
        for area in session.exec(select(AreaDB)).all():
            area.total_places = len(session.exec(select(PlaceDB).where(PlaceDB.area_id == area.area_id)).all())
            session.add(area)
        session.commit()

        # ---------------- VIBES (9) ----------------
        vibes = [
            VibeDB(vibe_name="High Energy & Clubbing", description="Loud beats, DJ sets, dancing and late-night party vibes"),
            VibeDB(vibe_name="Rooftop & Skyline", description="Open-air views of the Bangkok skyline and riverfront"),
            VibeDB(vibe_name="Craft Beer & Taproom", description="Artisan beers on tap and relaxed beer gardens"),
            VibeDB(vibe_name="Street Food & Late Bites", description="Late-night hunger cures and affordable street stalls"),
            VibeDB(vibe_name="Retro & Neon", description="Nostalgic design, neon lights and old-school music"),
            VibeDB(vibe_name="Waterfront & Chill", description="Breezy riverside places for calm drinks and conversations"),
            VibeDB(vibe_name="Live Music & Jazz", description="Live bands, jazz trios and indie gigs"),
            VibeDB(vibe_name="Hidden Speakeasy", description="Unmarked doors, secret entrances and serious cocktails"),
            VibeDB(vibe_name="Cafe & Daytime", description="Coffee, brunch and slow afternoons"),
        ]
        session.add_all(vibes)
        session.commit()

        # place_id → vibe_id (ตามลำดับสถานที่ด้านบน 1–30)
        place_vibe_pairs = {
            1: [7], 2: [8, 5], 3: [1], 4: [7, 4], 5: [3], 6: [2], 7: [4], 8: [8], 9: [2, 6], 10: [5],
            11: [7, 5], 12: [3], 13: [4], 14: [9], 15: [7, 6], 16: [1], 17: [1, 5], 18: [4], 19: [6, 9], 20: [4],
            21: [8, 5], 22: [6, 7], 23: [6, 2], 24: [9], 25: [7], 26: [4, 1], 27: [2, 6], 28: [4], 29: [5, 1], 30: [2],
        }
        session.add_all([PlaceVibeDB(place_id=p, vibe_id=v) for p, vs in place_vibe_pairs.items() for v in vs])
        session.commit()

        # ---------------- USERS (10) ----------------
        def user(username, name, number, nationality, language, bio):
            return UserDB(username=username, name=name, email=f"{username}@example.com", password_hash=f"hashed_pw_{number:03d}",
                          bio=bio, profile_image_url=f"https://i.pravatar.cc/300?img={number}", nationality=nationality, preferred_language=language)

        users = [
            user("timothee_c", "Timothee Chalamet", 4, "French", "French", "Rooftops and craft beer, always."),
            user("sydney_s", "Sydney Sweeney", 5, "American", "English", "Jazz bars and late dinners."),
            user("anya_tj", "Anya Taylor-Joy", 6, "British", "English", "Will cross the city for good noodles."),
            user("austin_b", "Austin Butler", 7, "American", "English", "Live music first, everything else second."),
            user("hoyeon_j", "Hoyeon Jung", 8, "Korean", "Korean", "Collecting secret spots."),
            user("barry_k", "Barry Keoghan", 9, "Irish", "English", "Neon, vinyl and anything retro."),
            user("rosalia_v", "Rosalia Vila", 11, "Spanish", "Spanish", "Cafe hopper by day."),
            user("jung_hy", "Jung Ho-yeon", 12, "Korean", "English", "Chinatown regular."),
            user("charles_m", "Charles Melton", 13, "American", "English", "Dance floors until sunrise."),
            user("greta_l", "Greta Lee", 14, "Korean-American", "English", "Riverside evenings and slow drinks."),
        ]
        session.add_all(users)
        session.commit()

        # ---------------- JOURNALS (34) ----------------
        def journal(user_id, place_id, title, rating, note, y, m, d, h=21):
            return JournalDB(user_id=user_id, place_id=place_id, title=title, rating=rating, note=note,
                             visited_at=datetime(y, m, d, h, 0), image_url=None, is_public=True)

        journals = [
            # user 4 (Austin Butler) = ผู้ใช้ที่ล็อกอินอยู่ในหน้าเว็บ
            journal(4, 1, "Acoustic & Soulful Jazz Night", 5, "The live saxophone solo was breathtaking. Truly an iconic music haven.", 2026, 9, 1),
            journal(4, 6, "Golden hour on the roof", 4, "Great skyline at sunset. Go before 7 pm to get a seat at the edge.", 2026, 9, 12, 18),
            journal(4, 22, "Jazz on the river", 5, "Dinner was fine, the band and the view were the real stars.", 2026, 10, 3, 20),
            journal(4, 14, "Sunday slow coffee", 4, "Quiet corner seat, great oat latte, natural wine list for later.", 2026, 10, 19, 11),
            journal(4, 25, "Thai indie gig", 4, "Tiny room, loud band, very friendly crowd.", 2026, 11, 2, 22),
            # คนอื่น
            journal(5, 2, "Secret phone booth", 5, "Dialing the hidden code to get in is half the fun. Great rum cocktails.", 2026, 9, 2, 22),
            journal(6, 3, "Big Saturday night", 4, "Packed and loud, amazing light show.", 2026, 9, 4, 23),
            journal(7, 5, "Beer under fairy lights", 4, "Super chilled vibe. Try the local IPA.", 2026, 9, 5, 19),
            journal(8, 6, "Sunset cocktails", 5, "Best panorama of Bangkok at golden hour.", 2026, 9, 6, 18),
            journal(1, 9, "River views from above", 5, "Worth the price for the view alone.", 2026, 9, 8, 19),
            journal(2, 1, "First time at Saxophone", 5, "The house band is incredible. Arrive early for a table.", 2026, 9, 9),
            journal(3, 7, "4am noodles", 4, "Exactly what you need after a night out.", 2026, 9, 10, 4),
            journal(9, 16, "Techno till morning", 5, "Sound system is unreal. Best club in Ekkamai.", 2026, 9, 13, 1),
            journal(10, 22, "Calm evening cruise", 4, "Slow, romantic, and the jazz was lovely.", 2026, 9, 14, 20),
            journal(6, 10, "Neon and gin", 4, "Feels like a Wong Kar-wai film.", 2026, 9, 15, 22),
            journal(8, 20, "Crab curry heaven", 5, "Messy, spicy and perfect. Bring cash.", 2026, 9, 16, 20),
            journal(5, 8, "Knock twice", 4, "Small and cosy, bartender made me a custom drink.", 2026, 9, 18, 22),
            journal(1, 12, "Craft beer flight", 4, "Twenty taps, all Thai. The mango sour was great.", 2026, 9, 20, 18),
            journal(7, 14, "Morning flat white", 5, "My favourite cafe in Ari.", 2026, 9, 21, 9),
            journal(2, 15, "Jazz trio in the garden", 4, "Relaxed and pretty, great for a first date.", 2026, 9, 23, 20),
            journal(3, 18, "Night market grill", 4, "Pork skewers and sticky rice for under 100 baht.", 2026, 9, 25, 23),
            journal(9, 17, "Pop night", 4, "Fun crowd, dance-floor energy all night.", 2026, 9, 27, 0),
            journal(10, 23, "Warehouse sunset", 5, "Best spot on the river for a quiet drink.", 2026, 9, 28, 18),
            journal(6, 11, "All-vinyl Friday", 5, "DJ played a whole Thai funk set. Loved it.", 2026, 10, 1, 22),
            journal(8, 21, "Shophouse gin", 4, "Hidden down a lane, worth the search.", 2026, 10, 4, 21),
            journal(1, 27, "Temples at sunset", 5, "The view of the temples lighting up is magic.", 2026, 10, 6, 18),
            journal(3, 26, "Khao San pad thai", 3, "Tourist prices but tasty after midnight.", 2026, 10, 8, 2),
            journal(7, 24, "Old shophouse cafe", 4, "Beautiful old building, good pastries.", 2026, 10, 10, 10),
            journal(5, 13, "Boat noodle stack", 4, "Ate twelve bowls. No regrets.", 2026, 10, 12, 13),
            journal(9, 29, "Arcade and cocktails", 4, "Played Street Fighter with a margarita in hand.", 2026, 10, 15, 21),
            journal(2, 19, "Long dinner in the garden", 4, "Lovely wine list, slow and quiet.", 2026, 10, 18, 20),
            journal(10, 30, "Fifty floors up", 5, "Glass walls, city lights everywhere.", 2026, 10, 22, 21),
            journal(4, 8, "Late visit (private note)", 3, "Too crowded tonight. Will come back on a weekday.", 2026, 11, 5, 23),
            journal(6, 4, "Acoustic night", 4, "Cheap drinks and a good cover band.", 2026, 11, 7, 21),
        ]
        journals[-2].is_public = False   # journal ส่วนตัว: ไม่แสดงในหน้ารายละเอียดสถานที่
        session.add_all(journals)
        session.commit()

        # ---------------- FAVORITES (30) ----------------
        favorite_pairs = [
            (4, 1), (4, 6), (4, 8), (4, 22), (4, 14),
            (1, 9), (1, 12), (1, 27), (2, 1), (2, 15), (2, 19), (3, 7), (3, 18), (3, 13),
            (5, 2), (5, 8), (5, 21), (6, 10), (6, 11), (6, 29), (7, 14), (7, 24), (7, 5),
            (8, 20), (8, 21), (9, 16), (9, 17), (10, 22), (10, 23), (10, 30),
        ]
        session.add_all([FavoriteDB(user_id=u, place_id=p) for u, p in favorite_pairs])
        session.commit()

        # ---------------- FOLLOWS (25) ----------------
        follow_pairs = [
            (4, 1), (4, 2), (4, 6), (4, 10),            # Austin ติดตาม 4 คน
            (2, 4), (3, 4), (5, 4), (7, 4), (9, 4),     # 5 คนติดตาม Austin
            (1, 2), (1, 3), (2, 1), (3, 1), (5, 6), (6, 7), (7, 8), (8, 9), (9, 10),
            (10, 1), (6, 2), (8, 3), (10, 7), (3, 5), (1, 10), (2, 10),
        ]
        session.add_all([FollowDB(follower_id=a, following_id=b) for a, b in follow_pairs])
        session.commit()

        # ---------------- COLLECTIONS = ตาราง lists (12) ----------------
        lists = [
            PlaceListDB(user_id=1, list_name="Ultimate Bangkok Rooftops", description="Best views in the city, from sunset to midnight", cover_image_url=IMG["rooftop"], is_public=True),
            PlaceListDB(user_id=2, list_name="Jazz & Chill Night", description="Top live-music spots for a slow evening", cover_image_url=IMG["jazz"], is_public=True),
            PlaceListDB(user_id=3, list_name="Late Night Eats", description="Where to eat after the bars close", cover_image_url=IMG["streetfood"], is_public=True),
            PlaceListDB(user_id=4, list_name="Speakeasy Hunt", description="Hidden bars and secret doors", cover_image_url=IMG["speakeasy"], is_public=True),
            PlaceListDB(user_id=4, list_name="Date Night Shortlist", description="Dim lights, good food, great views", cover_image_url=IMG["restaurant"], is_public=True),
            PlaceListDB(user_id=1, list_name="Craft Beer Crawl", description="Taprooms and beer gardens for one long night", cover_image_url=IMG["beer2"], is_public=True),
            PlaceListDB(user_id=6, list_name="Neon & Retro Bangkok", description="Vinyl, arcades and neon-lit bars", cover_image_url=IMG["bar2"], is_public=True),
            PlaceListDB(user_id=10, list_name="Riverside Evenings", description="Slow drinks by the Chao Phraya", cover_image_url=IMG["bangkok2"], is_public=True),
            PlaceListDB(user_id=7, list_name="Cafe Hopping", description="Coffee and slow afternoons around the city", cover_image_url=IMG["cafe2"], is_public=True),
            PlaceListDB(user_id=9, list_name="Dance Till Sunrise", description="Clubs for when you don't want the night to end", cover_image_url=IMG["club"], is_public=True),
            PlaceListDB(user_id=5, list_name="My Secret Spots", description="Private list only for me", cover_image_url=IMG["food"], is_public=False),
            PlaceListDB(user_id=4, list_name="Next Weekend Ideas", description="Places to try soon", cover_image_url=IMG["temple"], is_public=False),
        ]
        session.add_all(lists)
        session.commit()

        # list_id → place_id ตามลำดับที่แสดง
        list_place_map = {
            1: [6, 9, 23, 27, 30], 2: [1, 15, 22, 25, 11], 3: [7, 18, 20, 26, 28, 13], 4: [2, 8, 21, 10],
            5: [9, 19, 22, 23], 6: [5, 12, 15], 7: [10, 29, 11, 21, 17], 8: [22, 23, 24, 9],
            9: [14, 24, 19], 10: [3, 16, 17, 26], 11: [13, 20], 12: [25, 27, 12],
        }
        session.add_all([
            ListPlaceDB(list_id=l, place_id=p, position=i + 1)
            for l, ps in list_place_map.items() for i, p in enumerate(ps)
        ])
        session.commit()

        # ---------------- SAVED COLLECTIONS = ตาราง saved_lists (27) ----------------
        saved_pairs = [
            (4, 1), (4, 2), (4, 7),                     # Austin save ไว้ 3 อัน
            (2, 1), (5, 1), (7, 1), (10, 1),
            (1, 2), (6, 2), (9, 2),
            (1, 3), (5, 3), (8, 3),
            (3, 4), (7, 4),
            (9, 5), (6, 5),
            (10, 6), (8, 6),
            (3, 7),
            (6, 8), (3, 8), (9, 8),
            (2, 9),
            (1, 10), (8, 10), (7, 10),
        ]
        session.add_all([SavedListDB(user_id=u, list_id=l) for u, l in saved_pairs])
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
        statement = select(UserDB).join(FollowDB, FollowDB.follower_id == UserDB.user_id).where(FollowDB.following_id == user_id, FollowDB.is_deleted == False)   # [FINAL]
        return session.exec(statement).all()

@app.get("/users/{user_id}/following", status_code=status.HTTP_200_OK)
def read_user_following(user_id: int) -> list[UserOut]:
    with Session(engine) as session:
        statement = select(UserDB).join(FollowDB, FollowDB.following_id == UserDB.user_id).where(FollowDB.follower_id == user_id, FollowDB.is_deleted == False)   # [FINAL]
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
        statement = select(FollowDB).where(FollowDB.is_deleted == False)   # [FINAL] ซ่อนที่ unfollow แล้ว
        if follower_id is not None:
            statement = statement.where(FollowDB.follower_id == follower_id)
        if following_id is not None:
            statement = statement.where(FollowDB.following_id == following_id)
        statement = statement.offset(offset).limit(limit)
        return session.exec(statement).all()


@app.get("/follows/{follow_id}", status_code=status.HTTP_200_OK)
def read_follow(follow_id: int) -> FollowOut:
    with Session(engine) as session:
        follow = session.get(FollowDB, follow_id)
        if follow is not None and not follow.is_deleted:
            return follow
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Follow relationship not found"
    )


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
        # [FINAL] ตารางห้ามซ้ำ (follower_id + following_id) → ถ้าเคย unfollow ให้กู้คืนแถวเดิม
        existing = session.exec(
            select(FollowDB).where(
                FollowDB.follower_id == follow.follower_id,
                FollowDB.following_id == follow.following_id
            )
        ).first()
        if existing is not None and not existing.is_deleted:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You are already following this user"
            )
        if existing is not None:
            existing.is_deleted = False
            session.add(existing)
            session.commit()
            session.refresh(existing)
            return existing

        new_follow = FollowDB(**follow.model_dump(exclude={"is_deleted"}))
        session.add(new_follow)
        session.commit()
        session.refresh(new_follow)
        return new_follow


# [FINAL] update follow (ใช้ทำ soft delete = unfollow: ส่ง is_deleted = true)
@app.put("/follows/{follow_id}", status_code=status.HTTP_200_OK)
def update_follow(follow_id: int, new_follow: Follow) -> FollowOut:
    with Session(engine) as session:
        follow = session.get(FollowDB, follow_id)
        if follow is None or follow.is_deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Follow relationship not found"
            )
        if new_follow.follower_id != follow.follower_id or new_follow.following_id != follow.following_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="follower_id and following_id cannot be changed"
            )
        follow.is_deleted = new_follow.is_deleted
        session.add(follow)
        session.commit()
        session.refresh(follow)
        return follow


@app.delete("/follows/{follow_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_follow(follow_id: int):
    with Session(engine) as session:
        follow = session.get(FollowDB, follow_id)
        if follow is None or follow.is_deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Follow relationship not found"
            )
        follow.is_deleted = True   # [FINAL] soft delete
        session.add(follow)
        session.commit()
        return

# =========================================================
# LISTS (บนหน้าเว็บเรียกว่า Collections)
# =========================================================
@app.get("/lists/", status_code=status.HTTP_200_OK)
def read_lists(
    user_id: int | None = None,
    is_public: bool | None = None,
    offset: int = 0,
    limit: int = 100
) -> list[PlaceListOut]:
    with Session(engine) as session:
        statement = select(PlaceListDB).where(PlaceListDB.is_deleted == False)   # [FINAL]
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
                (SavedListDB.list_id == PlaceListDB.list_id) & (SavedListDB.is_deleted == False),
                isouter=True
            )
            .where(PlaceListDB.is_public == True, PlaceListDB.is_deleted == False)   # [FINAL]
            .group_by(PlaceListDB.list_id)
            .order_by(func.count(SavedListDB.saved_list_id).desc())
            .limit(limit)
        )
        return session.exec(statement).all()

@app.get("/lists/{list_id}", status_code=status.HTTP_200_OK)
def read_list(list_id: int) -> PlaceListOut:
    with Session(engine) as session:
        place_list = session.get(PlaceListDB, list_id)
        if place_list is not None and not place_list.is_deleted:   # [FINAL]
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
        new_list = PlaceListDB(**place_list.model_dump(exclude={"is_deleted"}))
        session.add(new_list)
        session.commit()
        session.refresh(new_list)
        return new_list

@app.put("/lists/{list_id}", status_code=status.HTTP_200_OK)
def update_list(list_id: int, new_list: PlaceList) -> PlaceListOut:
    with Session(engine) as session:
        db_list = session.get(PlaceListDB, list_id)
        if db_list is None or db_list.is_deleted:   # [FINAL] แก้ list ที่ลบแล้วไม่ได้
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="List not found"
            )
        if db_list.user_id != new_list.user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot change the owner of the list"
            )
        db_list.list_name = new_list.list_name
        db_list.description = new_list.description
        db_list.cover_image_url = new_list.cover_image_url
        db_list.is_public = new_list.is_public
        db_list.is_deleted = new_list.is_deleted   # [FINAL] ให้ PUT ใช้ทำ soft delete ได้
        session.add(db_list)
        session.commit()
        session.refresh(db_list)
        return db_list

@app.delete("/lists/{list_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_list(list_id: int):
    with Session(engine) as session:
        db_list = session.get(PlaceListDB, list_id)
        if db_list is None or db_list.is_deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="List not found"
            )
        db_list.is_deleted = True   # [FINAL] soft delete: ไม่ลบแถวจริง
        session.add(db_list)
        session.commit()
        return


# =========================================================
# LIST_PLACES (สถานที่ใน Collection)
# =========================================================

@app.get("/list-places/{list_id}", status_code=status.HTTP_200_OK)
def read_places_in_list(list_id: int) -> list[ListPlaceOut]:
    with Session(engine) as session:
        statement = (
            select(ListPlaceDB)
            .where(ListPlaceDB.list_id == list_id, ListPlaceDB.is_deleted == False)   # [FINAL]
            .order_by(ListPlaceDB.position)
        )
        return session.exec(statement).all()

@app.post("/list-places/", status_code=status.HTTP_201_CREATED)
def add_place_to_list(list_place: ListPlace) -> ListPlaceOut:
    with Session(engine) as session:
        db_list = session.get(PlaceListDB, list_place.list_id)
        place = session.get(PlaceDB, list_place.place_id)
        if db_list is None or db_list.is_deleted or place is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="List or Place not found"
            )
        # [FINAL] primary key คือ (list_id, place_id) → ถ้าเคยเอาออกแล้วให้กู้คืนแถวเดิม
        existing = session.get(ListPlaceDB, (list_place.list_id, list_place.place_id))
        if existing is not None and not existing.is_deleted:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Place is already in this list"
            )
        if existing is not None:
            existing.is_deleted = False
            existing.position = list_place.position
            session.add(existing)
            session.commit()
            session.refresh(existing)
            return existing

        new_list_place = ListPlaceDB(**list_place.model_dump(exclude={"is_deleted"}))
        session.add(new_list_place)
        session.commit()
        session.refresh(new_list_place)
        return new_list_place

# [FINAL] update list-place (ใช้ทำ soft delete = เอาสถานที่ออกจาก collection)
@app.put("/list-places/{list_id}/{place_id}", status_code=status.HTTP_200_OK)
def update_place_in_list(list_id: int, place_id: int, new_list_place: ListPlace) -> ListPlaceOut:
    with Session(engine) as session:
        list_place = session.get(ListPlaceDB, (list_id, place_id))
        if list_place is None or list_place.is_deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Place not found in this list"
            )
        if new_list_place.list_id != list_id or new_list_place.place_id != place_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="list_id and place_id cannot be changed"
            )
        list_place.position = new_list_place.position
        list_place.is_deleted = new_list_place.is_deleted
        session.add(list_place)
        session.commit()
        session.refresh(list_place)
        return list_place

@app.delete("/list-places/{list_id}/{place_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_place_from_list(list_id: int, place_id: int):
    with Session(engine) as session:
        list_place = session.get(ListPlaceDB, (list_id, place_id))
        if list_place is None or list_place.is_deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Place not found in this list"
            )
        list_place.is_deleted = True   # [FINAL] soft delete
        session.add(list_place)
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