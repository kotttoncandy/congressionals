<script>
    import { onMount } from 'svelte';

    let { coords = [21.3867, -157.9739], name = ""} = $props();

    let mapElement;
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



</style>