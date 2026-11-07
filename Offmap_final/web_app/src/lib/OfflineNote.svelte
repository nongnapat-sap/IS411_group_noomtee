<script>
	// แสดงป้ายเล็ก ๆ เมื่อหน้านั้นใช้ข้อมูลตัวอย่างแทน backend
	let { show = false } = $props();
</script>

{#if show}
	<p class="note">⚠ Backend is offline — showing sample data.</p>
{/if}

<style>
	.note {
		display: inline-block;
		margin-bottom: 1rem;
		padding: 0.25rem 0.75rem;
		border: 1px dashed #5a5a1a;
		border-radius: 6px;
		color: #d9d96a;
		font-size: 0.75rem;
	}
</style>