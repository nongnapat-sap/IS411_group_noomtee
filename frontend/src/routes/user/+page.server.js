import { fail } from '@sveltejs/kit';
import { CURRENT_USER_ID } from '#lib/config.js';
import { findOne, send } from '#lib/server/api.js';
import { getCatalog, getUserData, getListsData, getFollowData } from '#lib/server/data.js';
import { followActions, readCollectionForm } from '#lib/server/actions.js';

export async function load({ fetch }) {
	const catalog = await getCatalog(fetch);
	const [profile, lists, follow] = await Promise.all([
		getUserData(fetch, CURRENT_USER_ID, catalog),
		getListsData(fetch, CURRENT_USER_ID, catalog),
		getFollowData(fetch, CURRENT_USER_ID)
	]);

	return {
		user: profile.user,
		favoritePlaces: profile.favoritePlaces,
		journals: profile.journals,
		myLists: lists.mine,
		savedLists: lists.saved,
		following: follow.following,
		followerCount: follow.followerCount,
		// ใช้ทำ dropdown เลือกสถานที่ในฟอร์ม journal
		places: catalog.places
	};
}

// ---------------------------------------------------------------
// อ่านค่าจากฟอร์ม (formData ได้ค่าเป็น string เสมอ จึงต้องแปลงเป็นตัวเลข)
// ---------------------------------------------------------------
function readJournal(fd) {
	const visited = String(fd.get('visited_at') ?? '').trim();
	return {
		user_id: CURRENT_USER_ID,
		place_id: Number(fd.get('place_id')),
		title: String(fd.get('title') ?? '').trim(),
		rating: Number(fd.get('rating')),
		note: String(fd.get('note') ?? '').trim(),
		visited_at: visited ? `${visited}T00:00:00` : null,
		is_public: true
	};
}

// ---------------------------------------------------------------
// Validation ชั้น +page.server.js (ชั้นหน้าเว็บคือ required, ชั้น backend คือ Field ใน models.py)
// ---------------------------------------------------------------
function validateJournal(journal) {
	if (!journal.place_id) return 'Please select a place';
	if (!journal.title) return 'Please enter a title';
	if (journal.title.length > 100) return 'Title must be 100 characters or fewer';
	if (!(journal.rating >= 1 && journal.rating <= 5)) return 'Rating must be between 1 and 5';
	if (journal.note.length > 500) return 'Note must be 500 characters or fewer';
	if (journal.visited_at && new Date(journal.visited_at) > new Date()) return 'Visit date cannot be in the future';
	return null;
}

// ใช้ก่อน update และ delete: id ถูกต้อง, journal มีจริง (ยังไม่ถูกลบ), เป็นของผู้ใช้คนนี้
async function checkOwnJournal(fetch, id) {
	if (!id || Number.isNaN(Number(id))) {
		return { problem: fail(400, { message: 'Invalid journal ID' }) };
	}
	const journal = await findOne(`/journals/${id}`, fetch);
	if (!journal) {
		return { problem: fail(404, { message: 'Journal not found or already deleted' }) };
	}
	if (journal.user_id !== CURRENT_USER_ID) {
		return { problem: fail(403, { message: 'You can only edit or delete your own journals' }) };
	}
	return { journal };
}

export const actions = {
	// unfollow (DELETE = UPDATE is_deleted) ใช้โค้ดร่วมจาก src/lib/server/actions.js
	...followActions,

	// CREATE: สร้าง collection ใหม่ของตัวเอง
	createCollection: async ({ request, fetch }) => {
		const { collection, message } = readCollectionForm(await request.formData());
		if (message) return fail(422, { message });
		return send(fetch, '/lists/', 'POST', { user_id: CURRENT_USER_ID, cover_image_url: null, ...collection });
	},

	// CREATE
	createJournal: async ({ request, fetch }) => {
		const journal = readJournal(await request.formData());
		const message = validateJournal(journal);
		if (message) return fail(422, { message });
		return send(fetch, '/journals/', 'POST', journal);
	},

	// UPDATE
	updateJournal: async ({ request, fetch }) => {
		const fd = await request.formData();
		const { problem } = await checkOwnJournal(fetch, fd.get('id'));
		if (problem) return problem;

		const journal = readJournal(fd);
		const message = validateJournal(journal);
		if (message) return fail(422, { message });
		return send(fetch, `/journals/${fd.get('id')}`, 'PUT', journal);
	},

	// DELETE = UPDATE ให้ is_deleted เป็น true (soft delete) ข้อมูลยังอยู่ใน database
	deleteJournal: async ({ request, fetch }) => {
		const fd = await request.formData();
		const { journal, problem } = await checkOwnJournal(fetch, fd.get('id'));
		if (problem) return problem;
		return send(fetch, `/journals/${journal.id}`, 'PUT', { ...journal, is_deleted: true });
	}
};
