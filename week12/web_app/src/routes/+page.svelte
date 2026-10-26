 
<script>
    let { data } = $props()
</script>
 
<div class="centered">
    <h1>todos</h1>
 
    <form method="POST" action="?/create">
        <label>
            add a todo:
            <input
                type="text"
                name="description"
                autocomplete="off"
            />
        </label>
        <button type="submit">Add</button>
    </form>
 
    <ul class="todos">
        {#each data.todos as todo (todo.id)}
            <li>
                <form action="?/delete" method="POST">
                    <input
                        type="hidden"
                        name="id"
                        value={todo.id}
                    />
                    <span>{todo.description}</span>
                    <button type="submit">complete</button>
                </form>
            </li>
        {/each}
    </ul>
</div>
 
 