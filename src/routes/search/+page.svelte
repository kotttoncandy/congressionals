<script>
    import Footer from "$lib/components/footer.svelte";
    import SiteHeader from "$lib/components/siteHeader.svelte";
    import { onMount } from "svelte";
    let trails = $state();
    let beaches = $state();
    let query = $state("");
    let loaded = $state(false);
    import Beach from "$lib/components/Beach.svelte";
    import Trail from "$lib/components/Trail.svelte";
    async function getTrails() {
        
        const response = await fetch(`/api/trails`);
        const data = await response.json();
        trails = data.data;
        getBeaches();

    }

    async function getBeaches() {
        const response = await fetch("/beaches.json")
        const response2 = await fetch("/beachActivities.json");
        const data = await response.json();
        const data2 = await response2.json();



        beaches = data.elements
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
            <input bind:value={query} type="search" name="search" placeholder="Find Spots" autofocus />
        </fieldset>
    </form>

    {#if loaded}
        {#if query.length >= 2}
            {#each trails.filter((trail) => trail.name.toLowerCase().includes(query.toLowerCase())) as trail}
                <Trail trail={trail}></Trail>
                
            {/each}
            {#each beaches.filter((beach) => beach.tags.name.toLowerCase().includes(query.toLowerCase())) as beach}
                <Beach beach={beach}></Beach>
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