<script>
    import Quantifier from "$lib/Quantifier.svelte"

	let name = 'Chanyapak'
	let imageUrl = 'https://www.yourtango.com/sites/default/files/image_blog/2026-01/males-science-says-orange-cats-extra-special.png'
	let string = 'this string contains some strong-HTML!!!</strong>'
</script>


<h1>Welcome to IS411</h1>
<div>
	<p>Hello:{name}</p>
	<p>Week 09</p>
	<p>Example 1</p>
	<p>{@html string}</p>
	<img height="200" src={imageUrl} alt={name}>
</div>

<style>
	p {
		color: rgb(235, 180, 43);
		font-family: 'Comic Sans MS', cursive;
		font-size: 2em;
	}
	h1 {
		color: rgb(248, 138, 2);
		font-family: Verdana, Geneva, Tahoma, sans-serif;
	}
</style>

<Quantifier />

