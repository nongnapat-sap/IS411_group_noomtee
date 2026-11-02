<script>
    let { data, form } = $props()
</script>
 
<div class="centered">
    <h1>Todos</h1>
 
    {#if form?.error}
        <p class="error" style="color:red">{form.error}</p>
    {/if}
 
    <form method="post" action="?/create">
        <label>
            add a todo:
            <input
                type="text"
                name="description"
                value={form?.description ?? ''}
                autocomplete="off"
            />
        </label>
    </form>
    <ul class="todos">
        {#each data.todos as todo (todo.id)}
            <li>
                <form action="?/delete" method="post">
                    <input type="hidden" name="id" value={todo.id} />
                    <span>{todo.description}</span>
                    <button>Complete</button>
                </form>
            </li>
        {/each}
    </ul>
</div>
 