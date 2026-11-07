<script>
	// area: AreaOut จาก backend — กดแล้วไปหน้า Explore ที่กรองเฉพาะ area นี้
	let { area } = $props();

	// backend ยังไม่มีรูปจริง (cover_image_url เป็นลิงก์ตัวอย่าง) จึงใช้สีไล่เฉดตาม id แทน
	const hue = $derived((area.area_id * 47) % 360);
</script>

<a class="area" href={`/places?area=${area.area_id}`} style:--h={hue}>
	<span class="count">{area.total_places} {area.total_places === 1 ? 'place' : 'places'}</span>
	<div>
		<h3>{area.area_name}</h3>
		<p class="district">{area.district}</p>
		{#if area.description}<p class="desc">{area.description}</p>{/if}
	</div>
</a>

<style>
	.area {
		display: flex;
		flex-direction: column;
		justify-content: space-between;
		gap: 1.5rem;
		min-height: 180px;
		height: 100%;
		padding: 1.25rem;
		border: 1px solid var(--line);
		border-radius: 12px;
		background:
			radial-gradient(circle at 15% 0%, hsl(var(--h) 75% 32% / 0.6), transparent 65%),
			var(--card);
		color: #fff;
		transition: border-color 0.15s, transform 0.15s;
	}
	.area:hover {
		border-color: var(--lime);
		transform: translateY(-2px);
	}
	.count {
		align-self: flex-start;
		padding: 0.15rem 0.6rem;
		border-radius: 999px;
		background: rgba(0, 0, 0, 0.55);
		color: var(--lime);
		font-size: 0.7rem;
		font-weight: 700;
	}
	h3 {
		color: #fff;
		font-size: 1.3rem;
		font-weight: 800;
		line-height: 1.1;
	}
	.district {
		color: var(--lime);
		font-size: 0.75rem;
		font-weight: 600;
		margin-bottom: 0.4rem;
	}
	.desc {
		color: #cfcfcf;
		font-size: 0.8rem;
	}
</style>