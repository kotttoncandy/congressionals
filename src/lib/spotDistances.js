import { writable } from "svelte/store";

export let distances = writable({
    trail: [],
    beach: new Map(),
})