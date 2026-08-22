<script>
    import { onMount } from 'svelte';

    let { coords = [21.3867, -157.9739], name = ""} = $props();

    let mapElement;

    onMount(async () => {
        const L = await import('leaflet');

        const map = L.map(mapElement, {
            maxZoom: 18,
            minZoom: 10
        }).setView(coords, 13);

        L.maplibreGL({
            style: 'https://tiles.openfreemap.org/styles/liberty',
        }).addTo(map)

        L.marker(coords)
            .addTo(map)
            .bindPopup(name);


        return () => {
            map.remove();
        };
    });
</script>

<iframe
    src={`https://www.google.com/maps?q=${coords[0]},${coords[1]}&t=k&output=embed`}
    style="border:0;"
    allowfullscreen=""
    loading="lazy"
    title="map"
></iframe>
<style>
    iframe {
        width: 100%;
        height: calc(100% + 40px);
        border-radius: 20px;

    }

    :global(.leaflet-control-zoom) {
        display: flex;
        flex-direction: row;
        gap: 6px;
        background: transparent;
        border: none !important;
    }

    :global(.leaflet-control-zoom a) {
        display: flex;
        width: 38px !important;
        height: 38px !important;
        line-height: 38px !important;
        border-radius: 10px !important;
        border: none !important;
        background: white;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.18);
        color: #333;
        align-items: center;
        justify-content: center;
        
    }

    :global(.leaflet-marker-icon) {
        background-color: transparent;
        border: none;
    }

</style>