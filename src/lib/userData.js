import { writable } from "svelte/store";

export const userData = writable({
    lat: 0,
    lon: 0,
    island: "oahu",
    experience: "easy",
    beachActivities: [
        "swimming"
    ]
})