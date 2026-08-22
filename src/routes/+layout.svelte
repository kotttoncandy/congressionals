<script>
	import favicon from '$lib/assets/favicon.svg';
	import Footer from '$lib/components/footer.svelte';
	let { children } = $props();
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
	

</svelte:head>
<div class="app">
	<main class="mainApp">
		{@render children()}
	</main>
	
	<Footer></Footer>
</div>


<style>
  .app {
    display: flex;
    flex-direction: column;
	min-height: 100vh;
    gap: 1rem;
  }

  .mainApp {
	padding-bottom: 2rem;
  }
</style>