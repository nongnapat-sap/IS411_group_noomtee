<script>
	import { page } from '$app/state';

	let { children } = $props();
	let open = $state(false);

	const tabs = [
		{ href: '/', label: 'Home' },
		{ href: '/places', label: 'Explore' },
		{ href: '/lists', label: 'Lists' },
		{ href: '/user', label: 'User' }
	];

	const isActive = (href) =>
		href === '/' ? page.url.pathname === '/' : page.url.pathname.startsWith(href);
</script>

<svelte:head>
	<title>OFFMAP — Discover Bangkok beyond the obvious</title>
	<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bulma/1.0.2/css/bulma.min.css" />
</svelte:head>

<nav class="navbar is-black" aria-label="main navigation">
	<div class="navbar-brand">
		<a class="navbar-item brand" href="/" onclick={() => (open = false)}>OFFMAP</a>
		<button
			class="navbar-burger"
			class:is-active={open}
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

	<div class="navbar-menu" class:is-active={open}>
		<div class="navbar-start">
			{#each tabs as tab (tab.href)}
				<a
					class="navbar-item tab"
					class:active={isActive(tab.href)}
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
	:global(:root) {
		--lime: #ccff00;
		--card: #141414;
		--card-hover: #1b1b1b;
		--line: #2a2a2a;
		--muted: #8f8f8f;
	}
	:global(body) {
		background: #000;
		color: #fff;
	}

	/* ---------- ตัวช่วยที่ใช้ร่วมกันทุกหน้า ---------- */
	:global(.eyebrow) {
		color: var(--lime);
		font-size: 0.7rem;
		font-weight: 700;
		letter-spacing: 0.18em;
		text-transform: uppercase;
	}
	:global(.page-title) {
		color: #fff;
		font-size: clamp(1.8rem, 4vw, 2.6rem);
		font-weight: 800;
		letter-spacing: -0.02em;
		line-height: 1.1;
	}
	:global(.section-head) {
		display: flex;
		align-items: baseline;
		justify-content: space-between;
		gap: 1rem;
		margin-bottom: 1rem;
	}
	:global(.section-head h2) {
		color: #fff;
		font-size: 1.25rem;
		font-weight: 700;
	}
	:global(.see-all) {
		color: var(--lime);
		font-size: 0.8rem;
		font-weight: 700;
	}
	:global(.chips) {
		display: flex;
		flex-wrap: wrap;
		gap: 0.5rem;
	}
	:global(.chip) {
		display: inline-flex;
		align-items: center;
		gap: 0.4rem;
		padding: 0.4rem 0.9rem;
		border: 1px solid var(--line);
		border-radius: 999px;
		background: var(--card);
		color: #d6d6d6;
		font-size: 0.8rem;
		font-weight: 600;
		transition: border-color 0.15s, color 0.15s;
	}
	:global(a.chip:hover) {
		border-color: var(--lime);
		color: #fff;
	}
	:global(.chip.active) {
		background: var(--lime);
		border-color: var(--lime);
		color: #000;
	}
	:global(.empty) {
		padding: 2rem;
		border: 1px dashed var(--line);
		border-radius: 12px;
		color: var(--muted);
		text-align: center;
	}
	:global(.stack) {
		margin-bottom: 3rem;
	}

	/* ---------- navbar ---------- */
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