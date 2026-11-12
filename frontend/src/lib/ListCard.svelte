<script>
	// list = collection หนึ่งชุด: { list_id, title, description, owner_name, owner_avatar, cover_image_url, place_ids, place_count, saves }
	// (ใน database ชื่อตาราง lists แต่บนหน้าเว็บเรียกว่า Collection)
	// กดการ์ดแล้วไปหน้ารายละเอียด /collections/[list_id]
	let { list, vibeName = null } = $props();

	let imgFailed = $state(false);
</script>

<a class="list-link" href="/collections/{list.list_id}">
	<article class="list">
		<div class="cover" aria-hidden="true">
			{#if list.cover_image_url && !imgFailed}
				<img src={list.cover_image_url} alt="" loading="lazy" onerror={() => (imgFailed = true)} />
			{:else}
				<div class="grid">
					{#each list.place_ids.slice(0, 3) as id (id)}
						<span style="--h: {(id * 47) % 360}"></span>
					{/each}
				</div>
			{/if}
			<span class="count">{list.place_count} {list.place_count === 1 ? 'place' : 'places'}</span>
		</div>
		<h3>{list.title}</h3>
		<p class="by">by {list.owner_name}</p>
		{#if list.description}<p class="desc">{list.description}</p>{/if}
		<p class="meta">{list.saves} {list.saves === 1 ? 'save' : 'saves'}</p>
		{#if vibeName}<span class="tag vibe">{vibeName}</span>{/if}
	</article>
</a>

<style>
	.list-link {
		display: block;
		height: 100%;
		color: inherit;
	}
	.list {
		height: 100%;
		padding: 0.9rem;
		border-radius: 12px;
		background: var(--card);
		border: 1px solid var(--line);
		transition: border-color 0.15s, background 0.15s;
	}
	.list-link:hover .list {
		border-color: var(--lime);
		background: var(--card-hover);
	}
	.cover {
		position: relative;
		height: 140px;
		margin-bottom: 0.8rem;
		border-radius: 8px;
		overflow: hidden;
		background: #222;
	}
	.cover img {
		width: 100%;
		height: 100%;
		object-fit: cover;
		display: block;
	}
	.grid {
		display: grid;
		grid-template-columns: 2fr 1fr;
		grid-template-rows: 1fr 1fr;
		gap: 4px;
		height: 100%;
	}
	.grid span {
		background: linear-gradient(135deg, hsl(var(--h) 70% 40%), hsl(var(--h) 60% 14%));
	}
	.grid span:first-child {
		grid-row: span 2;
	}
	.count {
		position: absolute;
		left: 8px;
		bottom: 8px;
		padding: 0.1rem 0.55rem;
		border-radius: 999px;
		background: rgba(0, 0, 0, 0.65);
		color: var(--lime);
		font-size: 0.7rem;
		font-weight: 700;
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
