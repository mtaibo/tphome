<script setup>

    import { ref } from 'vue'

    import LightsLayer from './layers/LightsLayer.vue'
    import BlindsLayer from './layers/BlindsLayer.vue'
    import HouseLayer  from './layers/HouseLayer.vue'

</script>

<template>

    <div class="w-full h-full flex items-center justify-center p-8">

        <svg viewBox="0 0 500 450" class="w-full h-auto max-w-3xl" xmlns="http://www.w3.org/2000/svg">

            <HouseLayer  />
            <LightsLayer />
            <BlindsLayer />

        </svg>

    </div>

</template>