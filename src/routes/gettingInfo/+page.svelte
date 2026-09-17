
<main>
    <div class="title">
        <h1>
            hey cutie !
        </h1>
        <h2>lets get to know you</h2>
    </div>

    <div class="question">
        <p>what is your name ?</p>
        <input type="text" placeholder="your name" />
    </div>

</main>

<style>
    main {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 100%;
        overflow-y: auto;
        flex-shrink: 0;
    }

    h1 {
        font-size: 3rem;
    }

    h2 {
        font-size: 2rem;
    }

    .title {
        text-align: center;
        position: sticky;
        width: 100%;
        height: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
        
    }

    .question {
        text-align: center;
        margin-top: 2rem;
        height: 100%;
        width: 100%;
        flex-shrink: 0;
    }

</style>