<script>
	// area: AreaOut จาก backend — กดแล้วไปหน้า /areas/[area_id]
	let { area } = $props();

	// ถ้ารูปโหลดไม่ได้ ใช้สีไล่เฉดตาม id แทน
	const hue = $derived((area.area_id * 47) % 360);
	let imgFailed = $state(false);
</script>

<a class="area" href="/areas/{area.area_id}" style="--h: {hue}">
	{#if area.cover_image_url && !imgFailed}
		<img src={area.cover_image_url} alt="" loading="lazy" onerror={() => (imgFailed = true)} />
	{/if}
	<div class="shade"></div>
	<span class="count">{area.total_places} {area.total_places === 1 ? 'place' : 'places'}</span>
	<div class="text">
		<h3>{area.area_name}</h3>
		<p class="district">{area.district}</p>
		{#if area.description}<p class="desc">{area.description}</p>{/if}
	</div>
</a>

<style>
	.area {
		position: relative;
		display: flex;
		flex-direction: column;
		justify-content: space-between;
		gap: 1.5rem;
		min-height: 200px;
		height: 100%;
		padding: 1.25rem;
		overflow: hidden;
		border: 1px solid var(--line);
		border-radius: 12px;
		background: linear-gradient(135deg, hsl(var(--h) 70% 30%), hsl(var(--h) 60% 10%));
		color: #fff;
		transition: border-color 0.15s, transform 0.15s;
	}
	.area:hover {
		border-color: var(--lime);
		transform: translateY(-2px);
	}
	img {
		position: absolute;
		inset: 0;
		width: 100%;
		height: 100%;
		object-fit: cover;
	}
	/* ทำให้รูปมืดลงด้านล่าง ตัวหนังสือจะอ่านง่าย */
	.shade {
		position: absolute;
		inset: 0;
		background: linear-gradient(180deg, rgba(0, 0, 0, 0.15), rgba(0, 0, 0, 0.85));
	}
	.count,
	.text {
		position: relative;
	}
	.count {
		align-self: flex-start;
		padding: 0.15rem 0.6rem;
		border-radius: 999px;
		background: rgba(0, 0, 0, 0.6);
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
		color: #e2e2e2;
		font-size: 0.8rem;
	}
</style>
