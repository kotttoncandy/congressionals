<script>
	import { onNavigate } from '$app/navigation';
	import favicon from '$lib/assets/favicon.svg';
	import Footer from '$lib/components/footer.svelte';
	import { userData } from "$lib/userData.js";
	let { children } = $props();
	let previous = $userData;

	onNavigate((navigation) => {
		if (!document.startViewTransition) return;

		return new Promise((resolve) => {
			document.startViewTransition(async () => {
				resolve();
				await navigation.complete;
			});
		});
	});

	userData.subscribe((value) => {
		if (value != previous) {
			previous = value;
			localStorage.setItem("userData", JSON.stringify(value));
			console.log(value.favTrails)
		}

	});

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