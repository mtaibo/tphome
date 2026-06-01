<script setup>

    import { ref, computed } from 'vue'
    import { useDevices } from '@/config/devices'
    import { useMap } from '@/config/map'

    import LightsLayer   from '@/components/blueprint/Lights.vue'
    import BlindsLayer   from '@/components/blueprint/Blinds.vue'
    import HouseLayer    from '@/components/blueprint/Map.vue'

    import BlindsControl from './BlindsControl.vue'

    const store = useDevices()
    const map = useMap()

    const selectedId = ref(null)
    const selectedBlind = computed(() => 
        selectedId.value ? store.blinds[selectedId.value] : null
    )

    const handleSelection = (id) => { selectedId.value = id }

</script>

<template>

    <div class="flex flex-col md:flex-row h-full w-full overflow-hidden">

        <!-- Dot background - top-20 to not be shown below topbar due to its oppacity -->
        <div class="fixed inset-0 md:top-20 bg-grid-dots pointer-events-none z-0"></div>

        <!-- Blueprint itself -->
        <div class="flex-1 flex items-center justify-center p-4 md:p-12 transition-all duration-500 ease-in-out min-h-0">
            <svg :viewBox="map.storage.viewBox ?? '0 0 0 0'" class="w-full h-auto max-w-3xl drop-shadow-2xl" xmlns="http://www.w3.org/2000/svg">
                <HouseLayer />
                <LightsLayer />
                <BlindsLayer @select="handleSelection" />
            </svg>
        </div>

        <!-- Desktop sidebar -->
        <aside 
            class="hidden md:block h-full border-l border-tp-border bg-tp-surface/20 backdrop-blur-md transition-all duration-500 ease-in-out overflow-hidden"
            :class="selectedBlind ? 'w-80 opacity-100' : 'w-0 opacity-0 border-none'"
        >
            <div class="w-80 h-full">
                <BlindsControl v-if="selectedBlind" :id="selectedId" :device="selectedBlind" @close="selectedId = null" />
            </div>
        </aside>


        <!-- Mobile -->
        <div 
            class="md:hidden fixed inset-x-0 bottom-0 z-50 transition-transform duration-500 ease-in-out"
            :class="selectedBlind ? 'translate-y-0' : 'translate-y-full'"
        >
            <!-- Overlay -->
            <div 
                v-if="selectedBlind"
                class="fixed inset-0 bg-black/40 backdrop-blur-sm -z-10"
                @click="selectedId = null"
            />

            <div class="bg-tp-surface border-t border-tp-border rounded-t-2xl pb-18 flex flex-col min-h-[60vh]">
                <!-- Handle -->
                <div class="flex justify-center pt-3 pb-1 shrink-0">
                    <div class="w-10 h-1 bg-tp-border rounded-full"></div>
                </div>
                <BlindsControl v-if="selectedBlind" :id="selectedId" :device="selectedBlind" @close="selectedId = null" class="flex-1 min-h-0" />
            </div>
        </div>

    </div>

</template>