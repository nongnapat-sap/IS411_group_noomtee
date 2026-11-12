import { CURRENT_USER_ID } from '#lib/config.js';
import { api } from '#lib/server/api.js';
import { getCatalog, decoratePlaces, getFavoriteIdOf } from '#lib/server/data.js';
import { favoriteActions, addPlaceToCollection } from '#lib/server/actions.js';

const formatDate = (iso) =>
	iso ? new Date(iso).toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' }) : null;

// หน้ารายละเอียดสถานที่: /explore/5 → params.place_id = '5' (slug)
export async function load({ fetch, params }) {
	const placeId = Number(params.place_id);

	// ถ้าไม่มีสถานที่นี้ FastAPI ตอบ 404 → api() ส่งหน้า 404 ให้ผู้ใช้
	const [placeRaw, catalog, journals, users, favoriteIdOf, myLists] = await Promise.all([
		api(`/places/${placeId}`, fetch),
		getCatalog(fetch),
		api(`/journals/?place_id=${placeId}`, fetch),
		api('/users/', fetch),
		getFavoriteIdOf(fetch, CURRENT_USER_ID),
		api(`/lists/?user_id=${CURRENT_USER_ID}`, fetch)
	]);

	const place = decoratePlaces([placeRaw], catalog)[0];
	const area = catalog.areas.find((a) => a.area_id === place.area_id) ?? null;
	const userById = new Map(users.map((u) => [u.user_id, u]));

	// collection ของเรา: แยกว่าอันไหนมีสถานที่นี้แล้ว อันไหนยังไม่มี
	const placesInMyLists = await Promise.all(myLists.map((l) => api(`/list-places/${l.list_id}`, fetch)));
	const myCollections = myLists.map((l, i) => ({
		list_id: l.list_id,
		title: l.list_name,
		has_place: placesInMyLists[i].some((lp) => lp.place_id === placeId)
	}));

	return {
		place,
		area,
		favoriteId: favoriteIdOf[placeId] ?? null,
		// journal ที่ตั้งเป็นสาธารณะเท่านั้น ใหม่สุดขึ้นก่อน
		journals: journals
			.filter((j) => j.is_public)
			.sort((a, b) => String(b.visited_at).localeCompare(String(a.visited_at)))
			.map((j) => ({
				id: j.id,
				title: j.title,
				rating: j.rating,
				note: j.note,
				visited: formatDate(j.visited_at),
				author_name: userById.get(j.user_id)?.name ?? 'Unknown',
				author_avatar: userById.get(j.user_id)?.profile_image_url ?? null
			})),
		myCollections
	};
}

export const actions = {
	// addFavorite / removeFavorite ใช้โค้ดชุดเดียวกับหน้า Explore
	...favoriteActions,

	// CREATE: เพิ่มสถานที่นี้เข้า collection ของตัวเอง
	addToCollection: async ({ request, fetch, params }) => {
		const fd = await request.formData();
		return addPlaceToCollection(fetch, Number(fd.get('list_id')), Number(params.place_id));
	}
};
