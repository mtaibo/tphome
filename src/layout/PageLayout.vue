
<template>

    <div class="flex w-screen overflow-clip font-sans bg-tp-bg text-tp-text page-root">

        <slot></slot>

    </div>

</template>

<style scoped>
@reference "tailwindcss";

    .page-root {
        height: 100dvh;
    }

    @media (display-mode: standalone) {
        .page-root {
            height: calc(100dvh + env(safe-area-inset-top) + env(safe-area-inset-bottom));
        }
    }

</style>