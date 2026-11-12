<script>
	let { data, children } = $props();
	let open = $state(false);

	const tabs = [
		{ href: '/', label: 'Home' },
		{ href: '/explore', label: 'Explore' },
		{ href: '/collections', label: 'Collections' },
		{ href: '/user', label: 'My Profile' }
	];

	const isActive = (href) => (href === '/' ? data.path === '/' : data.path.startsWith(href));
</script>

<nav class="navbar is-black" aria-label="main navigation">
	<div class="navbar-brand">
		<a class="navbar-item brand" href="/" onclick={() => (open = false)}>OFFMAP</a>
		<button
			class="navbar-burger {open ? 'is-active' : ''}"
			aria-label="menu"
			aria-expanded={open}
			onclick={() => (open = !open)}
		>
			<span aria-hidden="true"></span>
			<span aria-hidden="true"></span>
			<span aria-hidden="true"></span>
			<span aria-hidden="true"></span>
		</button>
	</div>

	<div class="navbar-menu {open ? 'is-active' : ''}">
		<div class="navbar-start">
			{#each tabs as tab (tab.href)}
				<a
					class="navbar-item tab {isActive(tab.href) ? 'active' : ''}"
					href={tab.href}
					aria-current={isActive(tab.href) ? 'page' : undefined}
					onclick={() => (open = false)}
				>
					{tab.label}
				</a>
			{/each}
		</div>
	</div>
</nav>

<main class="section">
	<div class="container">
		{@render children()}
	</div>
</main>

<style>
	.navbar {
		border-bottom: 1px solid var(--line);
	}
	.brand {
		color: var(--lime);
		font-weight: 800;
		letter-spacing: 0.08em;
	}
	.tab {
		color: #b5b5b5;
		font-weight: 600;
	}
	.tab:hover {
		color: #fff;
		background: transparent;
	}
	.tab.active {
		color: var(--lime);
		box-shadow: inset 0 -2px 0 var(--lime);
	}
	.navbar-burger {
		color: #fff;
	}
	.navbar-menu {
		background: #000;
	}
	main {
		min-height: 100vh;
		background: #000;
	}
</style>
