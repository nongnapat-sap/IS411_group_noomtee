import { CURRENT_USER_ID } from '#lib/config.js';
import { getCatalog, getListsData } from '#lib/server/data.js';

// หน้า Lists = เลือกดู list สถานที่ของคนอื่น (การค้นหา/กรองทำในหน้าเว็บ)
export async function load({ fetch }) {
	const catalog = await getCatalog(fetch);
	const { others } = await getListsData(fetch, CURRENT_USER_ID, catalog);

	return {
		lists: others,
		// "Popular this week" = list ที่คน save เยอะที่สุด
		popular: [...others].sort((a, b) => b.saves - a.saves).slice(0, 4),
		vibes: catalog.vibes
	};
}
