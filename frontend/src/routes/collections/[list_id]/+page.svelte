<script>
	import PlaceCard from '#lib/PlaceCard.svelte';
	import SaveButton from '#lib/SaveButton.svelte';

	let { data, form } = $props();

	let imgFailed = $state(false);
	const hue = $derived((data.collection.list_id * 47) % 360);

	// ฟอร์มแก้ไข (เฉพาะเจ้าของ): เปิด/ปิดด้วย $state และผูกช่องชื่อด้วย bind:value
	let showEdit = $state(false);
	let name = $state(data.collection.title);
	let nameLeft = $derived(60 - name.length);
</script>

<a class="back" href="/collections">← Back to Collections</a>

{#if form?.message}
	<div class="notification is-danger is-light">{form.message}</div>
{/if}

<!-- ---------- ภาพปกและข้อมูล collection ---------- -->
<section class="hero stack" style="--h: {hue}">
	{#if data.collection.cover_image_url && !imgFailed}
		<img src={data.collection.cover_image_url} alt="" onerror={() => (imgFailed = true)} />
	{/if}
	<div class="shade"></div>
	<div class="hero-text">
		<p class="eyebrow">
			Collection · {data.places.length} {data.places.length === 1 ? 'place' : 'places'} · {data.saves}
			{data.saves === 1 ? 'save' : 'saves'}
			{#if !data.collection.is_public}<span class="private">Private</span>{/if}
		</p>
		<h1 class="page-title">{data.collection.title}</h1>
		{#if data.collection.description}<p class="lead">{data.collection.description}</p>{/if}
	</div>
</section>

<!-- ---------- เจ้าของ + ปุ่มที่ผู้ใช้ทำได้ ---------- -->
<section class="owner-row stack">
	<div class="owner">
		{#if data.owner.avatar}
			<img class="avatar" src={data.owner.avatar} alt="" />
		{:else}
			<span class="avatar ph">{data.owner.name[0]}</span>
		{/if}
		<div>
			<p class="muted">Made by</p>
			<p class="owner-name">{data.isOwner ? 'You' : data.owner.name}</p>
			{#if data.owner.bio && !data.isOwner}<p class="muted">{data.owner.bio}</p>{/if}
		</div>
	</div>

	{#if !data.isOwner}
		<div class="actions">
			{#if data.followId}
				<form method="POST" action="?/unfollow">
					<input type="hidden" name="follow_id" value={data.followId} />
					<button class="btn saved">✕ Unfollow {data.owner.name}</button>
				</form>
			{:else}
				<form method="POST" action="?/follow">
					<input type="hidden" name="user_id" value={data.owner.user_id} />
					<button class="btn">+ Follow {data.owner.name}</button>
				</form>
			{/if}
			<SaveButton list={data.collection} savedListId={data.savedListId} />
		</div>
	{:else}
		<div class="actions">
			<button class="btn" onclick={() => (showEdit = !showEdit)}>
				{showEdit ? 'Close editor' : '✎ Edit this Collection'}
			</button>
		</div>
	{/if}
</section>

<!-- ---------- แก้ไข / ลบ (เฉพาะเจ้าของ) ---------- -->
{#if data.isOwner && showEdit}
	<section class="panel-box stack">
		<p class="eyebrow">Edit collection details</p>
		<form method="POST" action="?/updateCollection">
			<div class="field">
				<label class="label has-text-grey-light" for="c-name">Name</label>
				<input id="c-name" class="input dark" name="list_name" bind:value={name} maxlength="60" required />
				<p class="help {nameLeft < 10 ? 'has-text-warning' : 'has-text-grey'}">{nameLeft} characters left</p>
			</div>
			<div class="field">
				<label class="label has-text-grey-light" for="c-desc">Description</label>
				<textarea id="c-desc" class="textarea dark" name="description" maxlength="200">{data.collection.description}</textarea>
			</div>
			<label class="checkbox has-text-grey-light">
				<input type="checkbox" name="is_public" checked={data.collection.is_public} />
				Public (other people can see and save it)
			</label>
			<div class="buttons mt-4">
				<button class="btn saved fit">Save Changes</button>
			</div>
		</form>

		<hr />
		<p class="muted">Deleting hides this collection from everyone. Your saved data stays in the database.</p>
		<form method="POST" action="?/deleteCollection">
			<button class="button is-danger is-outlined is-small mt-2">Delete this Collection</button>
		</form>
	</section>
{/if}

<!-- ---------- เพิ่มสถานที่ (เฉพาะเจ้าของ) ---------- -->
{#if data.isOwner}
	<section class="panel-box stack">
		<p class="eyebrow">Add a place to this collection</p>
		{#if data.addablePlaces.length}
			<form method="POST" action="?/addPlace" class="add-form">
				<div class="select is-fullwidth">
					<select name="place_id" required>
						{#each data.addablePlaces as p (p.place_id)}
							<option value={p.place_id}>{p.place_name} — {p.area_name}</option>
						{/each}
					</select>
				</div>
				<button class="btn saved fit">+ Add Place</button>
			</form>
		{:else}
			<p class="muted">Every place is already in this collection.</p>
		{/if}
	</section>
{/if}

<!-- ---------- สถานที่ใน collection ---------- -->
<section class="stack">
	<div class="section-head">
		<h2>Places in this collection</h2>
	</div>
	{#if data.places.length}
		<div class="columns is-multiline">
			{#each data.places as place, i (place.place_id)}
				<div class="column is-4-desktop is-6-tablet with-action">
					<span class="order">#{i + 1}</span>
					<div class="grow"><PlaceCard {place} /></div>
					{#if data.isOwner}
						<form method="POST" action="?/removePlace">
							<input type="hidden" name="place_id" value={place.place_id} />
							<button class="btn small">✕ Remove from this Collection</button>
						</form>
					{/if}
				</div>
			{/each}
		</div>
	{:else}
		<p class="empty">No places in this collection yet.</p>
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
		min-height: 280px;
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
	.private {
		margin-left: 0.5rem;
		padding: 0.1rem 0.5rem;
		border-radius: 999px;
		background: #333;
		color: #fff;
		letter-spacing: 0.05em;
	}
	.owner-row {
		display: flex;
		flex-wrap: wrap;
		align-items: center;
		justify-content: space-between;
		gap: 1rem;
	}
	.owner {
		display: flex;
		align-items: center;
		gap: 0.75rem;
	}
	.avatar {
		width: 52px;
		height: 52px;
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
	.owner-name {
		color: #fff;
		font-weight: 700;
	}
	.actions {
		display: grid;
		gap: 0.25rem;
		min-width: 260px;
	}
	.panel-box {
		padding: 1rem 1.25rem;
		border: 1px solid var(--line);
		border-radius: 12px;
		background: var(--card);
	}
	.panel-box .eyebrow {
		margin-bottom: 0.75rem;
	}
	.dark,
	.add-form select {
		background: #111;
		border-color: #444;
		color: #fff;
	}
	.add-form {
		display: flex;
		flex-wrap: wrap;
		gap: 0.6rem;
	}
	.add-form .select {
		flex: 1;
		min-width: 220px;
	}
	.btn {
		width: 100%;
		padding: 0.55rem 0.9rem;
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
	.btn.fit {
		width: auto;
	}
	.btn.small {
		margin-top: 0.5rem;
		font-size: 0.75rem;
	}
	hr {
		background: var(--line);
		height: 1px;
		margin: 1.25rem 0 0.75rem;
	}
	.muted {
		color: var(--muted);
		font-size: 0.8rem;
	}
	.with-action {
		position: relative;
		display: flex;
		flex-direction: column;
	}
	.grow {
		flex: 1;
	}
	.order {
		position: absolute;
		top: 1.3rem;
		left: 1.3rem;
		z-index: 1;
		padding: 0.1rem 0.5rem;
		border-radius: 999px;
		background: rgba(0, 0, 0, 0.7);
		color: var(--lime);
		font-size: 0.75rem;
		font-weight: 800;
	}
</style>
