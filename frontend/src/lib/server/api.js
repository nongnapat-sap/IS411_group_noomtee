import { error } from '@sveltejs/kit';

export const API_URL = 'http://127.0.0.1:8000';

/** ดึงข้อมูลจาก FastAPI ถ้าไม่สำเร็จให้ขึ้นหน้า error (ไม่มีข้อมูลสำรอง) */
export async function api(path, fetch) {
	const res = await fetch(`${API_URL}${path}`);
	if (!res.ok) error(res.status === 404 ? 404 : 502, `โหลดข้อมูลจาก FastAPI ไม่สำเร็จ: ${path} (${res.status})`);
	return res.json();
}