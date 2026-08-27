import { writable } from "svelte/store";

export const userData = writable({
    lat: 0,
    lon: 0,
    island: "oahu",
    experience: "easy",
    beachActivities: [
        "swimming"
    ],
    distance: 4,
    swimSafety: 20,
    favTrails: [],
    favBeach: []
})