import { userData } from './userData.js';
import {get} from 'svelte/store';
userData.subscribe((value) => {
    localStorage.setItem("userData", JSON.stringify(value));
    console.log(value.favTrails)
});