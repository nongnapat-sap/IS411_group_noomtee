<script>
	import PlaceCard from '#lib/PlaceCard.svelte';
	import ListCard from '#lib/ListCard.svelte';

	let { data, form } = $props();

	let showFollowing = $state(false);
	let imgFailed = $state(false);
	let copied = $state(false);

	const initial = $derived(data.user.name?.trim()?.[0]?.toUpperCase() ?? '?');
	const stars = (n) => {
		const r = Math.max(0, Math.min(5, Number(n) || 0));
		return '★'.repeat(r) + '☆'.repeat(5 - r);
	};

	async function share() {
		try {
			await navigator.clipboard.writeText(location.href);
			copied = true;
			setTimeout(() => (copied = false), 1500);
		} catch {
			/* clipboard ใช้ไม่ได้ (เช่น http) — ข้ามไปเฉย ๆ */
		}
	}

	// ---------- ฟอร์ม journal (ใช้ทั้งเพิ่มและแก้ไข) ----------
	const emptyJournal = { id: '', place_id: '', title: '', rating: 5, note: '', visited_at: '' };
	let isModalOpen = $state(false);
	let isEditMode = $state(false);
	let journalForm = $state({ ...emptyJournal });

	function openAddModal() {
		isEditMode = false;
		journalForm = { ...emptyJournal };
		isModalOpen = true;
	}

	function openEditModal(entry) {
		isEditMode = true;
		journalForm = {
			id: entry.id,
			place_id: entry.place_id,
			title: entry.title ?? '',
			rating: entry.rating,
			note: entry.note ?? '',
			// input type="date" ต้องการรูปแบบ YYYY-MM-DD
			visited_at: entry.visited_at ? entry.visited_at.slice(0, 10) : ''
		};
		isModalOpen = true;
	}

	function closeModal() {
		isModalOpen = false;
	}
</script>

{#if form?.message}
	<div class="notification is-danger is-light">{form.message}</div>
{/if}

<!-- ---------- โปรไฟล์ ---------- -->
<section class="profile stack">
	<div class="avatar" aria-hidden="true">
		{#if data.user.profile_image_url && !imgFailed}
			<img src={data.user.profile_image_url} alt="" onerror={() => (imgFailed = true)} />
		{:else}
			{initial}
		{/if}
	</div>
	<div class="who">
		<h1 class="page-title">{data.user.name}</h1>
		<p class="page-desc">Your favorite places, the journal of places you visited, and the collections you made or saved.</p>
		<p class="follow-line">
			<span><strong>{data.followerCount}</strong> followers</span>
			<span aria-hidden="true">•</span>
			<button
				class="following-btn"
				aria-expanded={showFollowing}
				aria-controls="following-panel"
				onclick={() => (showFollowing = !showFollowing)}
			>
				<strong>{data.following.length}</strong> following {showFollowing ? '▴' : '▾'}
			</button>
		</p>
		{#if data.user.nationality}
			<p class="meta">{data.user.nationality}{data.user.preferred_language ? ` · ${data.user.preferred_language}` : ''}</p>
		{/if}
		<div class="buttons">
			<button class="button share" onclick={share}>{copied ? 'Link copied ✓' : 'Share profile'}</button>
		</div>
	</div>
</section>

{#if showFollowing}
	<section id="following-panel" class="following stack" aria-label="People you follow">
		<p class="eyebrow">Following</p>
		{#if data.following.length}
			<ul>
				{#each data.following as person (person.user_id)}
					<li>
						<span class="mini-avatar" aria-hidden="true">{person.name[0].toUpperCase()}</span>
						<span class="pname">{person.name}</span>
						{#if person.nationality}<span class="pmeta">{person.nationality}</span>{/if}
					</li>
				{/each}
			</ul>
		{:else}
			<p class="empty">Not following anyone yet.</p>
		{/if}
	</section>
{/if}

<!-- ---------- Favourite place ---------- -->
<section class="stack">
	<div class="section-head">
		<div>
			<p class="eyebrow">Saved for yourself</p>
			<h2>Favourite places</h2>
		</div>
	</div>
	{#if data.favoritePlaces.length}
		<div class="columns is-multiline">
			{#each data.favoritePlaces as place (place.place_id)}
				<div class="column is-3-desktop is-6-tablet">
					<PlaceCard {place} />
				</div>
			{/each}
		</div>
	{:else}
		<p class="empty">No favourites yet. Add places from the Explore page.</p>
	{/if}
</section>

<!-- ---------- my Journal ---------- -->
<section class="stack">
	<div class="section-head">
		<div>
			<p class="eyebrow">Places you've been</p>
			<h2>My journal</h2>
		</div>
		<button class="button add" onclick={openAddModal}>+ Write a Journal Entry</button>
	</div>
	{#if data.journals.length}
		<ol class="journal">
			{#each data.journals as entry, i (entry.id)}
				<li>
					<span class="num">#{i + 1}</span>
					<div class="body">
						<p class="place">{entry.place_name}</p>
						{#if entry.title}<h3>{entry.title}</h3>{/if}
						<p class="stars" aria-label={`${entry.rating} out of 5`}>{stars(entry.rating)}</p>
						{#if entry.note}<p class="note">{entry.note}</p>{/if}
						{#if entry.visited}<p class="date">Visited {entry.visited}</p>{/if}
						<div class="buttons mt-3">
							<button class="button is-small is-dark" onclick={() => openEditModal(entry)}>Edit</button>
							<form method="POST" action="?/deleteJournal">
								<input type="hidden" name="id" value={entry.id} />
								<button class="button is-small is-danger is-outlined">Delete</button>
							</form>
						</div>
					</div>
				</li>
			{/each}
		</ol>
	{:else}
		<p class="empty">Your journal is empty. Write about the places you've visited.</p>
	{/if}
</section>

<!-- ---------- my list ---------- -->
<section class="stack">
	<div class="section-head">
		<div>
			<p class="eyebrow">Collections you created</p>
			<h2>My Collections</h2>
		</div>
	</div>
	{#if data.myLists.length}
		<ol class="mylists">
			{#each data.myLists as list, i (list.list_id)}
				<li>
					<span class="num">#{i + 1}</span>
					<div>
						<h3>{list.title}</h3>
						<p class="meta">
							{list.place_count}
							{list.place_count === 1 ? 'place' : 'places'} · {list.saves} saves
						</p>
					</div>
				</li>
			{/each}
		</ol>
	{:else}
		<p class="empty">You haven't created a collection yet.</p>
	{/if}
</section>

<!-- ---------- saved list ---------- -->
<section class="stack">
	<div class="section-head">
		<div>
			<p class="eyebrow">Collections you saved from others</p>
			<h2>Saved Collections</h2>
		</div>
	</div>
	{#if data.savedLists.length}
		<div class="columns is-multiline">
			{#each data.savedLists as list (list.list_id)}
				<div class="column is-3-desktop is-6-tablet">
					<ListCard {list} />
				</div>
			{/each}
		</div>
	{:else}
		<p class="empty">Collections you save on the Collections page will show up here.</p>
	{/if}
</section>

<!-- ---------- Modal เพิ่ม/แก้ไข journal ---------- -->
{#if isModalOpen}
	<div class="modal is-active">
		<div class="modal-background" onclick={closeModal} role="button" tabindex="0" onkeypress={closeModal}></div>
		<div class="modal-card">
			<header class="modal-card-head dark">
				<p class="modal-card-title has-text-white">{isEditMode ? 'Edit journal' : 'Write a Journal Entry'}</p>
				<button class="delete" aria-label="close" onclick={closeModal}></button>
			</header>

			<section class="modal-card-body darker">
				<form method="POST" action={isEditMode ? '?/updateJournal' : '?/createJournal'}>
					{#if isEditMode}
						<input type="hidden" name="id" value={journalForm.id} />
					{/if}

					<div class="field">
						<label class="label has-text-grey-light" for="j-place">Place</label>
						<div class="select is-fullwidth">
							<select id="j-place" name="place_id" bind:value={journalForm.place_id} required>
								<option value="" disabled>Select a place...</option>
								{#each data.places as place (place.place_id)}
									<option value={place.place_id}>{place.place_name}</option>
								{/each}
							</select>
						</div>
					</div>

					<div class="field">
						<label class="label has-text-grey-light" for="j-title">Title</label>
						<input id="j-title" class="input" name="title" bind:value={journalForm.title} required />
					</div>

					<div class="field">
						<label class="label has-text-grey-light" for="j-rating">Rating</label>
						<div class="select is-fullwidth">
							<select id="j-rating" name="rating" bind:value={journalForm.rating}>
								{#each [5, 4, 3, 2, 1] as r}
									<option value={r}>{stars(r)}</option>
								{/each}
							</select>
						</div>
					</div>

					<div class="field">
						<label class="label has-text-grey-light" for="j-date">Visited on</label>
						<input id="j-date" class="input" type="date" name="visited_at" bind:value={journalForm.visited_at} />
					</div>

					<div class="field">
						<label class="label has-text-grey-light" for="j-note">Note</label>
						<textarea id="j-note" class="textarea" name="note" bind:value={journalForm.note}></textarea>
					</div>

					<div class="buttons is-right mt-5">
						<button type="button" class="button is-dark" onclick={closeModal}>Cancel</button>
						<button type="submit" class="button add">{isEditMode ? 'Save changes' : 'Save Entry'}</button>
					</div>
				</form>
			</section>
		</div>
	</div>
{/if}

<style>
	.add {
		background: var(--lime);
		border-color: var(--lime);
		color: #000;
		font-weight: 700;
	}
	.dark {
		background: #1a1a1a;
		border-bottom: 1px solid #333;
	}
	.darker {
		background: #222;
	}
	.darker .input,
	.darker .textarea,
	.darker select {
		background: #111;
		border-color: #444;
		color: #fff;
	}
	.profile {
		display: flex;
		align-items: center;
		gap: 1.5rem;
		flex-wrap: wrap;
	}
	.avatar {
		display: grid;
		place-items: center;
		width: 112px;
		height: 112px;
		border-radius: 50%;
		overflow: hidden;
		background: #6b0f8a;
		color: #fff;
		font-size: 2.8rem;
		font-weight: 800;
	}
	.avatar img {
		width: 100%;
		height: 100%;
		object-fit: cover;
	}
	.follow-line {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		margin: 0.4rem 0;
		color: #cfcfcf;
		font-size: 0.9rem;
	}
	.follow-line strong {
		color: #fff;
	}
	.following-btn {
		padding: 0;
		border: 0;
		background: none;
		color: #cfcfcf;
		font: inherit;
		cursor: pointer;
	}
	.following-btn:hover {
		color: var(--lime);
	}
	.meta {
		color: var(--muted);
		font-size: 0.8rem;
	}
	.share {
		margin-top: 0.6rem;
		background: transparent;
		border-color: var(--line);
		border-radius: 999px;
		color: #fff;
		font-size: 0.8rem;
		font-weight: 600;
	}
	.share:hover {
		border-color: var(--lime);
		color: var(--lime);
	}

	.following {
		padding: 1rem 1.25rem;
		border: 1px solid var(--line);
		border-radius: 12px;
		background: var(--card);
	}
	.following ul {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
		gap: 0.75rem;
		margin-top: 0.75rem;
	}
	.following li {
		display: flex;
		align-items: center;
		gap: 0.6rem;
	}
	.mini-avatar {
		display: grid;
		place-items: center;
		flex: none;
		width: 32px;
		height: 32px;
		border-radius: 50%;
		background: #6b0f8a;
		color: #fff;
		font-size: 0.8rem;
		font-weight: 700;
	}
	.pname {
		color: #fff;
		font-size: 0.85rem;
		font-weight: 600;
	}
	.pmeta {
		color: var(--muted);
		font-size: 0.7rem;
	}

	.journal,
	.mylists {
		display: grid;
		gap: 0.75rem;
	}
	.journal li,
	.mylists li {
		display: flex;
		gap: 1rem;
		padding: 1rem 1.25rem;
		border: 1px solid var(--line);
		border-radius: 12px;
		background: var(--card);
	}
	.num {
		flex: none;
		min-width: 2rem;
		color: var(--lime);
		font-weight: 800;
	}
	.place {
		color: var(--lime);
		font-size: 0.7rem;
		font-weight: 700;
		letter-spacing: 0.12em;
		text-transform: uppercase;
	}
	h3 {
		color: #fff;
		font-size: 1rem;
		font-weight: 700;
	}
	.stars {
		color: var(--lime);
		letter-spacing: 0.1em;
		font-size: 0.85rem;
	}
	.note {
		margin-top: 0.3rem;
		color: #cfcfcf;
		font-size: 0.85rem;
	}
	.date {
		margin-top: 0.4rem;
		color: var(--muted);
		font-size: 0.75rem;
	}
</style>