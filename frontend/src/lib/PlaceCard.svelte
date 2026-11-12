<script>
	// place: PlaceOut จาก backend (ถ้าผ่าน decoratePlaces จะมี area_name และ vibes มาด้วย)
	// กดการ์ดแล้วไปหน้ารายละเอียดสถานที่ /explore/[place_id]
	let { place, areaName = undefined, vibes = undefined } = $props();

	const area = $derived(areaName ?? place.area_name ?? 'Unknown area');
	const tags = $derived(vibes ?? place.vibes ?? []);
	const hue = $derived((place.place_id * 47) % 360);

	// ถ้ารูปโหลดไม่ได้ ให้แสดงพื้นสีแทน
	let imgFailed = $state(false);
</script>

<a class="place-link" href="/explore/{place.place_id}">
	<article class="place">
		<div class="photo" style="--h: {hue}">
			{#if place.image_url && !imgFailed}
				<img src={place.image_url} alt={place.place_name} loading="lazy" onerror={() => (imgFailed = true)} />
			{/if}
		</div>

		<div class="body">
			<p class="eyebrow">{area}</p>
			<h3 class="name">{place.place_name}</h3>
			<p class="address">{place.address}</p>
			<p class="desc">{place.description}</p>
			<p class="hours">🕒 {place.opening_time} – {place.closing_time}</p>

			<div class="tags">
				{#if place.price_level}
					<span class="tag price">{place.price_level}</span>
				{:else}
					<span class="tag is-dark has-text-grey">No price data</span>
				{/if}
				{#each tags as v (v)}
					<span class="tag vibe">{v}</span>
				{/each}
			</div>
		</div>
	</article>
</a>

<style>
	.place-link {
		display: block;
		height: 100%;
		color: inherit;
	}
	.place {
		height: 100%;
		overflow: hidden;
		background: var(--card);
		border: 1px solid var(--line);
		border-radius: 12px;
		color: #fff;
		transition: border-color 0.15s, transform 0.15s;
	}
	.place-link:hover .place {
		border-color: var(--lime);
		transform: translateY(-2px);
	}
	.photo {
		height: 160px;
		background: linear-gradient(135deg, hsl(var(--h) 70% 35%), hsl(var(--h) 60% 12%));
	}
	.photo img {
		width: 100%;
		height: 100%;
		object-fit: cover;
		display: block;
	}
	.body {
		padding: 1.1rem 1.25rem 1.25rem;
	}
	.eyebrow {
		margin-bottom: 0.25rem;
	}
	.name {
		color: #fff;
		font-size: 1.15rem;
		font-weight: 700;
		line-height: 1.25;
		margin-bottom: 0.25rem;
	}
	.address {
		color: var(--muted);
		font-size: 0.75rem;
		margin-bottom: 0.75rem;
	}
	.desc {
		color: #cfcfcf;
		font-size: 0.85rem;
		margin-bottom: 0.5rem;
	}
	.hours {
		color: var(--muted);
		font-size: 0.8rem;
		margin-bottom: 0.75rem;
	}
	.tags {
		display: flex;
		flex-wrap: wrap;
		gap: 0.4rem;
	}
	.price {
		background: var(--lime);
		color: #000;
		font-weight: 700;
	}
	.vibe {
		background: transparent;
		border: 1px solid var(--line);
		color: #cfcfcf;
	}
</style>
