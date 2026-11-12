<script>
	import PlaceCard from '#lib/PlaceCard.svelte';

	let { data } = $props();

	let imgFailed = $state(false);
	const hue = $derived((data.area.area_id * 47) % 360);
</script>

<a class="back" href="/areas">← All areas</a>

<section class="hero stack" style="--h: {hue}">
	{#if data.area.cover_image_url && !imgFailed}
		<img src={data.area.cover_image_url} alt="" onerror={() => (imgFailed = true)} />
	{/if}
	<div class="shade"></div>
	<div class="hero-text">
		<p class="eyebrow">{data.area.district} · {data.places.length} {data.places.length === 1 ? 'place' : 'places'}</p>
		<h1 class="page-title">{data.area.area_name}</h1>
		{#if data.area.description}<p class="lead">{data.area.description}</p>{/if}
	</div>
</section>

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

<style>
	.back {
		display: inline-block;
		margin-bottom: 1rem;
		color: var(--lime);
		font-size: 0.85rem;
		font-weight: 700;
	}
	.hero {
		position: relative;
		min-height: 260px;
		display: flex;
		align-items: flex-end;
		overflow: hidden;
		border: 1px solid var(--line);
		border-radius: 16px;
		background: linear-gradient(135deg, hsl(var(--h) 70% 30%), hsl(var(--h) 60% 10%));
	}
	.hero img {
		position: absolute;
		inset: 0;
		width: 100%;
		height: 100%;
		object-fit: cover;
	}
	.shade {
		position: absolute;
		inset: 0;
		background: linear-gradient(180deg, rgba(0, 0, 0, 0.05), rgba(0, 0, 0, 0.85));
	}
	.hero-text {
		position: relative;
		padding: 1.75rem;
	}
	.lead {
		margin-top: 0.5rem;
		color: #e2e2e2;
		max-width: 40rem;
	}
</style>
