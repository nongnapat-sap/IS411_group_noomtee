import { fail } from '@sveltejs/kit';
import { CURRENT_USER_ID } from '#lib/config.js';
import { findOne, send } from '#lib/server/api.js';
import { getCatalog, decoratePlaces, getFavoriteIdOf } from '#lib/server/data.js';

export async function load({ fetch }) {
	const [catalog, favoriteIdOf] = await Promise.all([
		getCatalog(fetch),
		getFavoriteIdOf(fetch, CURRENT_USER_ID)
	]);
	return {
		places: decoratePlaces(catalog.places, catalog),
		areas: catalog.areas,
		vibes: catalog.vibes,
		favoriteIdOf // place_id → favorite_id ใช้บอกว่าที่ไหนกด favorite ไว้แล้ว
	};
}

export const actions = {
	// CREATE: เพิ่มสถานที่เข้า favorites
	addFavorite: async ({ request, fetch }) => {
		const fd = await request.formData();
		const placeId = Number(fd.get('place_id'));

		// validation
		if (!placeId) return fail(400, { message: 'Invalid place ID' });
		const place = await findOne(`/places/${placeId}`, fetch);
		if (!place) return fail(404, { message: 'Place not found' });
		const favoriteIdOf = await getFavoriteIdOf(fetch, CURRENT_USER_ID);
		if (favoriteIdOf[placeId]) {
			return fail(409, { message: `${place.place_name} is already in your favorites` });
		}

		return send(fetch, '/favorites/', 'POST', { user_id: CURRENT_USER_ID, place_id: placeId });
	},

	// DELETE = UPDATE ให้ is_deleted เป็น true (soft delete)
	removeFavorite: async ({ request, fetch }) => {
		const fd = await request.formData();
		const favoriteId = Number(fd.get('favorite_id'));

		// validation
		if (!favoriteId) return fail(400, { message: 'Invalid favorite ID' });
		const favorite = await findOne(`/favorites/${favoriteId}`, fetch);
		if (!favorite) return fail(404, { message: 'Favorite not found or already removed' });
		if (favorite.user_id !== CURRENT_USER_ID) {
			return fail(403, { message: 'You can only remove your own favorites' });
		}

		return send(fetch, `/favorites/${favoriteId}`, 'PUT', { ...favorite, is_deleted: true });
	}
};