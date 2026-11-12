import { getCatalog, decoratePlaces } from '#lib/server/data.js';

// "Recommend this week": หมุนรายการไปทีละสัปดาห์
function weekly(items, n = 4) {
	if (items.length === 0) return [];
	const week = Math.floor(Date.now() / (7 * 24 * 3600 * 1000));
	return Array.from({ length: Math.min(n, items.length) }, (_, i) => items[(week + i) % items.length]);
}

export async function load({ fetch }) {
	const catalog = await getCatalog(fetch);
	const places = decoratePlaces(catalog.places, catalog);
	return {
		places: weekly(places),
		areas: weekly(catalog.areas)
	};
}
