<script>
	import PlaceCard from '#lib/PlaceCard.svelte';

	let { data, form } = $props();

	// ค่าที่ผู้ใช้เลือก (ผูกกับ input ด้วย bind:value)
	let searchQuery = $state('');
	let selectedArea = $state('all');
	let selectedVibe = $state('all');

	// กรองสถานที่ใหม่ทุกครั้งที่ค่าใดค่าหนึ่งเปลี่ยน
	let filteredPlaces = $derived(
		data.places.filter((place) => {
			const q = searchQuery.toLowerCase().trim();
			const matchesSearch =
				!q ||
				place.place_name.toLowerCase().includes(q) ||
				(place.area_name ?? '').toLowerCase().includes(q) ||
				place.vibes.some((v) => v.toLowerCase().includes(q));
			const matchesArea = selectedArea === 'all' || place.area_id === selectedArea;
			const matchesVibe = selectedVibe === 'all' || place.vibes.includes(selectedVibe);
			return matchesSearch && matchesArea && matchesVibe;
		})
	);
</script>

<div class="stack">
	<p class="eyebrow">Explore</p>
	<h1 class="page-title">Find places</h1>
<p class="page-desc">
	Search and filter places by area or vibe. Tap "Add to Favorites" on any place to keep it in your profile.
</p>
</div>

{#if form?.message}
	<div class="notification is-danger is-light">{form.message}</div>
{/if}

<div class="filter-controls stack">
	<input
		type="text"
		bind:value={searchQuery}
		placeholder="Search places, areas, or vibes..."
		class="search-input"
	/>

	<div class="dropdown-group">
		<select bind:value={selectedArea} class="filter-select">
			<option value="all">All Areas</option>
			{#each data.areas as area (area.area_id)}
				<option value={area.area_id}>{area.area_name}</option>
			{/each}
		</select>

		<select bind:value={selectedVibe} class="filter-select">
			<option value="all">All Vibes</option>
			{#each data.vibes as vibe (vibe.vibe_id)}
				<option value={vibe.vibe_name}>{vibe.vibe_name}</option>
			{/each}
		</select>
	</div>
</div>

{#if filteredPlaces.length}
	<p class="count">{filteredPlaces.length} {filteredPlaces.length === 1 ? 'place' : 'places'}</p>
	<div class="columns is-multiline">
		{#each filteredPlaces as place (place.place_id)}
			<div class="column is-4-desktop is-6-tablet with-action">
				<div class="grow"><PlaceCard {place} /></div>

				<!-- ปุ่ม favorite: ถ้ากดไว้แล้ว → removeFavorite, ถ้ายัง → addFavorite -->
				{#if data.favoriteIdOf[place.place_id]}
					<form method="POST" action="?/removeFavorite" class="fav-form">
						<input type="hidden" name="favorite_id" value={data.favoriteIdOf[place.place_id]} />
						<button class="fav-btn saved">✕ Remove from Favorites</button>
					</form>
				{:else}
					<form method="POST" action="?/addFavorite" class="fav-form">
						<input type="hidden" name="place_id" value={place.place_id} />
						<button class="fav-btn">♡ Add to Favorites</button>
					</form>
				{/if}
			</div>
		{/each}
	</div>
{:else}
	<p class="empty">No places match your search criteria. Try adjusting your filters.</p>
{/if}

<style>
	.filter-controls {
		display: flex;
		flex-direction: column;
		gap: 0.9rem;
	}
	.search-input {
		width: 100%;
		padding: 0.75rem 1rem;
		background-color: #18181b;
		border: 1px solid #27272a;
		border-radius: 8px;
		color: #fff;
		font-size: 0.95rem;
		outline: none;
		transition: border-color 0.2s;
	}
	.search-input:focus {
		border-color: var(--lime);
	}
	.dropdown-group {
		display: flex;
		gap: 0.75rem;
		flex-wrap: wrap;
	}
	.filter-select {
		background-color: #18181b;
		border: 1px solid #27272a;
		border-radius: 8px;
		color: #fff;
		padding: 0.6rem 1rem;
		font-size: 0.9rem;
		outline: none;
		cursor: pointer;
	}
	.filter-select:focus {
		border-color: var(--lime);
	}
	/* ให้การ์ดยืดเต็มความสูง แล้วปุ่มอยู่ใต้การ์ดพอดี */
	.with-action {
		display: flex;
		flex-direction: column;
	}
	.grow {
		flex: 1;
	}
	.fav-form {
		margin-top: 0.5rem;
	}
	.fav-btn {
		width: 100%;
		padding: 0.45rem;
		border: 1px solid var(--line);
		border-radius: 8px;
		background: transparent;
		color: #d6d6d6;
		font: inherit;
		font-size: 0.8rem;
		font-weight: 600;
		cursor: pointer;
	}
	.fav-btn:hover {
		border-color: var(--lime);
		color: #fff;
	}
	.fav-btn.saved {
		background: var(--lime);
		border-color: var(--lime);
		color: #000;
	}
	.count {
		margin-bottom: 0.75rem;
		color: var(--muted);
		font-size: 0.8rem;
	}
</style>
