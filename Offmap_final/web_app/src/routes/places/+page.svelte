<script>
	import PlaceCard from '$lib/PlaceCard.svelte';
	import OfflineNote from '$lib/OfflineNote.svelte';

	let { data } = $props();

	// ตัวแปร Reactive State สำหรับค้นหาและฟิลเตอร์
	let searchQuery = $state('');
	let selectedArea = $state('all');
	let selectedVibe = $state('all');

	// ดึงรายชื่อ Area แบบไม่ซ้ำจาก data.places หรือ data.areas
	let areasList = $derived(() => {
		if (data.areas && data.areas.length) return data.areas;
		const uniqueMap = new Map();
		for (const p of data.places) {
			const id = p.area_id || p.area_name || p.area;
			const name = p.area_name || p.area;
			if (id && name && !uniqueMap.has(id)) {
				uniqueMap.set(id, { id, name });
			}
		}
		return Array.from(uniqueMap.values());
	});

	// ระบบกรองข้อมูลสถานที่ (Real-time Filtering)
	let filteredPlaces = $derived(
		data.places.filter((place) => {
			const name = (place.place_name || place.name || '').toLowerCase();
			const areaName = (place.area_name || place.area || '').toLowerCase();
			const vibeName = (place.vibe_name || place.vibe || '').toLowerCase();
			const q = searchQuery.toLowerCase().trim();

			// 1. กรองด้วย Search Bar (ค้นหาชื่อร้าน, ย่าน หรือ Vibe)
			const matchesSearch = !q || name.includes(q) || areaName.includes(q) || vibeName.includes(q);

			// 2. กรองตาม Area
			const matchesArea =
				selectedArea === 'all' ||
				String(place.area_id) === String(selectedArea) ||
				place.area_name === selectedArea ||
				place.area === selectedArea;

			// 3. กรองตาม Vibe
			const matchesVibe =
				selectedVibe === 'all' ||
				String(place.vibe_id) === String(selectedVibe) ||
				place.vibe_name === selectedVibe;

			return matchesSearch && matchesArea && matchesVibe;
		})
	);
</script>

<div class="stack">
	<p class="eyebrow">Explore</p>

	<!-- แก้หัวข้อตามที่ต้องการ -->
	<h1 class="page-title">Find places</h1>
</div>

<OfflineNote show={data.offline} />

<div class="filter-controls stack">
	<!-- 1. Search Bar (ค้นหา Place / Area / Vibe) -->
	<div class="search-box">
		<input
			type="text"
			bind:value={searchQuery}
			placeholder="Search places, areas, or vibes..."
			class="search-input"
		/>
	</div>

	<!-- 2. Dropdown Filters (แยกตาม Area และ Vibe) -->
	<div class="dropdown-group">
		<!-- Area Filter -->
		<select bind:value={selectedArea} class="filter-select">
			<option value="all">All Areas</option>
			{#each areasList() as area}
				<option value={area.id}>{area.name}</option>
			{/each}
		</select>

		<!-- Vibe Filter -->
		<select bind:value={selectedVibe} class="filter-select">
			<option value="all">All Vibes</option>
			{#each data.vibes as vibe (vibe.vibe_id)}
				<option value={vibe.vibe_id}>{vibe.vibe_name}</option>
			{/each}
		</select>
	</div>
</div>

{#if filteredPlaces.length}
	<p class="count">{filteredPlaces.length} {filteredPlaces.length === 1 ? 'place' : 'places'}</p>
	<div class="columns is-multiline">
		{#each filteredPlaces as place (place.place_id)}
			<div class="column is-4-desktop is-6-tablet">
				<PlaceCard {place} />
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
		margin-bottom: 1.5rem;
	}

	.search-input {
		width: 100%;
		padding: 0.75rem 1rem;
		background-color: #18181b;
		border: 1px solid #27272a;
		border-radius: 8px;
		color: #ffffff;
		font-size: 0.95rem;
		outline: none;
		transition: border-color 0.2s;
	}

	.search-input:focus {
		border-color: var(--lime, #a3e635);
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
		color: #ffffff;
		padding: 0.6rem 1rem;
		font-size: 0.9rem;
		outline: none;
		cursor: pointer;
		transition: border-color 0.2s;
	}

	.filter-select:focus {
		border-color: var(--lime, #a3e635);
	}

	.count {
		margin-bottom: 0.75rem;
		color: var(--muted, #a1a1aa);
		font-size: 0.8rem;
	}

	.empty {
		color: var(--muted, #a1a1aa);
		padding: 2rem 0;
	}
</style>