import { CURRENT_USER_ID } from '$lib/config.js';
import { getCatalog, getUserData, getListsData, getFollowData } from '$lib/server/data.js';

export async function load({ fetch }) {
	const catalog = await getCatalog(fetch);

	// จาก backend: โปรไฟล์ + favorites + journals
	const profile = await getUserData(fetch, CURRENT_USER_ID, catalog);
	// ยังไม่มีใน backend: my list / saved list / follow (อ่านจาก mock ผ่าน data.js)
	const { mine, saved } = getListsData(CURRENT_USER_ID);
	const { following, followerCount } = getFollowData(CURRENT_USER_ID);

	return {
		user: profile.user,
		favoritePlaces: profile.favoritePlaces,
		journals: profile.journals,
		myLists: mine,
		savedLists: saved,
		following,
		followerCount,
		offline: profile.offline
	};
}