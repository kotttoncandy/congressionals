<footer class="bottom-nav">
    <nav>
        <a href="/" aria-label="Home">
            <i class="fa-solid fa-house"></i>
        </a>

        <a href="/search" aria-label="Search">
            <i class="fa-solid fa-magnifying-glass"></i>
        </a>

        <a href="/favorites" aria-label="Favorites">
            <i class="fa-regular fa-star"></i>
        </a>
    </nav>
</footer>

<style>

    .bottom-nav {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        padding: 0.5rem;
        margin: 0;
    }

    .bottom-nav nav {
        display: flex;
        align-items: center;
        max-width: 175px;
        margin: auto;
        gap: 20px;
        justify-content: space-evenly;
        transition: max-width 0.3s ease 0s;
        padding-left: 10px;
        padding-right: 10px;

    }

    .bottom-nav nav:hover {
        max-width: 300px;
    }
    .bottom-nav nav:not(:hover) {
        max-width: 225px;
        transition-delay: 0.1s;
    }

    .bottom-nav a {
        font-size: 1.5rem;
        padding: 0.5rem;
    }
    a {
        color: white;
    }
    nav {
        background-color: var(--footer-background-color);
        border-radius: 20px;
    }
</style>
