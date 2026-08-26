<script>
    var coords;
    var lat = $state(0);
    var lon = $state(0);
    let { beach } = $props();
    let image = $state("");
    import Map from "./map.svelte";
    import { distances } from "$lib/spotDistances";
    import { beaches } from "$lib/beachData";
    let beachData = $beaches.data[beach.id]
    const clamp = (val, min, max) => Math.min(Math.max(val, min), max);

    $effect(() => {
        if ("center" in beach) {
            lat = beach.center.lat;
            lon = beach.center.lon;
        } else {
            lat = beach.lat;
            lon = beach.lon;
        }
        beachData = $beaches.data[beach.id]


        const controller = new AbortController();
        getCity(controller.signal);
        return () => controller.abort();
    });


    let city = $state("");
    async function getCity(signal) {
        try {
            var url = `https://geocode.maps.co/reverse?lat=${lat}&lon=${lon}&api_key=6a8222ab2ccce825459342ktlc36bca&format=json`;
            const response = await fetch(url);
            console.log(url);

            const data = await response.json();
            city =
                data.address.city ??
                data.address.suburb ??
                data.address.town ??
                data.address.village ??
                data.address.road ??
                data.address.county ??
                data.address.island ??
                "idek gng";
        } catch (err) {
            console.log(err);
        }
    }

</script>

<article class="beach-card">
    <Map coords={[lat, lon]}></Map>
    <div class="beachInfo">
        <h5 class="beachName">{beach.tags.name}</h5>
        <small>Swim Score: {clamp(beachData.swimming_safety.score + 50, -100, 100)}</small>
    </div>

</article>

<style>
    .beach-card {
        display: flex;
        width: 100%;
        height: 50dvh;
        flex-direction: column;
        padding: 20px;
        flex-shrink: 0;
        gap: 10px;
        border-radius: 20px;
        justify-content: space-between;
        background-color: transparent;
    }
    .beachImage {
        max-height: 100%;
    }
    .activities {
        overflow-y: scroll;
    }
    .imageDiv {
        height: 50%;
    }
    .beachInfo {
        color: var(--beach-text-color);
    }

    .beachInfo * {
        color: inherit;
    }
</style>
