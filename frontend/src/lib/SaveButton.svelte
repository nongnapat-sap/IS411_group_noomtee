<script>
	// ปุ่ม save / unsave ใต้การ์ด list
	// savedListId มีค่า = save ไว้แล้ว → ส่งไป unsaveList, ไม่มีค่า → ส่งไป saveList
	let { list, savedListId = undefined } = $props();
</script>

{#if savedListId}
	<form method="POST" action="?/unsaveList">
		<input type="hidden" name="saved_list_id" value={savedListId} />
		<button class="save-btn saved">✓ Saved</button>
	</form>
{:else}
	<form method="POST" action="?/saveList">
		<input type="hidden" name="list_id" value={list.list_id} />
		<button class="save-btn">+ Save list</button>
	</form>
{/if}

<style>
	form {
		margin-top: 0.5rem;
	}
	.save-btn {
		width: 100%;
		padding: 0.45rem;
		border: 1px solid var(--line);
		border-radius: 8px;
		background: transparent;
		color: #d6d6d6;
		font: inherit;
		font-size: 0.8rem;
		font-weight: 600;
		cursor: pointer;
	}
	.save-btn:hover {
		border-color: var(--lime);
		color: #fff;
	}
	.save-btn.saved {
		background: var(--lime);
		border-color: var(--lime);
		color: #000;
	}
</style>
