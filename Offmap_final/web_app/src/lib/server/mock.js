// ข้อมูลตัวอย่าง — ใช้เมื่อ backend ปิดอยู่ (หน้าเว็บจะขึ้นป้าย "sample data")
// รูปร่างข้อมูลตรงกับ response ของ backend (PlaceOut, AreaOut, ...) ตาม seed_data()
// ยกเว้นส่วน lists / follow ที่ backend ยังไม่มี (ดู "NOT IN BACKEND YET" ด้านล่าง)

const place = (place_id, place_name, description, area_id, address, price_level, opening_time, closing_time) => ({
	place_id, place_name, description, area_id, address,
	latitude: 13.74, longitude: 100.55,
	price_level, opening_time, closing_time,
	booking_link: null, image_url: null
});

export const places = [
	place(1, 'Saxophone Pub & Restaurant', 'A legendary live jazz music venue', 1, '3/8 Soi Ratchawithi 11, Ratchathewi, Bangkok 10400', '200-1000 THB', '18:00', '02:00'),
	place(2, 'Havana Social', 'A hidden 1940s pre-revolutionary Cuban-themed speakeasy', 2, '341 Sukhumvit Soi 11, Bangkok 10110', '400-1200 THB', '18:00', '02:00'),
	place(3, 'Upper House', 'A high-energy nightclub and bar', 3, '2nd floor of 24 BLVD at 88 Sukhumvit 24 Alley, Bangkok', '400-1200 THB', '21:00', '03:30'),
	place(4, 'Coco Walk', 'A popular hangout spot with multiple bars and live music', 1, 'Phaya Thai Rd, Ratchathewi, Bangkok', '200-800 THB', '17:00', '01:00'),
	place(5, 'Ari Beer Garden', 'Outdoor craft-beer taproom with live acoustic sets', 4, 'Soi Ari 4, Phaya Thai, Bangkok', '150-500 THB', '17:00', '00:00'),
	place(6, 'Ekkamai Rooftop', 'Open-air rooftop with city skyline views', 5, 'Soi Ekkamai 10, Watthana, Bangkok', '300-900 THB', '18:00', '01:00'),
	place(7, 'Ekkamai Late Bites', '24-hour street food spot popular after clubbing', 5, 'Soi Ekkamai 4, Watthana, Bangkok', '80-300 THB', '20:00', '06:00'),
	place(8, 'Silom Soi Speakeasy', 'Unmarked bar tucked in a narrow Silom alley', 6, 'Silom Soi 4, Bang Rak, Bangkok', '350-1000 THB', '19:00', '02:00'),
	place(9, 'Sky High Sathorn', 'Rooftop bar with panoramic Chao Phraya views', 7, 'Sathorn Rd, Sathon, Bangkok', '500-1500 THB', '17:30', '01:00'),
	place(10, 'Chinatown Neon Bar', 'Retro neon-lit bar serving Thai-Chinese fusion cocktails', 8, 'Yaowarat Rd, Samphanthawong, Bangkok', '250-700 THB', '18:00', '01:00')
];

const area = (area_id, area_name, district, description) => ({
	area_id, area_name, district, sub_district: null,
	latitude: 13.74, longitude: 100.55, description, cover_image_url: null,
	total_places: places.filter((p) => p.area_id === area_id).length
});

export const areas = [
	area(1, 'Ratchathewi', 'Ratchathewi', 'Home to Victory Monument and classic live-music venues'),
	area(2, 'Sukhumvit', 'Watthana', "Bangkok's nightlife hub with speakeasies and rooftop bars"),
	area(3, 'Thonglor', 'Watthana', 'Trendy district known for upscale clubs and cocktail bars'),
	area(4, 'Ari', 'Phaya Thai', 'Hip cafe and craft-beer neighborhood'),
	area(5, 'Ekkamai', 'Watthana', 'Laid-back bars and late-night eats'),
	area(6, 'Silom', 'Bang Rak', 'Business district by day, nightlife strip by night'),
	area(7, 'Sathorn', 'Sathon', 'Rooftop bars and skyline views'),
	area(8, 'Chinatown', 'Samphanthawong', 'Historic street-food and neon-lit alleys')
];

export const vibes = [
	{ vibe_id: 1, vibe_name: 'High Energy & Clubbing', description: 'Loud beats, DJ sets, dancing, and late-night party vibes' },
	{ vibe_id: 2, vibe_name: 'Rooftop & Skyline', description: 'Open-air scenic views of the Bangkok skyline and riverfront' },
	{ vibe_id: 3, vibe_name: 'Craft Beer & Taproom', description: 'Artisan beers on tap, casual brewing culture, and relaxed outdoor yards' },
	{ vibe_id: 4, vibe_name: 'Street Food & Late Bites', description: 'Late-night hunger cures, bustling street stalls, and affordable comfort eats' },
	{ vibe_id: 5, vibe_name: 'Retro & Neon', description: 'Nostalgic aesthetics, neon lights, and cultural fusion flair' },
	{ vibe_id: 6, vibe_name: 'Waterfront & Chill', description: 'Breezy riverside settings perfect for calm drinks and conversations' }
];

export const placeVibes = [
	{ place_id: 1, vibe_id: 1 },
	{ place_id: 2, vibe_id: 2 },
	{ place_id: 3, vibe_id: 3 },
	{ place_id: 5, vibe_id: 5 },
	{ place_id: 6, vibe_id: 4 },
	{ place_id: 7, vibe_id: 6 }
];

// ---------- ผู้ใช้ / favorites / journals (มีใน backend แล้ว) ----------
const user = (user_id, name, nationality, preferred_language) => ({
	user_id, name, email: `${name.split(' ')[0].toLowerCase()}@example.com`,
	profile_image_url: null, nationality, preferred_language,
	created_at: '2026-09-01T10:00:00', updated_at: '2026-09-01T10:00:00'
});

export const users = [
	user(1, 'Timothee Chalamet', 'French', 'French'),
	user(2, 'Sydney Sweeney', 'American', 'English'),
	user(3, 'Anya Taylor-Joy', 'British', 'English'),
	user(4, 'Austin Butler', 'American', 'English'),
	user(5, 'Hoyeon Jung', 'Korean', 'Korean'),
	user(6, 'Barry Keoghan', 'Irish', 'English'),
	user(7, 'Rosalia Vila', 'Spanish', 'Spanish'),
	user(8, 'Jung Ho-yeon', 'Korean', 'English'),
	user(9, 'Charles Melton', 'American', 'English'),
	user(10, 'Greta Lee', 'Korean-American', 'English')
];

// เพิ่มของ user 4 ให้เห็นหน้าตา UI ครบ 4 ใบ (ใน seed จริงมีแค่ 1)
export const favorites = [
	{ favorite_id: 1, user_id: 4, place_id: 4, created_at: '2026-09-03T10:00:00' },
	{ favorite_id: 2, user_id: 4, place_id: 1, created_at: '2026-09-04T10:00:00' },
	{ favorite_id: 3, user_id: 4, place_id: 6, created_at: '2026-09-05T10:00:00' },
	{ favorite_id: 4, user_id: 4, place_id: 8, created_at: '2026-09-06T10:00:00' }
];

export const journals = [
	{
		id: 1, user_id: 4, place_id: 1, title: 'Acoustic & Soulful Jazz Night', rating: 5,
		note: 'The live saxophone solo was breathtaking. Truly an iconic music haven.',
		visited_at: '2026-09-01T21:30:00', image_url: null, is_public: true,
		created_at: '2026-09-01T23:00:00', updated_at: '2026-09-01T23:00:00'
	},
	{
		id: 2, user_id: 4, place_id: 6, title: 'Golden hour on the roof', rating: 4,
		note: 'Great skyline at sunset. Go before 7 pm to get a seat at the edge.',
		visited_at: '2026-09-12T18:00:00', image_url: null, is_public: true,
		created_at: '2026-09-12T20:00:00', updated_at: '2026-09-12T20:00:00'
	}
];

// ---------- NOT IN BACKEND YET: lists / follow ----------
// เมื่อเพื่อนทำ endpoint แล้ว ให้ดู src/lib/server/data.js (getListsData / getFollowData)
// owner_id ชี้ไปที่ users, place_ids ชี้ไปที่ places, vibe_id ชี้ไปที่ vibes
export const lists = [
	{ list_id: 1, title: 'Rooftops with a view', description: 'Skyline drinks worth the elevator ride.', owner_id: 2, vibe_id: 2, place_ids: [6, 9], saves: 128 },
	{ list_id: 2, title: 'After-midnight eats', description: 'Where to go when the bars close and hunger hits.', owner_id: 3, vibe_id: 4, place_ids: [7, 10], saves: 96 },
	{ list_id: 3, title: 'Hidden speakeasies', description: 'No sign, no problem. Knock twice.', owner_id: 6, vibe_id: 5, place_ids: [2, 8], saves: 214 },
	{ list_id: 4, title: 'Live music nights', description: 'Jazz, acoustic sets and everything loud.', owner_id: 9, vibe_id: 1, place_ids: [1, 4, 5], saves: 77 },
	{ list_id: 5, title: 'Chill by the river', description: 'Slow drinks, cool breeze, long conversations.', owner_id: 10, vibe_id: 6, place_ids: [9, 10], saves: 143 },
	{ list_id: 6, title: 'Craft beer crawl', description: 'Taprooms and beer gardens, one night.', owner_id: 1, vibe_id: 3, place_ids: [5, 7], saves: 59 },
	// ของ user 4 (my list)
	{ list_id: 7, title: 'Date night shortlist', description: 'Dim lights, good cocktails.', owner_id: 4, vibe_id: 5, place_ids: [2, 9, 3], saves: 12 },
	{ list_id: 8, title: 'Weekend wanders', description: 'Easy places to drift between.', owner_id: 4, vibe_id: 6, place_ids: [5, 7, 10], saves: 3 }
];

// list ของคนอื่นที่ user 4 กด save ไว้ (saved list)
export const savedLists = [{ user_id: 4, list_id: 3 }, { user_id: 4, list_id: 5 }];

// คนที่ user 4 follow + จำนวน followers
export const follows = [
	{ follower_id: 4, following_id: 1 },
	{ follower_id: 4, following_id: 2 },
	{ follower_id: 4, following_id: 6 },
	{ follower_id: 4, following_id: 10 }
];
export const followerCounts = { 4: 18 };