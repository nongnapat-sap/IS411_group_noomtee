<script>
	import AreaCard from '#lib/AreaCard.svelte';

	let { data } = $props();
</script>

<div class="stack">
	<p class="eyebrow">Areas</p>
	<h1 class="page-title">Neighbourhoods of Bangkok</h1>
<p class="page-desc">
	Pick a neighbourhood to see every place in that area.
</p>
</div>

{#if data.areas.length}
	<div class="columns is-multiline">
		{#each data.areas as area (area.area_id)}
			<div class="column is-3-desktop is-6-tablet">
				<AreaCard {area} />
			</div>
		{/each}
	</div>
{:else}
	<p class="empty">No areas yet.</p>
{/if}
