import { CURRENT_USER_ID } from '#lib/config.js';
import { getCatalog, getListsData } from '#lib/server/data.js';
import { saveActions } from '#lib/server/actions.js';

// หน้า Collections = เลือกดู collection สถานที่ของคนอื่น (ใน database คือตาราง lists)
// การค้นหาและกรอง vibe ทำในหน้าเว็บ (+page.svelte)
export async function load({ fetch }) {
	const catalog = await getCatalog(fetch);
	const { others, savedIdOf } = await getListsData(fetch, CURRENT_USER_ID, catalog);

	return {
		lists: others,
		// "Popular this week" = collection ที่คน save เยอะที่สุด
		popular: [...others].sort((a, b) => b.saves - a.saves).slice(0, 4),
		vibes: catalog.vibes,
		savedIdOf // list_id → saved_list_id ใช้บอกว่า collection ไหน save ไว้แล้ว
	};
}

// saveList (CREATE) และ unsaveList (DELETE = UPDATE is_deleted)
// โค้ดอยู่ใน src/lib/server/actions.js เพราะหน้ารายละเอียด collection ใช้ร่วมกัน
export const actions = {
	...saveActions
};
