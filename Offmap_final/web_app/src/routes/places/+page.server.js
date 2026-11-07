import { getCatalog, decoratePlaces } from '$lib/server/data.js';

// กรองผ่าน query string: /places?vibe=2&area=3
// (ใช้ลิงก์ธรรมดา ไม่ต้องพึ่ง JS ฝั่งเบราว์เซอร์ และ share URL ได้)
export async function load({ fetch, url }) {
	const catalog = await getCatalog(fetch);
	const vibeId = Number(url.searchParams.get('vibe')) || null;
	const areaId = Number(url.searchParams.get('area')) || null;

	let places = decoratePlaces(catalog.places, catalog);

	if (areaId) {
		places = places.filter((p) => p.area_id === areaId);
	}
	if (vibeId) {
		const ids = new Set(
			catalog.placeVibes.filter((pv) => pv.vibe_id === vibeId).map((pv) => pv.place_id)
		);
		places = places.filter((p) => ids.has(p.place_id));
	}

	return {
		places,
		vibes: catalog.vibes,
		activeVibe: vibeId,
		activeArea: catalog.areas.find((a) => a.area_id === areaId) ?? null,
		offline: catalog.offline
	};
}