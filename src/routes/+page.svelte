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
    import { goto } from '$app/navigation';


    var index = $state(0);
    let loading = $state(true);
    const trailDistances = [];
    const beachDistances = new Map();
    let resultArr = $state([])
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


    function getHawaiianIsland(lon, lat) {
        const islands = {
            Niihau: {
                minLon: -160.3,
                maxLon: -159.5,
                minLat: 21.7,
                maxLat: 22.1
            },
            Kauai: {
                minLon: -159.8,
                maxLon: -159.2,
                minLat: 21.8,
                maxLat: 22.3
            },
            Oahu: {
                minLon: -158.3,
                maxLon: -157.6,
                minLat: 21.2,
                maxLat: 21.8
            },
            Molokai: {
                minLon: -157.4,
                maxLon: -156.6,
                minLat: 21.0,
                maxLat: 21.3
            },
            Lanai: {
                minLon: -157.1,
                maxLon: -156.8,
                minLat: 20.7,
                maxLat: 21.0
            },
            Maui: {
                minLon: -156.8,
                maxLon: -155.9,
                minLat: 20.5,
                maxLat: 21.1
            },
            Hawaii: {
                minLon: -156.1,
                maxLon: -154.7,
                minLat: 18.9,
                maxLat: 20.3
            }
        };

        for (const [island, box] of Object.entries(islands)) {
            if (
                lon >= box.minLon &&
                lon <= box.maxLon &&
                lat >= box.minLat &&
                lat <= box.maxLat
            ) {
                return island;
            }
        }

        return null;
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

    function setUserData() {
        if (localStorage.getItem("userData")) {
            userData.set(JSON.parse(localStorage.getItem("userData")));
            userData.update((current) => ({
                ...current,
                island: getHawaiianIsland(current.lon, current.lat)
            }))
        } else {
            goto("gettingInfo");

        }


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



        const ISLAND = data.elements.filter((beach) => data2[beach.id].swimming_safety.score > $userData.swimSafety);
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
        resultArr = interweave($trails, $beaches)
        console.log($trails)

    }


    onMount(() => {
        if ($beaches.names.length > 0) {
            loading = false

        } else {
            getTrails();
            getLocation();
        }
        
        setUserData()
        if ($trails.length > 0 && $beaches.names.length > 0) {
            resultArr = interweave($trails, $beaches)
        }

    });

    function changePage() {
        goto("search");
    }

    function interweave(a1, a2) {
        var maxLength = Math.max(a1.length, a2.names.length)
        var array = []
        for (let i = 0; i < maxLength; i++) {
            if (i < a1.length) {
                array.push({
                    a: a1[i],
                    t: "trail"
                })
            }

            if (i < a2.names.length) {
                array.push({
                    a: a2.names[i],
                    t: "beach"
                })
            }
        }
        return array
    }
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
            <form on:click={changePage} class="findSpots">
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
                {#if $trails.length > 0 && $beaches.names.length > 0}
                    {#each resultArr as t, i}
                        {#if i < 10}
                            {#if t.t == "trail"}
                                <Trail trail={t.a}></Trail>

                            {:else}
                                <Beach beach={t.a}></Beach>
                            {/if}
                        {/if}
                        
                    {/each}
                {/if}


            </div>
        {/if}
    </div>
</main>

<style>
    #main {
        display: flex;
        flex-direction: column;
        justify-content: center;
                overflow-x: hidden;

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
        width: 100%;
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
    #beachSlider {
        margin-bottom: 50px;
    }
    .findSpots {
        view-transition-name: findSpots;
    }
</style>
