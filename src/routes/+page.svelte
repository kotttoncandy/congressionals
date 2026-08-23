<script>
    import { onMount } from "svelte";
    import { trails } from "../lib/trailData";
    import { beaches } from "../lib/beachData";
    import SiteHeader from "$lib/components//siteHeader.svelte";
    import Trail from "$lib/components/Trail.svelte";
    import Beach from "$lib/components/Beach.svelte";
    import Footer from "$lib/components/footer.svelte";
    import Tracker from "$lib/components//tracker.svelte";
    import { userData } from "$lib/userData";
    import { distances } from "$lib/spotDistances";
    var index = $state(0);
    let loading = $state(true);
    const trailDistances = [];
    const beachDistances = new Map();

    function distanceMiles(lat1, lon1, lat2, lon2) {
        const R = 3958.8; // Earth's radius in miles

        const toRadians = (degrees) => (degrees * Math.PI) / 180;

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
            const res = await fetch("https://ipapi.co/json/");
            const location = await res.json();

            userData.update((current) => ({
                ...current,
                lat: location.latitude,
                lon: location.longitude,
            }));
        }
    }

    function showPosition(position) {
        userData.update((current) => ({
            ...current,
            lat: position.coords.latitude,
            lon: position.coords.longitude,
        }));
    }

    async function showError() {
        const res = await fetch("https://ipapi.co/json/");
        const location = await res.json();

        userData.update((current) => ({
            ...current,
            lat: location.latitude,
            lon: location.longitude,
        }));
    }

    async function getTrails() {
        
        const response = await fetch(`/api/trails`);
        const data = await response.json();
        trails.set(data.data);
        console.log(data.data);
        const ISLAND = $trails.filter(
            (trail) =>
                trail.island === "OAHU" &&
                trail.closed === false &&
                trail.lengthMiles != null &&
                trail.lengthMiles <= $userData.distance,
        );

        trails.set(ISLAND);
        $trails.forEach((element) => {
            trailDistances[element.idKey] = distanceMiles(
                element.coords.latitude,
                element.coords.longitude,
                $userData.lat,
                $userData.lon,
            );
        });

        distances.update((current) => {
            trail: trailDistances;
        });

        const sortByDistance = $trails.sort(
            (a, b) => distances[a.idKey] - distances[b.idKey],
        );
        trails.set(sortByDistance);
        console.log(sortByDistance);
        getBeaches();
    }

    function get_coordinates(beach) {
        if (beach.type == "node") {
            let lat = beach.lat;
            let lon = beach.lon;
            return [lat, lon];
        } else {
            let lat = beach.center.lat;
            let lon = beach.center.lon;
            return [lat, lon];
        }
    }

    async function getBeaches() {
        const response = await fetch("/beaches.json")
        const response2 = await fetch("/beachActivities.json");
        const data = await response.json();
        const data2 = await response2.json();



        const ISLAND = data.elements.filter((beach) => beach.island === "OAHU" && data2[beach.id].swimming_safety.score > 40);
        beaches.update((current) => ({
            names: ISLAND,
            data: data2
        }));
        $beaches.names.forEach((beach) => {
            beachDistances.set(
                beach.id,
                distanceMiles(
                    get_coordinates(beach)[0],
                    get_coordinates(beach)[1],
                    $userData.lat,
                    $userData.lon,
                ),
            );
            distances.update((current) => ({
                ...current,
                beach: beachDistances
            }))
        });
        const sortedBeaches = [...$beaches.names].sort((a, b) => {
            const distanceA = beachDistances.get(a.id);
            const distanceB = beachDistances.get(b.id);

            return distanceA - distanceB;
        });
        beaches.update((current) => ({
            ...current,
            names: sortedBeaches
        }));
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
            <article class="loading" aria-busy="true">Loading spots...</article>
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
            <form>
                <fieldset role="group">
                    <input
                        type="search"
                        name="search"
                        placeholder="Find Spots"
                    />
                </fieldset>
            </form>
            <h4>Spots near you:</h4>
            <div class="slider">
                <Trail trail={$trails[index]}></Trail>
                <Beach beach={$beaches.names[index]}></Beach>
                <Trail trail={$trails[index + 2]}></Trail>
                <Beach beach={$beaches.names[index + 1]}></Beach>
                <Trail trail={$trails[index + 1]}></Trail>
                <Beach beach={$beaches.names[index + 2]}></Beach>
            </div>
        {/if}
    </div>
</main>

<style>
    #main {
        display: flex;
        flex-direction: column;
        justify-content: center;
    }

    .slider {
        display: flex;
        flex-direction: column;
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
