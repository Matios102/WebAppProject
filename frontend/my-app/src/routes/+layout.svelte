<script>
    import { onMount } from "svelte";
    import { page } from "$app/stores";
    import HeaderMenu from "$lib/components/HeaderMenu.svelte";
    import '../styles/cardsStyle.css';
    import '../styles/pageStyle.css';
    import '../styles/filterStyle.css';
    import '../styles/popupStyle.css';
    import Notification from "$lib/components/Popups/Notification/Notification.svelte";

    let activeTab = "";

    $: {
        const path = $page.url.pathname;
        activeTab = path.substring(1);
    }

    onMount(() => {
        return () => unsubscribe();
    });
</script>

{#if $page.url.pathname !== "/login" && $page.url.pathname !== "/register" && $page.url.pathname !== "/" && $page.url.pathname !== "/pending-approval" && $page.url.pathname !== "/test"}
    <HeaderMenu/>
{/if}

<slot/>

<Notification/>

<style>
    :global(body) {
        margin: 0px;
    }
</style>
