<script>
    import { quantity } from '$lib/quantity.svelte.js'

    function increment() {
        quantity.number += 1
    }

    function decrement() {
        if (quantity.number === 0) {
            return
        }
        quantity.number -= 1
    }
</script>

<span>Current quantity : {quantity.number}</span>

<div>
    <button class="button" onclick={decrement}> - </button>
    <button class="button" onclick={increment}> + </button>
</div>