<script>
    var coords;
    var lat = 0;
    var lon = 0;
    let { beach } = $props();
    let image = $state("");

    $effect(() => {
        if ("center" in beach) {
            lat = beach.center.lat;
            lon = beach.center.lon;
        } else {
            lat = beach.lat;
            lon = beach.lon;
        }

        const controller = new AbortController();
        getCity(controller.signal);

        if (beach.tags?.name) {
            getImage(beach.tags.name);
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

<article class="beach-card">
    <div class="beachInfo">
        <h5 class="beachName">{beach.tags.name}</h5>
        <p>
            Located in: {city}
        </p>
    </div>

    <div class="imageDiv">
        {#if image}
            <img class="beachImage" src={image} alt={beach.tags.name} />
        {:else}
            <div aria-busy="true">Loading image...</div>
        {/if}
    </div>
</article>

<style>
    .beach-card {
        display: flex;
        width: 100%;
        height: 50dvh;
        flex-direction: row;
        padding: 20px;
        flex-shrink: 0;
        gap: 10px;
        border-radius: 20px;
        justify-content: space-between;
        background-color: var(--beach-color);
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
