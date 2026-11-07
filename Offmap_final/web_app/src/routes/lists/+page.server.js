import { CURRENT_USER_ID } from '$lib/config.js';
import { getCatalog, getListsData } from '$lib/server/data.js';

// หน้า Lists = ค้นหา/เลือกดู "list สถานที่" ของคนอื่น (แบบหน้า search ของ Spotify)
// ?q=คำค้น  ?vibe=id
export async function load({ fetch, url }) {
	const q = (url.searchParams.get('q') ?? '').trim();
	const vibeId = Number(url.searchParams.get('vibe')) || null;

	const catalog = await getCatalog(fetch); // ใช้แค่ชื่อ vibe
	const { others } = getListsData(CURRENT_USER_ID);

	const vibeName = new Map(catalog.vibes.map((v) => [v.vibe_id, v.vibe_name]));
	const decorated = others.map((l) => ({ ...l, vibe_name: vibeName.get(l.vibe_id) ?? null }));

	const needle = q.toLowerCase();
	const matches = decorated.filter(
		(l) =>
			(!vibeId || l.vibe_id === vibeId) &&
			(!needle ||
				l.title.toLowerCase().includes(needle) ||
				l.owner_name.toLowerCase().includes(needle) ||
				(l.description ?? '').toLowerCase().includes(needle))
	);

	return {
		q,
		activeVibe: vibeId,
		vibes: catalog.vibes,
		searching: Boolean(q || vibeId),
		results: matches,
		// "Popular this week" = list ที่คน save เยอะที่สุด
		popular: [...decorated].sort((a, b) => b.saves - a.saves).slice(0, 4),
		all: decorated,
		offline: catalog.offline
	};
}