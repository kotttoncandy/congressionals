<script>
    import Map from "./map.svelte";
    var coords;
    var lat = $state(0);
    var lon = $state(0);
    let { trail } = $props();
    let image = $state("");
    let description = $state("");

    $effect(() => {
        coords = trail.coords;
        lat = coords.latitude;
        lon = coords.longitude;
        const controller = new AbortController();
        getCity(controller.signal);
        if (trail?.name) {
            getImage(trail.name);
        }

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



    async function getImage(name) {
        const response = await fetch(
            `https://commons.wikimedia.org/w/api.php?action=query&generator=search&gsrsearch=${encodeURIComponent(name)}&gsrnamespace=6&gsrlimit=1&prop=imageinfo&iiprop=url&iiurlwidth=800&format=json&origin=*`,
        );
        console.log(
            `https://commons.wikimedia.org/w/api.php?action=query&generator=search&gsrsearch=${encodeURIComponent(name)}&gsrnamespace=6&gsrlimit=1&prop=imageinfo&iiprop=url&iiurlwidth=800&format=json&origin=*`,
        );

        const data = await response.json();

        const pages = data.query?.pages;

        if (!pages) {
            image = "";
            return;
        }

        const page = Object.values(pages)[0];

        image = page.imageinfo?.[0]?.thumburl ?? "";
    }

</script>
<a href="/info?type=hike&id={trail.idKey}">
<article class="trail-card">
    <Map class="map" coords={[lat, lon]} name={trail.name}></Map>

    <div class="trailInfo">
        <h5 class="trailName">{trail.name}</h5>
        <small>Length: {trail.lengthMiles}mi {trail.dificulty}</small>
    </div>



</article>

</a>

<style>
    .trail-card {
        display: flex;
        width: 100%;
        height: 50dvh;
        flex-direction: column;

        flex-shrink: 0;
        gap: 10px;
        border-radius: 20px;
        justify-content: space-between;
        background-color: transparent;
    }
    .map {

    }
    .trailInfo {
        color: var(--pico-text-color);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .trailInfo * {
        color: inherit;
    }

    .trailImage {
        max-height: 100%;
    }
    .activities {
        overflow-y: scroll;
    }

    .description {
        overflow-y: scroll;
        max-height: 80%;
    }
</style>
