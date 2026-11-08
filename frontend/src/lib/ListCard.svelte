<script>
	// list: { title, description, owner_name, place_ids, place_count, saves }
	// list คือ "เพลย์ลิสต์ของสถานที่" แบบ Spotify
	let { list, vibeName = null } = $props();
</script>

<article class="list">
	<div class="cover" aria-hidden="true">
		{#each list.place_ids.slice(0, 3) as id (id)}
			<span style="--h: {(id * 47) % 360}"></span>
		{/each}
	</div>
	<h3>{list.title}</h3>
	<p class="by">by {list.owner_name}</p>
	{#if list.description}<p class="desc">{list.description}</p>{/if}
	<p class="meta">
		{list.place_count}
		{list.place_count === 1 ? 'place' : 'places'} · {list.saves} saves
	</p>
	{#if vibeName}<span class="tag vibe">{vibeName}</span>{/if}
</article>

<style>
	.list {
		height: 100%;
		padding: 0.9rem;
		border-radius: 12px;
		background: var(--card);
		border: 1px solid var(--line);
		transition: border-color 0.15s, background 0.15s;
	}
	.list:hover {
		border-color: var(--lime);
		background: var(--card-hover);
	}
	.cover {
		display: grid;
		grid-template-columns: 2fr 1fr;
		grid-template-rows: 1fr 1fr;
		gap: 4px;
		height: 120px;
		margin-bottom: 0.8rem;
		border-radius: 8px;
		overflow: hidden;
	}
	.cover span {
		background: linear-gradient(135deg, hsl(var(--h) 70% 40%), hsl(var(--h) 60% 14%));
	}
	.cover span:first-child {
		grid-row: span 2;
	}
	h3 {
		color: #fff;
		font-size: 1rem;
		font-weight: 700;
		line-height: 1.25;
	}
	.by {
		color: var(--lime);
		font-size: 0.75rem;
		font-weight: 600;
		margin-bottom: 0.4rem;
	}
	.desc {
		color: #cfcfcf;
		font-size: 0.8rem;
		margin-bottom: 0.4rem;
	}
	.meta {
		color: var(--muted);
		font-size: 0.75rem;
		margin-bottom: 0.5rem;
	}
	.vibe {
		background: transparent;
		border: 1px solid var(--line);
		color: #cfcfcf;
		font-size: 0.7rem;
	}
</style>