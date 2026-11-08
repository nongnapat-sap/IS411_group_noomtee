import { getCatalog, decoratePlaces } from '#lib/server/data.js';

export async function load({ fetch }) {
	const catalog = await getCatalog(fetch);
	return {
		places: decoratePlaces(catalog.places, catalog),
		areas: catalog.areas,
		vibes: catalog.vibes
	};
}