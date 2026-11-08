<script>
	import PlaceCard from '#lib/PlaceCard.svelte';

	let { data } = $props();
</script>

<div class="stack">
	<p class="eyebrow">{data.area.district}</p>
	<h1 class="page-title">{data.area.area_name}</h1>
	{#if data.area.description}
		<p class="has-text-grey-light mt-2">{data.area.description}</p>
	{/if}
	<a class="see-all" href="/areas">← All areas</a>
</div>

{#if data.places.length}
	<div class="columns is-multiline">
		{#each data.places as place (place.place_id)}
			<div class="column is-4-desktop is-6-tablet">
				<PlaceCard {place} />
			</div>
		{/each}
	</div>
{:else}
	<p class="empty">No places in this area yet.</p>
{/if}