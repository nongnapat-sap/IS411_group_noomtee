<script>
	let { children } = $props();
</script>

<nav class="navbar is-black" style="border-bottom: 1px solid #333;">
	<div class="navbar-brand">
		<a class="navbar-item has-text-weight-bold" style="color: #ccff00;" href="/">OFFMAP</a>
	</div>
	<div class="navbar-menu is-active" style="background-color: black;">
		<div class="navbar-start">
			<a class="navbar-item has-text-white" href="/places">Explore</a>
			<a class="navbar-item has-text-grey-light" href="/areas">Areas</a>
			<!-- ลบ style สีเขียวออก และเปลี่ยนเป็น has-text-grey-light -->
			<a class="navbar-item has-text-grey-light" href="/journal">Journal</a>
		</div>
	</div>
</nav>

<main class="section has-background-black" style="min-height: 100vh;">
	<div class="container">
		{@render children()}
	</div>
</main>