<article class="tracker">
    <h2>Forecast</h2>
    <div class="days">
        {#each { length: 7 } as _, index}
            <h3>7{index + 1}&deg</h3>
        {/each}
    </div>
    <small>this not real btw it fake</small>
</article>

<style>
    .tracker {
        display: flex;
        width: 100%;
        flex-direction: column;
        border-radius: 20px;
    }
    .days {
        display: flex;
        justify-content: space-between;
        width: 100%;
    }
</style>