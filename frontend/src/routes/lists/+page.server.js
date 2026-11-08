import { fail } from '@sveltejs/kit';
import { CURRENT_USER_ID } from '#lib/config.js';
import { findOne, send, api } from '#lib/server/api.js';
import { getCatalog, getListsData } from '#lib/server/data.js';

// หน้า Lists = เลือกดู list สถานที่ของคนอื่น (การค้นหา/กรองทำในหน้าเว็บ)
export async function load({ fetch }) {
	const catalog = await getCatalog(fetch);
	const { others, savedIdOf } = await getListsData(fetch, CURRENT_USER_ID, catalog);

	return {
		lists: others,
		// "Popular this week" = list ที่คน save เยอะที่สุด
		popular: [...others].sort((a, b) => b.saves - a.saves).slice(0, 4),
		vibes: catalog.vibes,
		savedIdOf // list_id → saved_list_id ใช้บอกว่า list ไหน save ไว้แล้ว
	};
}

export const actions = {
	// CREATE: save list ของคนอื่น
	saveList: async ({ request, fetch }) => {
		const fd = await request.formData();
		const listId = Number(fd.get('list_id'));

		// validation
		if (!listId) return fail(400, { message: 'Invalid list ID' });
		const list = await findOne(`/lists/${listId}`, fetch);
		if (!list) return fail(404, { message: 'List not found' });
		if (!list.is_public) return fail(403, { message: 'This list is private and cannot be saved' });
		if (list.user_id === CURRENT_USER_ID) {
			return fail(400, { message: 'You cannot save your own list' });
		}
		const mine = await api(`/saved-lists/?user_id=${CURRENT_USER_ID}`, fetch);
		if (mine.some((s) => s.list_id === listId)) {
			return fail(409, { message: `"${list.list_name}" is already in your saved lists` });
		}

		return send(fetch, '/saved-lists/', 'POST', { user_id: CURRENT_USER_ID, list_id: listId });
	},

	// DELETE = UPDATE ให้ is_deleted เป็น true (soft delete)
	unsaveList: async ({ request, fetch }) => {
		const fd = await request.formData();
		const savedListId = Number(fd.get('saved_list_id'));

		// validation
		if (!savedListId) return fail(400, { message: 'Invalid saved list ID' });
		const mine = await api(`/saved-lists/?user_id=${CURRENT_USER_ID}`, fetch);
		const record = mine.find((s) => s.saved_list_id === savedListId);
		if (!record) return fail(404, { message: 'This list is not in your saved lists' });

		return send(fetch, `/saved-lists/${savedListId}`, 'PUT', { ...record, is_deleted: true });
	}
};