<script>
	import favicon from '#lib/assets/favicon.svg';

	/** @type {{children: import('svelte').Snippet}} */
	let { children } = $props();
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>

<nav>
	<a href="/">Home</a>
	<a href="/one">Props</a>
	<a href="/two">Logic</a>
	<a href="/three">Each blocks</a>
	<a href="/four">Keyed each</a>
	<a href="/five">Blogs</a>
	<a href="/six">Bindings</a>
	<a href="/seven">Shared</a>

</nav>

{@render children()}
