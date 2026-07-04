
<template>

    <div class="flex h-svh w-screen overflow-clip font-sans bg-tp-bg text-tp-text page-root">

        <slot></slot>

    </div>

</template>

<style scoped>
@reference "tailwindcss";

    :global(.is-standalone) .page-root {
        height: 100dvh;
    }

</style>