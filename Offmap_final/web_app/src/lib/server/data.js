import { api } from './api.js';
import * as mock from './mock.js';

// ---------------------------------------------------------------
// Catalog: places / areas / vibes / place_vibes  (มีใน backend แล้ว)
// ถ้า backend ปิดอยู่จะใช้ข้อมูลตัวอย่างแทน และตั้ง offline = true
// ---------------------------------------------------------------
export async function getCatalog(fetchFn) {
	try {
		const [places, areas, vibes, placeVibes] = await Promise.all([
			api('/places/?limit=500', fetchFn),
			api('/areas/', fetchFn),
			api('/vibes/', fetchFn),
			api('/place-vibes/?limit=1000', fetchFn)
		]);
		return { places, areas, vibes, placeVibes, offline: false };
	} catch {
		return {
			places: mock.places,
			areas: mock.areas,
			vibes: mock.vibes,
			placeVibes: mock.placeVibes,
			offline: true
		};
	}
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

// ---------------------------------------------------------------
// User: โปรไฟล์ / favorites / journals  (มีใน backend แล้ว)
// ---------------------------------------------------------------
const formatDate = (iso) =>
	iso
		? new Date(iso).toLocaleDateString('en-GB', {
				day: 'numeric', month: 'short', year: 'numeric', timeZone: 'Asia/Bangkok'
			})
		: null;

// ตัด password_hash / email ออก ไม่ให้ถูกส่งไปที่เบราว์เซอร์
const publicUser = (u) => ({
	user_id: u.user_id,
	name: u.name,
	nationality: u.nationality ?? null,
	preferred_language: u.preferred_language ?? null,
	profile_image_url: u.profile_image_url ?? null
});

export async function getUserData(fetchFn, userId, catalog) {
	let user, favorites, journals, offline = catalog.offline;

	if (!offline) {
		try {
			[user, favorites, journals] = await Promise.all([
				api(`/users/${userId}`, fetchFn),
				api(`/favorites/?user_id=${userId}`, fetchFn),
				api(`/journals/?user_id=${userId}`, fetchFn)
			]);
		} catch {
			offline = true;
		}
	}
	if (offline) {
		user = mock.users.find((u) => u.user_id === userId);
		favorites = mock.favorites.filter((f) => f.user_id === userId);
		journals = mock.journals.filter((j) => j.user_id === userId);
	}

	const decorated = decoratePlaces(catalog.places, catalog);
	const byId = new Map(decorated.map((p) => [p.place_id, p]));

	return {
		user: publicUser(user),
		favoritePlaces: favorites.map((f) => byId.get(f.place_id)).filter(Boolean),
		journals: journals.map((j) => ({
			id: j.id,
			title: j.title,
			rating: j.rating,
			note: j.note,
			place_name: byId.get(j.place_id)?.place_name ?? 'Unknown place',
			visited: formatDate(j.visited_at)
		})),
		offline
	};
}

// ---------------------------------------------------------------
// NOT IN BACKEND YET: lists + follow
// ตอนนี้อ่านจาก mock.js ทั้งหมด ถ้าเพื่อนเพิ่ม endpoint (เช่น /lists/, /follows/)
// ให้แก้เฉพาะสองฟังก์ชันนี้ — หน้าเว็บไม่ต้องแก้
// รูปร่างที่หน้าเว็บคาดหวังอยู่ใน mock.js (lists, savedLists, follows)
// ---------------------------------------------------------------
const ownerName = (id) => mock.users.find((u) => u.user_id === id)?.name ?? 'Unknown';
const withMeta = (l) => ({ ...l, owner_name: ownerName(l.owner_id), place_count: l.place_ids.length });

export function getListsData(userId) {
	const all = mock.lists.map(withMeta);
	const savedIds = new Set(mock.savedLists.filter((s) => s.user_id === userId).map((s) => s.list_id));
	return {
		others: all.filter((l) => l.owner_id !== userId), // list ของคนอื่น (หน้า Lists)
		mine: all.filter((l) => l.owner_id === userId),
		saved: all.filter((l) => savedIds.has(l.list_id))
	};
}

export function getFollowData(userId) {
	const following = mock.follows
		.filter((f) => f.follower_id === userId)
		.map((f) => mock.users.find((u) => u.user_id === f.following_id))
		.filter(Boolean)
		.map((u) => ({ user_id: u.user_id, name: u.name, nationality: u.nationality ?? null }));
	return { following, followerCount: mock.followerCounts[userId] ?? 0 };
}