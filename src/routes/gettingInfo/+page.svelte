<script>
    import { onMount } from 'svelte';
    import { page } from '$app/stores';
    import {userData} from '$lib/userData';
    import {goto} from '$app/navigation';
    let name = '';
    let island = '';
    let beachSafety = 0;
    let trailLength = 0;

    // Function to handle form submission
    function handleSubmit() {
        const userInfo = [
            name,
            island,
            beachSafety,
            trailLength
        ];

        for (let i = 0; i < userInfo.length; i++) {
            if (userInfo[i] === '' || userInfo[i] === null || userInfo[i] === undefined) {
                alert('Please fill out all fields before submitting.');
                return;
            }
        }
        userData.update((current) => ({
            ...current,
            name: userInfo[0],
            island: userInfo[1],
            swimSafety: userInfo[2],
            distance: userInfo[3]
        }));
        goto("");

        // You can send this data to a server or store it as needed
    }

    let container;
    
    // Optional: You can use onMount to perform any setup when the component is mounted
    onMount(() => {
        console.log('Getting Info Page Mounted');

        const boxes = document.querySelectorAll('.question');
        console.log(boxes);

        boxes.forEach((element) => {
            element.addEventListener('submit', () => {
                container.scrollTo({
                    top: element.offsetTop,
                    behavior: 'smooth'
                });
                console.log("wasd")
            });
        });
    });

</script>


<main id="main" bind:this={container}>
    <div class="title">
        <h1>
            hey cutie !
        </h1>
        <h2>lets get to know you</h2>
    </div>

    <div class="question">
        <h3>what is your name ?</h3>
        <input type="text" placeholder="your name" class="question-input" bind:value={name}/>
    </div>

    <div class="question">
        <h3>what island are you on ?</h3>
        <select class="question-input" bind:value={island}>

            <option value="">Select your island</option>
            <option value="island1">Big Island</option>
            <option value="island2">Maui</option>
            <option value="island3">Molokai</option>
            <option value="island4">Lanai</option>
            <option value="island5">Oahu</option>
            <option value="island6">Kauai</option>

        </select>
    </div>

    <div class="question">
        <h3>from 0 - 10 how safe do u want beaches ?</h3>
        <input type="range" placeholder="your rating" class="question-input" min=0 max=10 bind:value={beachSafety}/>
    </div>

    <div class="question">
        <h3>what would be the max trail length for you be ?</h3>
        <input type="range" placeholder="your rating" class="question-input" min=0 max=7 bind:value={trailLength}/>
    </div>

    <div class="question">
        <button  onclick={handleSubmit}>
            <h1>get started !</h1>
        </button>

    </div>

</main>

<style>
    main {
        display: flex;
        flex-direction: column;
        align-items: center;
        height: 100%;
        overflow-y: auto;
        flex-shrink: 0;
        height: 94vh;
        gap: 2rem;
        scroll-snap-type: y mandatory; /* Enforces snapping on the Y-axis */
        scroll-behavior: smooth; /* Adds smooth scrolling effect    */  
    }

    h1 {
        font-size: 3rem;
    }

    h2 {
        font-size: 2rem;
    }

    .title {
        text-align: center;
        width: 100%;
        height: 100vh;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
        position: sticky;
        scroll-snap-align: start; /* Snaps the top of the div to the top of the container */
    }

    .question {
        text-align: center;
        margin-top: 2rem;
        height: 100%;
        width: 100%;
        flex-shrink: 0;
        padding: 0 1rem;
        justify-content: center;
        align-content: center;
        scroll-snap-align: start; /* Snaps the top of the div to the top of the container */

    }

    .question-input {
        max-width: 75%;
        padding: 0.5rem;
        font-size: 1rem;
    }

</style>