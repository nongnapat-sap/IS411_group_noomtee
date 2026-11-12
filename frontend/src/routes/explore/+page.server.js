import { CURRENT_USER_ID } from '#lib/config.js';
import { getCatalog, decoratePlaces, getFavoriteIdOf } from '#lib/server/data.js';
import { favoriteActions } from '#lib/server/actions.js';

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

// addFavorite (CREATE) และ removeFavorite (DELETE = UPDATE is_deleted)
// โค้ดอยู่ใน src/lib/server/actions.js เพราะหน้ารายละเอียดสถานที่ใช้ร่วมกัน
export const actions = {
	...favoriteActions
};
