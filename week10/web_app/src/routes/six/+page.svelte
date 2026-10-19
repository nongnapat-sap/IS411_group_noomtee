<script>
    import { marked } from 'marked'
    let value = $state(`Some words are *italic*, some are **bold**\n\n- lists\n- are\n- cool`)
    let name = $state('World')
    let a = $state(1)
    let b = $state(2)
    let yes = $state(false)
 
    let question = $state([
        {id: 1, text: 'What is your name?'},
        {id: 2, text: 'What is your mother\'s name?'},
        {id: 3, text: 'What is your personal fact from Google?'}
    ])
 
    let selected = $state()
    let answer = $state('')
    // @ts-ignore
    function handleSubmit(e) {
        e.preventDefault()
        alert(`answered question ${selected.id} (${selected.text})
with "${answer}"`)
    }
   let scoops = $state(1)
    // @ts-ignore
    let flavours = $state([])
    const formatter = new Intl.ListFormat('en', { style: 'long', type: 'conjunction'})

</script>
 
<hr>
<input type="text" value={name}>
<input type="text" bind:value={name}>
 
<h1>Hello {name}!</h1>
 
<hr>
 
<label>
    <input type="number" bind:value={a} min="0" max="10"/>
    <input type="range" bind:value={a} min="0" max="10"/>
</label>
 
<label>
    <input type="number" bind:value={b} min="0" max="10"/>
    <input type="range" bind:value={b} min="0" max="10"/>
</label>
<p> {a} + {b} = {a + b}</p>
 
<hr>
 
<label>
    <input type="checkbox" bind:checked={yes}/>
    Yes! Send me regular email updates
</label>
 
{#if yes}
    <p>Thank you. We will bombard your inbox.</p>
{:else}
    <p>You must opt-in to continue.</p>
{/if}
 
<hr />
 
<h2>Insecurity questions</h2>
<form onsubmit={handleSubmit}>
 
    <select bind:value={selected} onchange={() => (answer = '')}>
        {#each question as question}
            <option value={question}>
                {question.text}
            </option>
        {/each}
    </select>
    <input value={answer} />
    <button disabled={!answer} type="submit">
        Submit
    </button>
</form>
 
<p>selected question {selected
    ? selected.id
    : '[waiting...]'}
</p>

<hr />

<h2>Size</h2>
{#each [1, 2, 3, 4] as number}
    <label>
        <input
            type="radio"
            name="scoops"
            value={number}
            bind:group={scoops}
        />
        {number} {number === 1 ? 'scoop' : 'scoops'}
    </label>
 {/each}

<h2>Flavours</h2>
{#each ['Chocolate', 'Vanilla', 'Strawberry'] as flavour}
    <label>
        <input
            type="checkbox"
            name="flavours"
            value={flavour}
            bind:group={flavours}
        />
        {flavour}
    </label>

{/each}

{#if flavours.length === 0}
    <p>Please select at least one flavour</p>
{:else if flavours.length > scoops}
    <p>Cannot select more than {scoops} flavours</p>
{:else}
    <p>
        Your ordered {scoops} {scoops === 1 ? 'scoop' : 'scoops'} of
        {formatter.format(flavours)}
    </p>
{/if}

<div class="grid">
        input
        <textarea bind:value></textarea>
        output
        <div>{@html marked(value)}</div>
</div>

<style>
    .grid {
        display: grid;
        grid-template-columns: 5em 1fr;
        grid-template-rows: 1fr 1fr;
        grid-gap: 1em;
        height: 100%;
    }

    textarea {
        flex: 1;
        resize: none;
    }
</style>