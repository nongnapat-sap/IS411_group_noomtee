import { api } from '#lib/server/api.js';
import { getCatalog, decoratePlaces } from '#lib/server/data.js';

// /areas/1 → params.area_id === '1' (เป็น string)
export async function load({ fetch, params }) {
	const [area, catalog] = await Promise.all([
		api(`/areas/${params.area_id}`, fetch),
		getCatalog(fetch)
	]);
	const places = await api(`/areas/${params.area_id}/places`, fetch);

	return {
		area,
		places: decoratePlaces(places, catalog)
	};
}
