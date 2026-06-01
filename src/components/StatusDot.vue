<script setup>

    import { apiOnline } from '@/config/socket'

</script>

<template>

    <div
        class="md:hidden fixed top-4 left-4 z-50 w-2.5 h-2.5 rounded-full shadow-[0_0_8px] animate-pulse transition-all duration-500"
        :class="apiOnline ? 'bg-tp-ok shadow-tp-ok/50' : 'bg-tp-danger shadow-tp-danger/50'"
    ></div>

</template>