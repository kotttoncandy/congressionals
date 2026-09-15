<script>
	import { onNavigate } from '$app/navigation';
	import favicon from '$lib/assets/favicon.svg';
	import Footer from '$lib/components/footer.svelte';
	import { userData } from "$lib/userData.js";
	import {onMount} from "svelte";
	import {beaches} from "$lib/beachData.js";
	let { children } = $props();
	let previous = $userData;
    const beachDistances = new Map();
    import { distances } from "$lib/spotDistances";
	

    function get_coordinates(beach) {
        if (beach.type == "node") {
            let lat = beach.lat;
            let lon = beach.lon;
            return [lat, lon];
        } else {
            let lat = beach.center.lat;
            let lon = beach.center.lon;
            return [lat, lon];
        }
    }

    function distanceMiles(lat1, lon1, lat2, lon2) {
        const R = 3958.8; // Earth's radius in miles

        const toRadians = (degrees) => (degrees * Math.PI) / 180;

        const dLat = toRadians(lat2 - lat1);
        const dLon = toRadians(lon2 - lon1);

        const a =
            Math.sin(dLat / 2) ** 2 +
            Math.cos(toRadians(lat1)) *
                Math.cos(toRadians(lat2)) *
                Math.sin(dLon / 2) ** 2;

        const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));

        return R * c;
    }


	onNavigate((navigation) => {
		if (!document.startViewTransition) return;

		return new Promise((resolve) => {
			document.startViewTransition(async () => {
				resolve();
				await navigation.complete;
			});
		});
	});

	userData.subscribe((value) => {
		if (value != previous) {
			previous = value;
			localStorage.setItem("userData", JSON.stringify(value));
			console.log(value.favTrails)
		}

	});

    function setUserData() {
        if (localStorage.getItem("userData")) {
            userData.set(JSON.parse(localStorage.getItem("userData")));
        }

		getBeaches()

    }

	onMount(() => {
		setUserData();
		

	});

	async function getBeaches() {
        const response = await fetch("/beaches.json")
        const response2 = await fetch("/beachActivities.json");
        const data = await response.json();
        const data2 = await response2.json();



        const ISLAND = data.elements.filter((beach) => beach.island === $userData.island.toUpperCase() && data2[beach.id].swimming_safety.score > $userData.swimSafety);
        beaches.update((current) => ({
            names: ISLAND,
            data: data2
        }));
        $beaches.names.forEach((beach) => {
            beachDistances.set(
                beach.id,
                distanceMiles(
                    get_coordinates(beach)[0],
                    get_coordinates(beach)[1],
                    $userData.lat,
                    $userData.lon,
                ),
            );
            distances.update((current) => ({
                ...current,
                beach: beachDistances
            }))
        });
        const sortedBeaches = [...$beaches.names].sort((a, b) => {
            const distanceA = beachDistances.get(a.id);
            const distanceB = beachDistances.get(b.id);

            return distanceA - distanceB;
        });
        beaches.update((current) => ({
            ...current,
            names: sortedBeaches
        }));
    }

</script>

<svelte:head>
	<link rel="icon" href={favicon} />
	

</svelte:head>
<div class="app">
	<main class="mainApp">
		{@render children()}
	</main>
	
	<Footer></Footer>
</div>


<style>
  .app {
    display: flex;
    flex-direction: column;
	min-height: 100vh;
    gap: 1rem;
  }

  .mainApp {
	padding-bottom: 2rem;
  }
</style>