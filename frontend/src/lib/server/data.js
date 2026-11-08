import { api } from './api.js';

// ไฟล์นี้ไม่มีข้อมูลเก็บไว้เอง ทุกฟังก์ชันรับ fetch มาจาก load() แล้วดึงจาก FastAPI เท่านั้น
// แยกไว้ที่นี่เพราะหลายหน้าต้องใช้ข้อมูลชุดเดียวกัน

// ---------------- สถานที่ / ย่าน / vibe ----------------
export async function getCatalog(fetch) {
	const [places, areas, vibes, placeVibes] = await Promise.all([
		api('/places/?limit=500', fetch),
		api('/areas/', fetch),
		api('/vibes/', fetch),
		api('/place-vibes/?limit=1000', fetch)
	]);
	return { places, areas, vibes, placeVibes };
}

/** ใส่ area_name และ vibes (ชื่อ) ให้แต่ละ place เพื่อให้การ์ดแสดงผลได้เลย */
export function decoratePlaces(places, { areas, vibes, placeVibes }) {
	const areaName = new Map(areas.map((a) => [a.area_id, a.area_name]));
	const vibeName = new Map(vibes.map((v) => [v.vibe_id, v.vibe_name]));
	const vibesOf = new Map();
	for (const pv of placeVibes) {
		if (!vibesOf.has(pv.place_id)) vibesOf.set(pv.place_id, []);
		if (vibeName.has(pv.vibe_id)) vibesOf.get(pv.place_id).push(vibeName.get(pv.vibe_id));
	}
	return places.map((p) => ({
		...p,
		area_name: areaName.get(p.area_id) ?? null,
		vibes: vibesOf.get(p.place_id) ?? []
	}));
}

// ---------------- ผู้ใช้ ----------------
const formatDate = (iso) =>
	iso
		? new Date(iso).toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' })
		: null;

// backend ส่ง password_hash และ email มาด้วย ต้องตัดออกก่อนส่งไปที่เบราว์เซอร์
const publicUser = (u) => ({
	user_id: u.user_id,
	name: u.name,
	nationality: u.nationality ?? null,
	preferred_language: u.preferred_language ?? null,
	profile_image_url: u.profile_image_url ?? null
});

export async function getUserData(fetch, userId, catalog) {
	const [user, favorites, journals] = await Promise.all([
		api(`/users/${userId}`, fetch),
		api(`/favorites/?user_id=${userId}`, fetch),
		api(`/journals/?user_id=${userId}`, fetch)
	]);
	const byId = new Map(decoratePlaces(catalog.places, catalog).map((p) => [p.place_id, p]));

	return {
		user: publicUser(user),
		favoritePlaces: favorites.map((f) => byId.get(f.place_id)).filter(Boolean),
		journals: journals.map((j) => ({
			id: j.id,
			place_id: j.place_id,
			title: j.title,
			rating: j.rating,
			note: j.note,
			visited_at: j.visited_at,
			place_name: byId.get(j.place_id)?.place_name ?? 'Unknown place',
			visited: formatDate(j.visited_at)
		}))
	};
}

// ---------------- Lists ----------------
// backend ใช้ชื่อ field ต่างจากที่การ์ดใช้ จึงแปลงชื่อที่นี่ที่เดียว:
// list_name → title, user_id → owner_name, list-places → place_ids, saved-lists → saves
export async function getListsData(fetch, userId, catalog) {
	const [lists, users, saved] = await Promise.all([
		api('/lists/', fetch),
		api('/users/', fetch),
		api('/saved-lists/?limit=1000', fetch)
	]);
	const placesOf = await Promise.all(lists.map((l) => api(`/list-places/${l.list_id}`, fetch)));

	const userName = new Map(users.map((u) => [u.user_id, u.name]));
	const vibeName = new Map(catalog.vibes.map((v) => [v.vibe_id, v.vibe_name]));
	const vibesOfPlace = new Map();
	for (const pv of catalog.placeVibes) {
		if (!vibesOfPlace.has(pv.place_id)) vibesOfPlace.set(pv.place_id, []);
		vibesOfPlace.get(pv.place_id).push(pv.vibe_id);
	}

	const all = lists.map((l, i) => {
		const place_ids = placesOf[i].map((lp) => lp.place_id);
		// list ใน backend ไม่มี vibe ของตัวเอง จึงใช้ vibe ของสถานที่ใน list แทน
		const vibe_ids = [...new Set(place_ids.flatMap((id) => vibesOfPlace.get(id) ?? []))];
		return {
			list_id: l.list_id,
			title: l.list_name,
			description: l.description,
			is_public: l.is_public,
			owner_id: l.user_id,
			owner_name: userName.get(l.user_id) ?? 'Unknown',
			place_ids,
			place_count: place_ids.length,
			saves: saved.filter((s) => s.list_id === l.list_id).length,
			vibe_ids,
			vibe_name: vibeName.get(vibe_ids[0]) ?? null
		};
	});

	// list_id → saved_list_id ของผู้ใช้คนนี้ (ใช้ทั้งเช็กว่า save แล้วหรือยัง และส่งไปตอนเลิก save)
	const savedIdOf = {};
	for (const s of saved) if (s.user_id === userId) savedIdOf[s.list_id] = s.saved_list_id;

	return {
		others: all.filter((l) => l.is_public && l.owner_id !== userId),
		mine: all.filter((l) => l.owner_id === userId),
		saved: all.filter((l) => savedIdOf[l.list_id]),
		savedIdOf
	};
}

// ---------------- Follow ----------------
export async function getFollowData(fetch, userId) {
	const [following, followers] = await Promise.all([
		api(`/users/${userId}/following`, fetch),
		api(`/users/${userId}/followers`, fetch)
	]);
	return {
		following: following.map((u) => ({
			user_id: u.user_id,
			name: u.name,
			nationality: u.nationality ?? null
		})),
		followerCount: followers.length
	};
}

// ---------------- Favorites ----------------
/** place_id → favorite_id ของผู้ใช้คนนี้ (FastAPI ไม่ส่งรายการที่ถูกลบแล้วมา) */
export async function getFavoriteIdOf(fetch, userId) {
	const favorites = await api(`/favorites/?user_id=${userId}`, fetch);
	const favoriteIdOf = {};
	for (const f of favorites) favoriteIdOf[f.place_id] = f.favorite_id;
	return favoriteIdOf;
}
