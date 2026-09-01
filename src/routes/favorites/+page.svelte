<script>
    import Footer from "$lib/components/footer.svelte";
    import Trail from "$lib/components/Trail.svelte";
    import Beach from "$lib/components/Beach.svelte";
    import { userData } from "$lib/userData";
    
</script>

<main>
    <header class="header">
        <div>
            <h1>its ur favs!</h1>
            <small>lets relive a memory</small>
        </div>

    </header>
    <div class="favDIv">
        {#if $userData.favTrails.length == 0 && $userData.favBeach.length == 0 }
            <h3>no favs at this moment</h3>
        {:else}
            {#each $userData.favTrails as item}
                <Trail trail={item}></Trail>
            {/each}

            {#each $userData.favBeach as item}
                <Beach beach={item}></Beach>
            {/each}
        {/if}
    </div>
</main>

<style>
    .favDIv {
        display: flex;
        flex-direction: column;
        padding: 20px

    }
    main {
    }
    .header {
        display: flex;
        width: 100dvw;
        padding: 20px;
        padding-top: 40px;
        padding-bottom: 0px;
        align-items: center;
    }
    .header div h1{
        margin-bottom: 4px;
    }
    .header div small{
        margin-bottom: 10px;
    }
</style>