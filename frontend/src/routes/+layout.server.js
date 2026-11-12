// ส่ง path ปัจจุบันให้ layout ใช้ไฮไลต์แท็บที่เปิดอยู่
export function load({ url }) {
	return { path: url.pathname };
}
