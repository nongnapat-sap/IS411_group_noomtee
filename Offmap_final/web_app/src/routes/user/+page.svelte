<script>
	import PlaceCard from '$lib/PlaceCard.svelte';
	import ListCard from '$lib/ListCard.svelte';
	import OfflineNote from '$lib/OfflineNote.svelte';

	let { data } = $props();

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
</script>

<OfflineNote show={data.offline} />

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
		<p class="empty">No favourites yet. Heart a place while exploring.</p>
	{/if}
</section>

<!-- ---------- my Journal ---------- -->
<section class="stack">
	<div class="section-head">
		<div>
			<p class="eyebrow">Places you've been</p>
			<h2>My journal</h2>
		</div>
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
			<p class="eyebrow">Like a playlist, but for places</p>
			<h2>My lists</h2>
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
		<p class="empty">You haven't made a list yet.</p>
	{/if}
</section>

<!-- ---------- saved list ---------- -->
<section class="stack">
	<div class="section-head">
		<div>
			<p class="eyebrow">From other people</p>
			<h2>Saved lists</h2>
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
		<p class="empty">Lists you save from others will show up here.</p>
	{/if}
</section>

<style>
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