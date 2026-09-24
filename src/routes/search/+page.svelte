<script>
    import Footer from "$lib/components/footer.svelte";
    import SiteHeader from "$lib/components/siteHeader.svelte";
    import { onMount } from "svelte";
    let searchedTrails = $state([]);
    let searchedBeaches = $state([]);
    let trails = $state([]);
    let beaches = $state([]);
    let timeout = null;

    let query = $state("");

    $effect(() => {
        console.log(query);
        clearTimeout(timeout);

        timeout = setTimeout(() => {
            if (query.length < 2) return;
            searchedTrails = trails.filter(
                (trail) =>
                    trail.name.toLowerCase().includes(query.toLowerCase()) ||
                    trail.island.toLowerCase().includes(query.toLowerCase()),
            );
            searchedBeaches = beaches.filter((beach) =>
                beach.tags.name.toLowerCase().includes(query.toLowerCase()),
            );
        }, 1500);
    });

    let loaded = $state(false);
    import Beach from "$lib/components/Beach.svelte";
    import Trail from "$lib/components/Trail.svelte";
    import { get } from "svelte/store";

    async function getTrails() {
        const response = await fetch(`/api/trails`);
        const data = await response.json();
        trails = data.data;
        getBeaches();
    }

    async function getBeaches() {
        const response = await fetch("/beaches.json");
        const response2 = await fetch("/beachActivities.json");
        const data = await response.json();
        const data2 = await response2.json();

        beaches = data.elements;
        loaded = true;
    }

    onMount(() => {
        getTrails();
    });
</script>

<main>
    <h1 style="padding-top: 20px;" class="pageTitle">Search Away!</h1>
    <form class="findSpots">
        <fieldset role="group">
            <input
                bind:value={query}
                type="search"
                name="search"
                placeholder="Find Spots"
                autofocus
            />
        </fieldset>
    </form>

    {#if loaded}
        {#if query.length >= 2}
            {#each searchedTrails as trail}
                <Trail {trail}></Trail>
            {/each}
            {#each searchedBeaches as beach}
                <Beach {beach}></Beach>
            {/each}
        {/if}
    {/if}
</main>

<style>
    main {
        display: flex;
        padding: 20px;
        flex-direction: column;
    }
    main * {
        border-radius: 20px;
    }
    .findSpots {
        view-transition-name: findSpots;
        width: 100%;
    }

    .pageTitle {
        view-transition-name: pageTitle;
    }
</style>
