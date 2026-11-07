import { fail } from '@sveltejs/kit';
import { API_URL } from '#lib/server/api.js';

export async function load({ fetch }) {
    try {
        // ดึงทั้ง Journals และ Places (เพื่อเอามาทำ Dropdown ให้ User เลือกตอน Add)
        const [journalsRes, placesRes] = await Promise.all([
            fetch(`${API_URL}/journals/`),
            fetch(`${API_URL}/places/`)
        ]);
        
        if (!journalsRes.ok || !placesRes.ok) throw new Error('โหลดข้อมูลไม่สำเร็จ');
        
        return { 
            logs: await journalsRes.json(),
            places: await placesRes.json()
        };
    } catch (err) {
        return { logs: [], places: [] };
    }
}

export const actions = {
    // 1. เพิ่มรีวิว
    create: async ({ request, fetch }) => {
        const data = await request.formData();
        const payload = {
            user_id: 1, // Mock user ไว้ที่ 1 ก่อนจนกว่าจะทำระบบ Sign In
            place_id: Number(data.get('place_id')),
            title: data.get('title'),
            rating: Number(data.get('rating')),
            note: data.get('note'),
            is_public: true
        };

        const res = await fetch(`${API_URL}/journals/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (!res.ok) {
            const err = await res.json().catch(() => null);
            return fail(res.status, { message: err?.detail ?? 'Failed to create journal' });
        }
        return { success: true };
    },

    // 2. แก้ไขรีวิว
    update: async ({ request, fetch }) => {
        const data = await request.formData();
        const id = data.get('id');
        const payload = {
            user_id: 1, 
            place_id: Number(data.get('place_id')),
            title: data.get('title'),
            rating: Number(data.get('rating')),
            note: data.get('note'),
            is_public: true
        };

        const res = await fetch(`${API_URL}/journals/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (!res.ok) return fail(res.status, { message: 'Failed to update journal' });
        return { success: true };
    },

    // 3. ลบรีวิว
    delete: async ({ request, fetch }) => {
        const data = await request.formData();
        const id = data.get('id');

        const res = await fetch(`${API_URL}/journals/${id}`, { method: 'DELETE' });

        if (!res.ok) return fail(res.status, { message: 'Failed to delete journal' });
        return { success: true };
    }
};