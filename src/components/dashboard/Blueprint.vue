<script setup>

    import { ref } from 'vue'

    import LightsLayer   from './layers/LightsLayer.vue'
    import BlindsLayer   from './layers/BlindsLayer.vue'
    import HouseLayer    from './layers/HouseLayer.vue'

    import BlindsControl from '../layout/BlindsControl.vue'

    const selectedBlind = ref(null)

    const handleSelection = (device) => {
        selectedBlind.value = device
    }

</script>

<template>

    <div class="flex h-[calc(100vh-5rem)] w-full overflow-hidden">
    
        <div class="flex-1 flex items-center justify-center p-12 transition-all duration-500 ease-in-out">

            <svg viewBox="0 0 500 450" class="w-full h-auto max-w-3xl drop-shadow-2xl" xmlns="http://www.w3.org/2000/svg">

                <HouseLayer />
                <LightsLayer />
                <BlindsLayer @select="handleSelection" />

            </svg>

        </div>

        <aside 
            class="h-full border-l border-tp-border bg-tp-surface/20 backdrop-blur-md transition-all duration-500 ease-in-out overflow-hidden"
            :class="selectedBlind ? 'w-80 opacity-100' : 'w-0 opacity-0 border-none'"
        >

            <div class="w-80 h-full">

                <BlindsControl 
                    v-if="selectedBlind"
                    :device="selectedBlind" 
                    @close="selectedBlind = null" 
                />

            </div>

        </aside>

  </div>

</template>