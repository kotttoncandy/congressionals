<script>
    import Footer from "$lib/components/footer.svelte";
    import { page } from '$app/state';
    import { onMount } from "svelte";

    const type = page.url.searchParams.get('type');
    const id = page.url.searchParams.get('id');
    const name = page.url.searchParams.get('name');

    let details = $state();
    let loaded = $state(false)

    async function getDetails() {
        const response = await fetch(`/api/trails?trail=${id}`);
        const data = await response.json();
        console.log(data);
        details = data.data;
        loaded = true

    }
    onMount(() => {
        getDetails();
    });
</script>

<main class="infoPage">
    <h1 class="trailName">{name}</h1>
    {#if !loaded}
    
        <h5 aria-busy="true">Loading</h5>
    {:else}
        
        <div class="body">
            <article>
                {details.description}
            </article>

        </div>
    {/if}
</main>

<style>
    .infoPage {
        display: flex;
        padding: 20px;
        flex-direction: column;
    }
    .body {
        display: flex;

    }

    .trailName {
        padding-top: 20px;
    }
</style>