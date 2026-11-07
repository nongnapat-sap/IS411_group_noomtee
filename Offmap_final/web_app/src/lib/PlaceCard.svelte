<script>
	// place: PlaceOut จาก backend (ถ้าผ่าน decoratePlaces จะมี area_name และ vibes มาด้วย)
	let { place, areaName = undefined, vibes = undefined } = $props();

	const area = $derived(areaName ?? place.area_name ?? 'Unknown area');
	const tags = $derived(vibes ?? place.vibes ?? []);
</script>

<article class="card place">
	<p class="eyebrow">{area}</p>
	<h3 class="name">{place.place_name}</h3>
	<p class="address">{place.address}</p>
	<p class="desc">{place.description}</p>
	<p class="hours">🕒 {place.opening_time} – {place.closing_time}</p>

	<div class="tags">
		{#if place.price_level}
			<span class="tag price">{place.price_level}</span>
		{:else}
			<span class="tag is-dark has-text-grey">No price data</span>
		{/if}
		{#each tags as v (v)}
			<span class="tag vibe">{v}</span>
		{/each}
	</div>
</article>

<style>
	.place {
		height: 100%;
		padding: 1.25rem;
		background: var(--card);
		border: 1px solid var(--line);
		border-radius: 12px;
		color: #fff;
		transition: border-color 0.15s, transform 0.15s;
	}
	.place:hover {
		border-color: var(--lime);
		transform: translateY(-2px);
	}
	.eyebrow {
		margin-bottom: 0.25rem;
	}
	.name {
		color: #fff;
		font-size: 1.15rem;
		font-weight: 700;
		line-height: 1.25;
		margin-bottom: 0.25rem;
	}
	.address {
		color: var(--muted);
		font-size: 0.75rem;
		margin-bottom: 0.75rem;
	}
	.desc {
		color: #cfcfcf;
		font-size: 0.85rem;
		margin-bottom: 0.5rem;
	}
	.hours {
		color: var(--muted);
		font-size: 0.8rem;
		margin-bottom: 0.75rem;
	}
	.tags {
		display: flex;
		flex-wrap: wrap;
		gap: 0.4rem;
	}
	.price {
		background: var(--lime);
		color: #000;
		font-weight: 700;
	}
	.vibe {
		background: transparent;
		border: 1px solid var(--line);
		color: #cfcfcf;
	}
</style>