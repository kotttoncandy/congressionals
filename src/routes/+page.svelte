<script>
    import { onMount } from "svelte";
    import { trails } from "../lib/trailData";
    import { beaches } from "../lib/beachData"
    import SiteHeader from "$lib/components//siteHeader.svelte";
    import MainSlider from "$lib/components//mainSlider.svelte";
    import BeachSlider from "$lib/components/beachSlider.svelte";
    import Footer from "$lib/components/footer.svelte";
    import Tracker from "$lib/components//tracker.svelte";
    import { userData } from "$lib/userData";
    var index = $state(0);
    let loading = $state(true);
    var distances = [

    ]

    function distanceMiles(lat1, lon1, lat2, lon2) {
        const R = 3958.8; // Earth's radius in miles

        const toRadians = degrees => degrees * Math.PI / 180;

        const dLat = toRadians(lat2 - lat1);
        const dLon = toRadians(lon2 - lon1);

        const a =
            Math.sin(dLat / 2) ** 2 +
            Math.cos(toRadians(lat1)) *
            Math.cos(toRadians(lat2)) *
            Math.sin(dLon / 2) ** 2;

        const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));

        return R * c;
    }

    async function getLocation() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(showPosition, showError);
        } else { 
            alert("location cannot be determined")
        }
    }

    function showPosition(position) {
        userData.update(current => ({
            ...current,
            lat: position.coords.latitude,
            lon: position.coords.longitude
        }));
    }

    function showError() {
        alert("location cannot be determined")
    }

    async function getTrails() {
        const response = await fetch(`/api/trails`);
        const data = await response.json();
        trails.set(data.data);
        console.log(data.data)
        const ISLAND = $trails.filter((trail) => trail.island === "OAHU" && trail.closed === false);

        trails.set(ISLAND);
        $trails.forEach(element => {
            distances[element.idKey] = distanceMiles(
                element.coords.latitude, element.coords.longitude, 
                $userData.lat, $userData.lon
            )   
        });

        const sortByDistance = $trails.sort((a, b) => distances[a.idKey] - distances[b.idKey]);
        trails.set(sortByDistance)
        console.log(sortByDistance)
        getBeaches()
    }
    async function getBeaches() {
        const response = await fetch("/beaches.json");
        const data = await response.json();
        console.log(data)
        beaches.set(data.elements);
        const ISLAND = $beaches.filter((beach) => beach.island === "OAHU");
        beaches.set(ISLAND);
        loading = false;
    }
    onMount(() => {
        getTrails();
        getLocation();
    });
</script>

<main id="main">
    <SiteHeader></SiteHeader>
    <div class="mainContent">

        {#if loading}
            <article class="loading" aria-busy="true">Loading trails...</article>
        {:else}
        <!--
        <form class="searchBar">
            <fieldset role="group">
                <input
                    type="search"
                    name="search"
                    placeholder="Seach Places"
                />
                <input type="submit" value="Go!" />
            </fieldset>
        </form>
        -->
            <Tracker></Tracker>
            <h4>Hikes near you:</h4>
            <div class="slider">
                <MainSlider trail={$trails[index]}></MainSlider>
                <MainSlider trail={$trails[index+1]}></MainSlider>
            </div>
            <div class="slider" id="beachSlider">
                <BeachSlider beach={$beaches[index]}></BeachSlider>
                <BeachSlider beach={$beaches[index + 1]}></BeachSlider>
            </div>
        {/if}
    </div>

    <div class="gap"></div>
    <Footer></Footer>
</main>

<style>
    #main {
        display: flex;
        flex-direction: column;
        justify-content: center;
    }

    .slider {
        display: flex;
        flex-direction: row;
        gap: 20px;
        overflow-x: scroll;
    }

    .slider button {
        width: 20px;
        height: 30px;
        font-size: 25px;
        display: flex;
        justify-content: center;
        align-items: center;
        border-radius: 100px;
        background-color: transparent;
        border: none;
    }
    .mainContent {
        margin-top: 0px;
        padding: 20px;
        padding-top: 0px;
        border-radius: 20px;
    }
    .mainContent * {
        border-radius: inherit;
    }
    form {
        margin-bottom: 0px;
    }
    h4 {
        margin-top: 0;
        margin-bottom: 1rem;

    }
    .searchBar {
        border-radius: 20px;
    }
    #beachSlider {
        margin-bottom: 50px;
    }


</style>
