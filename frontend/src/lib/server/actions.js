import { fail } from '@sveltejs/kit';
import { CURRENT_USER_ID } from '#lib/config.js';
import { api, findOne, send } from './api.js';
import { getFavoriteIdOf } from './data.js';

// ---------------------------------------------------------------
// actions ที่ใช้ซ้ำหลายหน้า รวมไว้ที่ไฟล์เดียว
// แต่ละหน้าดึงไปใช้ด้วย  export const actions = { ...favoriteActions }
// ทุก action: อ่านฟอร์ม → validation → ส่งไป FastAPI ด้วย send()
// ลบ = PUT ให้ is_deleted เป็น true (soft delete) ไม่ใช่ DELETE
// ---------------------------------------------------------------

// ---------------- Favorites (หน้า Explore และหน้ารายละเอียดสถานที่) ----------------
export const favoriteActions = {
	// CREATE: เพิ่มสถานที่เข้า favorites
	addFavorite: async ({ request, fetch }) => {
		const fd = await request.formData();
		const placeId = Number(fd.get('place_id'));

		if (!placeId) return fail(400, { message: 'Invalid place ID' });
		const place = await findOne(`/places/${placeId}`, fetch);
		if (!place) return fail(404, { message: 'Place not found' });
		const favoriteIdOf = await getFavoriteIdOf(fetch, CURRENT_USER_ID);
		if (favoriteIdOf[placeId]) {
			return fail(409, { message: `${place.place_name} is already in your favorites` });
		}

		return send(fetch, '/favorites/', 'POST', { user_id: CURRENT_USER_ID, place_id: placeId });
	},

	// DELETE = UPDATE ให้ is_deleted เป็น true
	removeFavorite: async ({ request, fetch }) => {
		const fd = await request.formData();
		const favoriteId = Number(fd.get('favorite_id'));

		if (!favoriteId) return fail(400, { message: 'Invalid favorite ID' });
		const favorite = await findOne(`/favorites/${favoriteId}`, fetch);
		if (!favorite) return fail(404, { message: 'Favorite not found or already removed' });
		if (favorite.user_id !== CURRENT_USER_ID) {
			return fail(403, { message: 'You can only remove your own favorites' });
		}

		return send(fetch, `/favorites/${favoriteId}`, 'PUT', { ...favorite, is_deleted: true });
	}
};

// ---------------- Save collection (หน้า Collections และหน้ารายละเอียด collection) ----------------
// หมายเหตุ: บนหน้าเว็บเรียกว่า Collection แต่ใน FastAPI คือตาราง lists / saved_lists
export const saveActions = {
	// CREATE: save collection ของคนอื่น
	saveList: async ({ request, fetch }) => {
		const fd = await request.formData();
		const listId = Number(fd.get('list_id'));

		if (!listId) return fail(400, { message: 'Invalid collection ID' });
		const list = await findOne(`/lists/${listId}`, fetch);
		if (!list) return fail(404, { message: 'Collection not found' });
		if (!list.is_public) return fail(403, { message: 'This collection is private and cannot be saved' });
		if (list.user_id === CURRENT_USER_ID) {
			return fail(400, { message: 'You cannot save your own collection' });
		}
		const mine = await api(`/saved-lists/?user_id=${CURRENT_USER_ID}`, fetch);
		if (mine.some((s) => s.list_id === listId)) {
			return fail(409, { message: `"${list.list_name}" is already in your saved collections` });
		}

		return send(fetch, '/saved-lists/', 'POST', { user_id: CURRENT_USER_ID, list_id: listId });
	},

	// DELETE = UPDATE ให้ is_deleted เป็น true
	unsaveList: async ({ request, fetch }) => {
		const fd = await request.formData();
		const savedListId = Number(fd.get('saved_list_id'));

		if (!savedListId) return fail(400, { message: 'Invalid saved collection ID' });
		const mine = await api(`/saved-lists/?user_id=${CURRENT_USER_ID}`, fetch);
		const record = mine.find((s) => s.saved_list_id === savedListId);
		if (!record) return fail(404, { message: 'This collection is not in your saved collections' });

		return send(fetch, `/saved-lists/${savedListId}`, 'PUT', { ...record, is_deleted: true });
	}
};

// ---------------- Follow (หน้ารายละเอียด collection และหน้า My Profile) ----------------
export const followActions = {
	// CREATE: ติดตามผู้ใช้
	follow: async ({ request, fetch }) => {
		const fd = await request.formData();
		const userId = Number(fd.get('user_id'));

		if (!userId) return fail(400, { message: 'Invalid user ID' });
		if (userId === CURRENT_USER_ID) return fail(400, { message: 'You cannot follow yourself' });
		const person = await findOne(`/users/${userId}`, fetch);
		if (!person) return fail(404, { message: 'User not found' });
		const mine = await api(`/follows/?follower_id=${CURRENT_USER_ID}`, fetch);
		if (mine.some((f) => f.following_id === userId)) {
			return fail(409, { message: `You are already following ${person.name}` });
		}

		return send(fetch, '/follows/', 'POST', { follower_id: CURRENT_USER_ID, following_id: userId });
	},

	// DELETE = UPDATE ให้ is_deleted เป็น true (เลิกติดตาม)
	unfollow: async ({ request, fetch }) => {
		const fd = await request.formData();
		const followId = Number(fd.get('follow_id'));

		if (!followId) return fail(400, { message: 'Invalid follow ID' });
		const follow = await findOne(`/follows/${followId}`, fetch);
		if (!follow) return fail(404, { message: 'You are not following this user' });
		if (follow.follower_id !== CURRENT_USER_ID) {
			return fail(403, { message: 'You can only unfollow for yourself' });
		}

		return send(fetch, `/follows/${followId}`, 'PUT', { ...follow, is_deleted: true });
	}
};

// ---------------- ตัวช่วยตรวจ collection ของตัวเอง ----------------
// ใช้ก่อน update / delete / เพิ่มหรือเอาสถานที่ออก
export async function checkOwnCollection(fetch, id) {
	if (!id || Number.isNaN(Number(id))) {
		return { problem: fail(400, { message: 'Invalid collection ID' }) };
	}
	const list = await findOne(`/lists/${id}`, fetch);
	if (!list) return { problem: fail(404, { message: 'Collection not found or already deleted' }) };
	if (list.user_id !== CURRENT_USER_ID) {
		return { problem: fail(403, { message: 'You can only change your own collections' }) };
	}
	return { list };
}

// อ่านค่าฟอร์มสร้าง/แก้ collection แล้วตรวจข้อมูล
export function readCollectionForm(fd) {
	const collection = {
		list_name: String(fd.get('list_name') ?? '').trim(),
		description: String(fd.get('description') ?? '').trim(),
		is_public: fd.get('is_public') === 'on'
	};
	let message = null;
	if (!collection.list_name) message = 'Please enter a collection name';
	else if (collection.list_name.length > 60) message = 'Collection name must be 60 characters or fewer';
	else if (collection.description.length > 200) message = 'Description must be 200 characters or fewer';
	return { collection, message };
}

// เพิ่มสถานที่เข้า collection ของตัวเอง (ใช้ทั้งหน้ารายละเอียด collection และหน้ารายละเอียดสถานที่)
export async function addPlaceToCollection(fetch, listId, placeId) {
	const { problem } = await checkOwnCollection(fetch, listId);
	if (problem) return problem;
	if (!placeId) return fail(400, { message: 'Please choose a place' });
	const place = await findOne(`/places/${placeId}`, fetch);
	if (!place) return fail(404, { message: 'Place not found' });
	const inList = await api(`/list-places/${listId}`, fetch);
	if (inList.some((lp) => lp.place_id === placeId)) {
		return fail(409, { message: `${place.place_name} is already in this collection` });
	}
	return send(fetch, '/list-places/', 'POST', {
		list_id: listId,
		place_id: placeId,
		position: inList.length + 1
	});
}
