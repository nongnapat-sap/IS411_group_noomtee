<script>
	import { count } from '#lib/shared.js';
	import Incrementer from './incrementer.svelte';
	import Decrementer from './decrementer.svelte';
	import Resetter from './Resetter.svelte';
</script>

<h1>The count is {$count}</h1>

<Incrementer />
<Decrementer />
<Resetter />