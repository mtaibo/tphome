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

    <div class="flex flex-col md:flex-row h-full w-full overflow-hidden min-h-0">

        <!-- Dot background - top-20 to not be shown below topbar due to its oppacity -->
        <div class="fixed inset-0 md:top-20 bg-grid-dots pointer-events-none z-0"></div>

        <!-- Blueprint itself -->
        <div class="flex-1 flex items-center justify-center p-4 md:p-12 md:pb-12 transition-all duration-500 ease-in-out min-h-0">
                <svg :viewBox="map.storage.viewBox ?? '0 0 0 0'" class="w-full h-full max-h-full max-w-3xl drop-shadow-2xl" xmlns="http://www.w3.org/2000/svg">
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


        <!-- Mobile popup -->
        <Teleport to="body">
            <div 
                v-if="selectedBlind"
                class="blinds-popup-overlay md:hidden"
                @click.self="selectedId = null"
            >
                <div class="blinds-popup">
                    <BlindsControl :id="selectedId" :device="selectedBlind" @close="selectedId = null" />
                </div>
            </div>
        </Teleport>

    </div>

</template>
