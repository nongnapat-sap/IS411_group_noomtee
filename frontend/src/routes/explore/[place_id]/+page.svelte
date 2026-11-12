<script>
	let { data, form } = $props();

	// ถ้ารูปโหลดไม่ได้ ให้แสดงพื้นสีแทน
	let imgFailed = $state(false);
	const hue = $derived((data.place.place_id * 47) % 360);

	// collection ของเราที่ยังไม่มีสถานที่นี้ (ใช้ทำ dropdown)
	let canAdd = $derived(data.myCollections.filter((c) => !c.has_place));
	let alreadyIn = $derived(data.myCollections.filter((c) => c.has_place));

	const stars = (n) => '★'.repeat(n) + '☆'.repeat(5 - n);
</script>

<a class="back" href="/explore">← Back to Explore</a>

{#if form?.message}
	<div class="notification is-danger is-light">{form.message}</div>
{/if}

<!-- ---------- รูปและข้อมูลหลัก ---------- -->
<section class="hero stack" style="--h: {hue}">
	{#key data.place.place_id}
		{#if data.place.image_url && !imgFailed}
			<img src={data.place.image_url} alt={data.place.place_name} onerror={() => (imgFailed = true)} />
		{/if}
	{/key}
	<div class="shade"></div>
	<div class="hero-text">
		{#if data.area}
			<a class="eyebrow" href="/areas/{data.area.area_id}">{data.area.area_name}</a>
		{/if}
		<h1 class="page-title">{data.place.place_name}</h1>
		<p class="lead">{data.place.description}</p>
	</div>
</section>

<div class="columns stack">
	<!-- ซ้าย: รายละเอียด -->
	<div class="column is-7">
		<div class="info">
			<p><span class="label-sm">Address</span>{data.place.address}</p>
			<p><span class="label-sm">Open</span>{data.place.opening_time} – {data.place.closing_time}</p>
			<p><span class="label-sm">Price</span>{data.place.price_level}</p>
			{#if data.place.vibes.length}
				<div class="tags">
					{#each data.place.vibes as v (v)}
						<span class="tag vibe">{v}</span>
					{/each}
				</div>
			{/if}
		</div>
	</div>

	<!-- ขวา: สิ่งที่ผู้ใช้ทำได้ -->
	<div class="column is-5">
		<div class="panel-box">
			<p class="eyebrow">Your favorites</p>
			{#if data.favoriteId}
				<form method="POST" action="?/removeFavorite">
					<input type="hidden" name="favorite_id" value={data.favoriteId} />
					<button class="btn saved">✕ Remove from Favorites</button>
				</form>
			{:else}
				<form method="POST" action="?/addFavorite">
					<input type="hidden" name="place_id" value={data.place.place_id} />
					<button class="btn">♡ Add to Favorites</button>
				</form>
			{/if}
		</div>

		<div class="panel-box">
			<p class="eyebrow">Add to one of your collections</p>
			{#if canAdd.length}
				<form method="POST" action="?/addToCollection" class="add-form">
					<div class="select is-fullwidth">
						<select name="list_id" required>
							{#each canAdd as c (c.list_id)}
								<option value={c.list_id}>{c.title}</option>
							{/each}
						</select>
					</div>
					<button class="btn">+ Add to Collection</button>
				</form>
			{:else if data.myCollections.length}
				<p class="muted">This place is already in all of your collections.</p>
			{:else}
				<p class="muted">You don't have a collection yet. Create one on your profile page.</p>
			{/if}

			{#if alreadyIn.length}
				<p class="muted mt-3">
					Already in:
					{#each alreadyIn as c, i (c.list_id)}
						<a href="/collections/{c.list_id}">{c.title}</a>{i < alreadyIn.length - 1 ? ', ' : ''}
					{/each}
				</p>
			{/if}
		</div>
	</div>
</div>

<!-- ---------- journal ของคนที่เคยไป ---------- -->
<section class="stack">
	<div class="section-head">
		<div>
			<p class="eyebrow">From people who have been here</p>
			<h2>Visitor journals ({data.journals.length})</h2>
		</div>
	</div>
	{#if data.journals.length}
		<div class="journals">
			{#each data.journals as j (j.id)}
				<article class="journal">
					<div class="who">
						{#if j.author_avatar}
							<img class="avatar" src={j.author_avatar} alt="" />
						{:else}
							<span class="avatar ph">{j.author_name[0]}</span>
						{/if}
						<div>
							<p class="name">{j.author_name}</p>
							{#if j.visited}<p class="muted">Visited {j.visited}</p>{/if}
						</div>
					</div>
					<p class="stars" aria-label={`${j.rating} out of 5`}>{stars(j.rating)}</p>
					{#if j.title}<h3>{j.title}</h3>{/if}
					{#if j.note}<p class="note">{j.note}</p>{/if}
				</article>
			{/each}
		</div>
	{:else}
		<p class="empty">No one has written about this place yet.</p>
	{/if}
</section>

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
		min-height: 320px;
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
	.info p {
		margin-bottom: 0.75rem;
		color: #e2e2e2;
	}
	.label-sm {
		display: inline-block;
		min-width: 5rem;
		color: var(--muted);
		font-size: 0.8rem;
		font-weight: 700;
		text-transform: uppercase;
		letter-spacing: 0.08em;
	}
	.tags {
		display: flex;
		flex-wrap: wrap;
		gap: 0.4rem;
		margin-top: 1rem;
	}
	.vibe {
		background: transparent;
		border: 1px solid var(--line);
		color: #cfcfcf;
	}
	.panel-box {
		margin-bottom: 1rem;
		padding: 1rem 1.25rem;
		border: 1px solid var(--line);
		border-radius: 12px;
		background: var(--card);
	}
	.panel-box .eyebrow {
		margin-bottom: 0.6rem;
	}
	.add-form {
		display: flex;
		flex-direction: column;
		gap: 0.6rem;
	}
	.add-form select {
		background: #111;
		color: #fff;
		border-color: #444;
	}
	.btn {
		width: 100%;
		padding: 0.55rem;
		border: 1px solid var(--line);
		border-radius: 8px;
		background: transparent;
		color: #fff;
		font: inherit;
		font-size: 0.85rem;
		font-weight: 700;
		cursor: pointer;
	}
	.btn:hover {
		border-color: var(--lime);
	}
	.btn.saved {
		background: var(--lime);
		border-color: var(--lime);
		color: #000;
	}
	.muted {
		color: var(--muted);
		font-size: 0.8rem;
	}
	.muted a {
		color: var(--lime);
	}
	.journals {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
		gap: 1rem;
	}
	.journal {
		padding: 1rem 1.25rem;
		border: 1px solid var(--line);
		border-radius: 12px;
		background: var(--card);
	}
	.who {
		display: flex;
		align-items: center;
		gap: 0.6rem;
		margin-bottom: 0.6rem;
	}
	.avatar {
		width: 36px;
		height: 36px;
		border-radius: 50%;
		object-fit: cover;
		flex: none;
	}
	.avatar.ph {
		display: grid;
		place-items: center;
		background: #6b0f8a;
		color: #fff;
		font-weight: 700;
	}
	.name {
		color: #fff;
		font-weight: 700;
		font-size: 0.9rem;
	}
	.stars {
		color: var(--lime);
		letter-spacing: 0.1em;
	}
	.journal h3 {
		color: #fff;
		font-weight: 700;
		margin: 0.2rem 0;
	}
	.note {
		color: #cfcfcf;
		font-size: 0.85rem;
	}
</style>
