import { error, fail } from '@sveltejs/kit';

export const API_URL = 'http://127.0.0.1:8000';

/** ใช้ใน load(): ดึงข้อมูลจาก FastAPI ถ้าไม่สำเร็จให้ขึ้นหน้า error (ไม่มีข้อมูลสำรอง) */
export async function api(path, fetch) {
	const res = await fetch(`${API_URL}${path}`);
	if (!res.ok) error(res.status === 404 ? 404 : 502, `Failed to load data from FastAPI: ${path} (${res.status})`);
	return res.json();
}

/** ใช้ใน actions: อ่านข้อมูล 1 รายการ คืน null ถ้าไม่มี (หรือถูกลบแล้ว) แทนการขึ้นหน้า error */
export async function findOne(path, fetch) {
	const res = await fetch(`${API_URL}${path}`);
	if (!res.ok) return null;
	return res.json();
}

/** ใช้ใน actions: ส่ง POST / PUT ไป FastAPI ถ้า FastAPI ตอบ error ให้คืน fail() กลับไปที่หน้าเว็บ */
export async function send(fetch, path, method, body) {
	const res = await fetch(`${API_URL}${path}`, {
		method,
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify(body)
	});
	if (!res.ok) {
		const err = await res.json().catch(() => null);
		const message = typeof err?.detail === 'string' ? err.detail : `FastAPI error (${res.status})`;
		return fail(res.status, { message });
	}
	return { success: true };
}
