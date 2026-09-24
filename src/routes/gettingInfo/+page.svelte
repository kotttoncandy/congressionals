<script>
    import { onMount } from 'svelte';
    import { page } from '$app/stores';
    import {userData} from '$lib/userData';
    import {goto} from '$app/navigation';
    let name = '';
    let island = '';
    let beachSafety = $state(10);
    let trailLength = $state(4);

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
        goto("/");

        // You can send this data to a server or store it as needed
    }

    let container;
    
    // Optional: You can use onMount to perform any setup when the component is mounted
    onMount(() => {
        console.log('Getting Info Page Mounted');

        const boxes = document.querySelectorAll('.question-input');
        console.log(boxes);

        boxes.forEach((element) => {
            element.addEventListener('submit', () => scrollNext());
        });
    });


    function scrollNext() {
        if (container) {
            container.scrollBy({
                top: window.innerHeight,
                behavior: 'smooth'
            });
        }
    }

    function getSafety(value) {
        if (value < 6) {
            return "not safe / only surfing"
        } else if (value < 7) {
            return "teenagers should be fine"
        } else {
            return "my baby cousin can swim here"
        }
    }
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
        <form action="" class="question-input">
            <input type="text" placeholder="your name" class="question-box" bind:value={name}/>
            <button type="submit" onclick={scrollNext}>
                <h3>next</h3>
            </button>
        </form>
    </div>

    <div class="question">
        <h3>what island are you on ?</h3>
        <form action="" class="question-input">
            <select class="question-box"  bind:value={island}>

                <option value="">Select your island</option>
                <option value="island1">Big Island</option>
                <option value="island2">Maui</option>
                <option value="island3">Molokai</option>
                <option value="island4">Lanai</option>
                <option value="island5">Oahu</option>
                <option value="island6">Kauai</option>

            </select>
            <button type="submit" onclick={scrollNext}>
                <h3>next</h3>
            </button>
        </form>

    </div>

    <div class="question">
        <h3>from 0 - 10 how safe do u want beaches ?</h3>
        <form action="" class="question-input">

            <input type="range" placeholder="your rating" class="question-box" min=0 max=10 bind:value={beachSafety}/>
            <h3>{beachSafety}</h3>
            <h3>{getSafety(beachSafety)}</h3>

            <button type="submit" onclick={scrollNext}>
                <h3>next</h3>
            </button>
        </form>
    </div>

    <div class="question">
        <h3>what would be the max trail length for you be ?</h3>
        <form action="" class="question-input">
            <input type="range" placeholder="your rating" class="question-box" min=0 max=7 bind:value={trailLength}/>
            <h3>
                {trailLength}
                {#if trailLength < 1}
                mile

                {/if}
                
                {#if trailLength < 7 && trailLength > 1}
                    miles
                {/if}

                {#if trailLength == 7}
                    + miles
                {/if}
            </h3>
            <button type="submit" onclick={scrollNext}>
                <h3>next</h3>
            </button>
        </form>
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
        max-width: 100%;
        padding: 0.5rem;
        font-size: 1rem;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;

    }

    .question-input button {
        width: 25%;
        height: 3rem;
        display: inline-flex;
        justify-content: center; /* Centers text horizontally */
        align-items: center;     /* Centers text vertically */    
        padding-top: 1.5rem
    }

    .question-box {
        max-width: 50%;
        padding: 1rem;
        font-size: 1rem;
    }

</style>