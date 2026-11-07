<script>
	import ListCard from '$lib/ListCard.svelte';
	import OfflineNote from '$lib/OfflineNote.svelte';

	let { data } = $props();

	// ชิปเปลี่ยน vibe โดยคงคำค้นไว้
	const hrefFor = (vibeId) => {
		const params = new URLSearchParams();
		if (data.q) params.set('q', data.q);
		if (vibeId) params.set('vibe', String(vibeId));
		const qs = params.toString();
		return qs ? `?${qs}` : '/lists';
	};
</script>

<div class="stack">
	<p class="eyebrow">Lists</p>
	<h1 class="page-title">Lists from other people</h1>
</div>

<OfflineNote show={data.offline} />

<form class="search stack" method="GET" action="/lists" role="search">
	{#if data.activeVibe}<input type="hidden" name="vibe" value={data.activeVibe} />{/if}
	<input
		class="input"
		type="search"
		name="q"
		value={data.q}
		placeholder="Search lists, people or vibes…"
		aria-label="Search lists"
	/>
	<button class="button go" type="submit">Search</button>
	{#if data.q}
		<a class="button clear" href={hrefFor(data.activeVibe)}>Clear</a>
	{/if}
</form>

<div class="chips stack" role="group" aria-label="Filter lists by vibe">
	<a class="chip" class:active={!data.activeVibe} href={hrefFor(null)}>All</a>
	{#each data.vibes as vibe (vibe.vibe_id)}
		<a class="chip" class:active={data.activeVibe === vibe.vibe_id} href={hrefFor(vibe.vibe_id)}>
			{vibe.vibe_name}
		</a>
	{/each}
</div>

{#if data.searching}
	<section class="stack">
		<div class="section-head">
			<h2>Results</h2>
			<span class="muted">{data.results.length} found</span>
		</div>
		{#if data.results.length}
			<div class="columns is-multiline">
				{#each data.results as list (list.list_id)}
					<div class="column is-3-desktop is-6-tablet">
						<ListCard {list} vibeName={list.vibe_name} />
					</div>
				{/each}
			</div>
		{:else}
			<p class="empty">No lists found. Try a different search.</p>
		{/if}
	</section>
{:else}
	<section class="stack">
		<div class="section-head">
			<div>
				<p class="eyebrow">Most saved</p>
				<h2>Popular this week</h2>
			</div>
		</div>
		<div class="columns is-multiline">
			{#each data.popular as list (list.list_id)}
				<div class="column is-3-desktop is-6-tablet">
					<ListCard {list} vibeName={list.vibe_name} />
				</div>
			{/each}
		</div>
	</section>

	<section class="stack">
		<div class="section-head">
			<h2>All lists</h2>
		</div>
		<div class="columns is-multiline">
			{#each data.all as list (list.list_id)}
				<div class="column is-3-desktop is-6-tablet">
					<ListCard {list} vibeName={list.vibe_name} />
				</div>
			{/each}
		</div>
	</section>
{/if}

<style>
	.search {
		display: flex;
		gap: 0.5rem;
		max-width: 36rem;
	}
	.search :global(.input) {
		background: var(--card);
		border-color: var(--line);
		color: #fff;
		border-radius: 999px;
		padding-inline: 1.1rem;
	}
	.search :global(.input:focus) {
		border-color: var(--lime);
		box-shadow: 0 0 0 2px rgba(204, 255, 0, 0.2);
	}
	.go {
		background: var(--lime);
		border-color: var(--lime);
		color: #000;
		font-weight: 700;
		border-radius: 999px;
	}
	.clear {
		background: transparent;
		border-color: var(--line);
		color: #fff;
		border-radius: 999px;
	}
	.muted {
		color: var(--muted);
		font-size: 0.8rem;
	}
</style>