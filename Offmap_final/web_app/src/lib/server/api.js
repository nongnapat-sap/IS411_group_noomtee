import { env } from '$env/dynamic/private';

// ตั้ง API_BASE ใน .env ได้ เช่น API_BASE=http://127.0.0.1:8000
const API_BASE = env.API_BASE ?? 'http://127.0.0.1:8000';

/** เรียก backend (FastAPI) แล้วคืน JSON — โยน error ถ้าเชื่อมต่อไม่ได้หรือสถานะไม่ใช่ 2xx */
export async function api(path, fetchFn = fetch) {
	const res = await fetchFn(`${API_BASE}${path}`, { signal: AbortSignal.timeout(3000) });
	if (!res.ok) throw new Error(`${path} -> ${res.status}`);
	return res.json();
}