import { fail } from '@sveltejs/kit';
import { CURRENT_USER_ID } from '#lib/config.js';
import { API_URL } from '#lib/server/api.js';
import { getCatalog, getUserData, getListsData, getFollowData } from '#lib/server/data.js';

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

// อ่านค่าจากฟอร์ม journal (formData ได้ค่าเป็น string เสมอ จึงต้องแปลงเป็นตัวเลข)
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

// ตรวจข้อมูลก่อนส่งไป FastAPI ถ้าผิดคืนข้อความกลับไปที่หน้าเว็บ
function validate(journal) {
	if (!journal.place_id) return 'กรุณาเลือกสถานที่';
	if (!journal.title) return 'กรุณาใส่หัวข้อ';
	if (!(journal.rating >= 1 && journal.rating <= 5)) return 'คะแนนต้องอยู่ระหว่าง 1–5';
	return null;
}

async function sendToApi(fetch, path, method, body) {
	const res = await fetch(`${API_URL}${path}`, {
		method,
		headers: body ? { 'Content-Type': 'application/json' } : undefined,
		body: body ? JSON.stringify(body) : undefined
	});
	if (!res.ok) {
		const err = await res.json().catch(() => null);
		const message = typeof err?.detail === 'string' ? err.detail : `FastAPI error (${res.status})`;
		return fail(res.status, { message });
	}
	return { success: true };
}

export const actions = {
	createJournal: async ({ request, fetch }) => {
		const journal = readJournal(await request.formData());
		const message = validate(journal);
		if (message) return fail(422, { message });
		return sendToApi(fetch, '/journals/', 'POST', journal);
	},

	updateJournal: async ({ request, fetch }) => {
		const fd = await request.formData();
		const journal = readJournal(fd);
		const message = validate(journal);
		if (message) return fail(422, { message });
		return sendToApi(fetch, `/journals/${fd.get('id')}`, 'PUT', journal);
	},

	deleteJournal: async ({ request, fetch }) => {
		const fd = await request.formData();
		return sendToApi(fetch, `/journals/${fd.get('id')}`, 'DELETE');
	}
};
