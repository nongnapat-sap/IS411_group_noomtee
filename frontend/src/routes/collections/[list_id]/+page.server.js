import { error, fail, redirect } from '@sveltejs/kit';
import { CURRENT_USER_ID } from '#lib/config.js';
import { api, send } from '#lib/server/api.js';
import { getCatalog, decoratePlaces } from '#lib/server/data.js';
import {
	saveActions,
	followActions,
	checkOwnCollection,
	readCollectionForm,
	addPlaceToCollection
} from '#lib/server/actions.js';

// หน้ารายละเอียด collection: /collections/3 → params.list_id = '3' (slug)
// (ใน FastAPI คือตาราง lists และ list_places)
export async function load({ fetch, params }) {
	const listId = Number(params.list_id);

	// ถ้าไม่มี หรือถูกลบแล้ว FastAPI ตอบ 404 → api() ส่งหน้า 404 ให้ผู้ใช้
	const list = await api(`/lists/${listId}`, fetch);
	const isOwner = list.user_id === CURRENT_USER_ID;

	// collection ส่วนตัวของคนอื่น → ทำเหมือนไม่มีอยู่
	if (!list.is_public && !isOwner) error(404, 'Collection not found');

	const [catalog, users, listPlaces, saved, myFollows] = await Promise.all([
		getCatalog(fetch),
		api('/users/', fetch),
		api(`/list-places/${listId}`, fetch),
		api('/saved-lists/?limit=1000', fetch),
		api(`/follows/?follower_id=${CURRENT_USER_ID}`, fetch)
	]);

	const allPlaces = decoratePlaces(catalog.places, catalog);
	const placeById = new Map(allPlaces.map((p) => [p.place_id, p]));
	const inList = listPlaces.map((lp) => placeById.get(lp.place_id)).filter(Boolean);
	const inListIds = new Set(inList.map((p) => p.place_id));
	const owner = users.find((u) => u.user_id === list.user_id);

	return {
		collection: {
			list_id: list.list_id,
			title: list.list_name,
			description: list.description ?? '',
			cover_image_url: list.cover_image_url ?? null,
			is_public: list.is_public
		},
		owner: {
			user_id: owner?.user_id ?? list.user_id,
			name: owner?.name ?? 'Unknown',
			avatar: owner?.profile_image_url ?? null,
			bio: owner?.bio ?? null
		},
		isOwner,
		places: inList,
		saves: saved.filter((s) => s.list_id === listId).length,
		savedListId: saved.find((s) => s.list_id === listId && s.user_id === CURRENT_USER_ID)?.saved_list_id ?? null,
		followId: myFollows.find((f) => f.following_id === list.user_id)?.follow_id ?? null,
		// สถานที่ที่ยังไม่อยู่ใน collection (ใช้ทำ dropdown เพิ่มสถานที่ เฉพาะเจ้าของ)
		addablePlaces: isOwner
			? allPlaces
					.filter((p) => !inListIds.has(p.place_id))
					.sort((a, b) => a.place_name.localeCompare(b.place_name))
					.map((p) => ({ place_id: p.place_id, place_name: p.place_name, area_name: p.area_name }))
			: []
	};
}

export const actions = {
	// saveList / unsaveList และ follow / unfollow ใช้โค้ดร่วมจาก src/lib/server/actions.js
	...saveActions,
	...followActions,

	// UPDATE: แก้ชื่อ คำอธิบาย และการแชร์ (เฉพาะเจ้าของ)
	updateCollection: async ({ request, fetch, params }) => {
		const { list, problem } = await checkOwnCollection(fetch, params.list_id);
		if (problem) return problem;

		const { collection, message } = readCollectionForm(await request.formData());
		if (message) return fail(422, { message });

		return send(fetch, `/lists/${list.list_id}`, 'PUT', { ...list, ...collection });
	},

	// DELETE = UPDATE ให้ is_deleted เป็น true แล้วกลับไปหน้าโปรไฟล์
	deleteCollection: async ({ fetch, params }) => {
		const { list, problem } = await checkOwnCollection(fetch, params.list_id);
		if (problem) return problem;

		const result = await send(fetch, `/lists/${list.list_id}`, 'PUT', { ...list, is_deleted: true });
		if (!result?.success) return result; // FastAPI ตอบ error → แสดงกล่องแดง
		redirect(303, '/user');
	},

	// CREATE: เพิ่มสถานที่เข้า collection (เฉพาะเจ้าของ)
	addPlace: async ({ request, fetch, params }) => {
		const fd = await request.formData();
		return addPlaceToCollection(fetch, Number(params.list_id), Number(fd.get('place_id')));
	},

	// DELETE = UPDATE ให้ is_deleted เป็น true (เอาสถานที่ออกจาก collection)
	removePlace: async ({ request, fetch, params }) => {
		const { list, problem } = await checkOwnCollection(fetch, params.list_id);
		if (problem) return problem;

		const placeId = Number((await request.formData()).get('place_id'));
		if (!placeId) return fail(400, { message: 'Invalid place ID' });
		const inList = await api(`/list-places/${list.list_id}`, fetch);
		const record = inList.find((lp) => lp.place_id === placeId);
		if (!record) return fail(404, { message: 'This place is not in the collection' });

		return send(fetch, `/list-places/${list.list_id}/${placeId}`, 'PUT', { ...record, is_deleted: true });
	}
};
