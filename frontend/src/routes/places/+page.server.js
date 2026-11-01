import { error, fail } from '@sveltejs/kit';
import { API_URL } from '#lib/server/api.js';

export async function load({ fetch }) {
    const [placesRes, areasRes] = await Promise.all([
        fetch(`${API_URL}/places/`),
        fetch(`${API_URL}/areas/`)
    ]);
    if (!placesRes.ok || !areasRes.ok) error(502, 'โหลดข้อมูลจาก FastAPI ไม่สำเร็จ');
    return { places: await placesRes.json(), areas: await areasRes.json() };
}

function readPlace(fd) {
    const text = (k) => String(fd.get(k) ?? '').trim();
    return {
        place_name: text('place_name'), description: text('description'),
        area_id: Number(text('area_id')), address: text('address'),
        latitude: Number(text('latitude')), longitude: Number(text('longitude')),
        price_level: text('price_level'), opening_time: text('opening_time'),
        closing_time: text('closing_time'), booking_link: text('booking_link') || null,
        image_url: text('image_url') || null
    };
}

async function callApi(fetch, path, method, body) {
    const res = await fetch(`${API_URL}${path}`, {
        method, headers: body ? { 'Content-Type': 'application/json' } : undefined,
        body: body ? JSON.stringify(body) : undefined
    });
    if (!res.ok) {
        const data = await res.json().catch(() => null);
        return fail(res.status, { message: data?.detail ?? `FastAPI error (${res.status})` });
    }
    return { success: true };
}

export const actions = {
    create: async ({ request, fetch }) => callApi(fetch, '/places/', 'POST', readPlace(await request.formData()))
};