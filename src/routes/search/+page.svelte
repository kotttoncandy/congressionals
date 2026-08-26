<script>
    import Footer from "$lib/components/footer.svelte";
    import SiteHeader from "$lib/components/siteHeader.svelte";
</script>


<main>
    <h1 style="padding-top: 20px;" class="pageTitle">Seach Away!</h1>
    <form class="findSpots">
        <fieldset role="group">
            <input type="search" name="search" placeholder="Find Spots" />
        </fieldset>
    </form>
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