<script>
    import Map from "./map.svelte";
    import { userData } from "$lib/userData";
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

    function addFav() {
        let currentFavs = $userData.favorites

        currentFavs = currentFavs.push(trail)
        console.log(currentFavs)

        userData.update((current => ({
            ...current,
            favorites: currentFavs
        })))

    }

</script>

<article class="trail-card">
    <Map class="map" coords={[lat, lon]} name={trail.name}></Map>

    <div class="trailInfo">
        <a href="/info?type=hike&id={trail.idKey}">
            <div class="trailBody">
                <h5 class="trailName">{trail.name}</h5>
                <small>Length: {trail.lengthMiles}mi {trail.dificulty}</small>
            </div>
        </a>

        <button onclick={addFav} id="favoriteButton" aria-label="Favorites">
            <i class="fa-regular fa-star"></i>
        </button>
    </div>
</article>

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
    #favoriteButton {
        background-color: transparent;
    }
    .trailInfo {
        color: var(--pico-text-color);
        display: flex;
        flex-direction: row;
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
