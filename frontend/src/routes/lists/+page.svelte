<script>
	import ListCard from '#lib/ListCard.svelte';
	import SaveButton from '#lib/SaveButton.svelte';

	let { data, form } = $props();

	let q = $state('');
	let activeVibe = $state(null);

	let searching = $derived(q.trim() !== '' || activeVibe !== null);

	let results = $derived(
		data.lists.filter((l) => {
			const needle = q.toLowerCase().trim();
			const matchesText =
				!needle ||
				l.title.toLowerCase().includes(needle) ||
				l.owner_name.toLowerCase().includes(needle) ||
				(l.description ?? '').toLowerCase().includes(needle);
			const matchesVibe = activeVibe === null || l.vibe_ids.includes(activeVibe);
			return matchesText && matchesVibe;
		})
	);
</script>

<div class="stack">
	<p class="eyebrow">Lists</p>
	<h1 class="page-title">Lists from other people</h1>
</div>

{#if form?.message}
	<div class="notification is-danger is-light">{form.message}</div>
{/if}

<div class="search stack">
	<input
		class="input search-input"
		type="search"
		bind:value={q}
		placeholder="Search lists, people or vibes…"
		aria-label="Search lists"
	/>
	{#if q}
		<button class="button clear" onclick={() => (q = '')}>Clear</button>
	{/if}
</div>

<div class="chips stack" role="group" aria-label="Filter lists by vibe">
	<button class="chip {activeVibe === null ? 'active' : ''}" onclick={() => (activeVibe = null)}>
		All
	</button>
	{#each data.vibes as vibe (vibe.vibe_id)}
		<button
			class="chip {activeVibe === vibe.vibe_id ? 'active' : ''}"
			onclick={() => (activeVibe = vibe.vibe_id)}
		>
			{vibe.vibe_name}
		</button>
	{/each}
</div>

{#if searching}
	<section class="stack">
		<div class="section-head">
			<h2>Results</h2>
			<span class="muted">{results.length} found</span>
		</div>
		{#if results.length}
			<div class="columns is-multiline">
				{#each results as list (list.list_id)}
					<div class="column is-3-desktop is-6-tablet with-action">
						<div class="grow"><ListCard {list} vibeName={list.vibe_name} /></div>
						<SaveButton {list} savedListId={data.savedIdOf[list.list_id]} />
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
				<div class="column is-3-desktop is-6-tablet with-action">
					<div class="grow"><ListCard {list} vibeName={list.vibe_name} /></div>
						<SaveButton {list} savedListId={data.savedIdOf[list.list_id]} />
				</div>
			{/each}
		</div>
	</section>

	<section class="stack">
		<div class="section-head">
			<h2>All lists</h2>
		</div>
		{#if data.lists.length}
			<div class="columns is-multiline">
				{#each data.lists as list (list.list_id)}
					<div class="column is-3-desktop is-6-tablet with-action">
						<div class="grow"><ListCard {list} vibeName={list.vibe_name} /></div>
						<SaveButton {list} savedListId={data.savedIdOf[list.list_id]} />
					</div>
				{/each}
			</div>
		{:else}
			<p class="empty">No public lists yet.</p>
		{/if}
	</section>
{/if}

<style>
	.search {
		display: flex;
		gap: 0.5rem;
		max-width: 36rem;
	}
	.search-input {
		background: var(--card);
		border-color: var(--line);
		color: #fff;
		border-radius: 999px;
		padding-inline: 1.1rem;
	}
	.search-input:focus {
		border-color: var(--lime);
		box-shadow: 0 0 0 2px rgba(204, 255, 0, 0.2);
	}
	.clear {
		background: transparent;
		border-color: var(--line);
		color: #fff;
		border-radius: 999px;
	}
	/* ให้การ์ดยืดเต็มความสูง แล้วปุ่มอยู่ใต้การ์ดพอดี */
	.with-action {
		display: flex;
		flex-direction: column;
	}
	.grow {
		flex: 1;
	}
	.muted {
		color: var(--muted);
		font-size: 0.8rem;
	}
</style>
