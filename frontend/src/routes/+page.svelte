<script>
	import PlaceCard from '#lib/PlaceCard.svelte';
	import AreaCard from '#lib/AreaCard.svelte';

	let { data } = $props();
</script>

<section class="hero">
	<p class="eyebrow">Bangkok / Thailand — a field guide to the unlisted</p>
	<h1>
		Discover Bangkok
		<mark>beyond the obvious.</mark>
	</h1>
	<p class="sub">
		Find places that match your vibe, not just your location. Bars behind unmarked doors, cafés in
		shophouses, noodle soup under neon — the city your local friend would take you to.
	</p>
	<div class="buttons">
		<a class="button cta" href="/places">Explore places</a>
		<a class="button ghost" href="/lists">Browse lists</a>
	</div>
</section>


<section class="stack">
	<div class="section-head">
		<div>
			<p class="eyebrow">Recommend this week</p>
			<h2>Places</h2>
		</div>
		<a class="see-all" href="/places">See all →</a>
	</div>
	{#if data.places.length}
		<div class="columns is-multiline">
			{#each data.places as place (place.place_id)}
				<div class="column is-3-desktop is-6-tablet">
					<PlaceCard {place} />
				</div>
			{/each}
		</div>
	{:else}
		<p class="empty">No places yet.</p>
	{/if}
</section>


<section class="stack">
	<div class="section-head">
		<div>
			<p class="eyebrow">Recommend this week</p>
			<h2>Areas</h2>
		</div>
		<a class="see-all" href="/areas">See all →</a>
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
</section>

<style>
	.hero {
		position: relative;
		margin-bottom: 3rem;
		padding: clamp(2rem, 6vw, 4.5rem) clamp(1.25rem, 4vw, 3rem);
		border: 1px solid var(--line);
		border-radius: 16px;
		overflow: hidden;
		background:
			radial-gradient(ellipse at 85% 20%, rgba(204, 255, 0, 0.14), transparent 55%),
			radial-gradient(ellipse at 10% 100%, rgba(255, 120, 40, 0.16), transparent 55%),
			linear-gradient(180deg, #0c0c0c, #050505);
	}
	h1 {
		margin: 0.6rem 0 1.2rem;
		color: #fff;
		font-size: clamp(2.2rem, 7vw, 4.6rem);
		font-weight: 800;
		letter-spacing: -0.03em;
		line-height: 1.02;
	}
	mark {
		display: inline-block;
		margin-top: 0.3rem;
		padding: 0 0.3em;
		background: var(--lime);
		color: #000;
	}
	.sub {
		max-width: 34rem;
		margin-bottom: 1.75rem;
		color: #b8b8b8;
		font-size: 0.95rem;
		line-height: 1.6;
	}
	.cta {
		background: var(--lime);
		border-color: var(--lime);
		color: #000;
		font-weight: 700;
	}
	.cta:hover {
		background: #b8e600;
		color: #000;
	}
	.ghost {
		background: transparent;
		border-color: var(--line);
		color: #fff;
		font-weight: 600;
	}
	.ghost:hover {
		border-color: var(--lime);
		color: var(--lime);
	}
</style>