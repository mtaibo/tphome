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

    const mapDims = computed(() => {
        const parts = (map.storage.viewBox ?? '0 0 100 100').split(' ').map(Number)
        const w = parts[2] || 100
        const h = parts[3] || 100
        return { w, h, rx: Math.round(Math.min(w, h) * 0.05) }
    })

</script>

<template>

    <div class="flex flex-col md:flex-row h-full w-full overflow-hidden min-h-0">

        <!-- Blueprint itself -->
        <div class="flex-1 flex items-center justify-center p-5 md:p-10 transition-all duration-500 ease-in-out">
            <svg
                :viewBox="map.storage.viewBox ?? '0 0 0 0'"
                class="w-full h-auto max-w-3xl"
                xmlns="http://www.w3.org/2000/svg"
            >
                <defs>
                    <clipPath id="map-clip">
                        <rect x="0" y="0" :width="mapDims.w" :height="mapDims.h" :rx="mapDims.rx" :ry="mapDims.rx" />
                    </clipPath>
                </defs>

                <!-- All content clipped to rounded corners -->
                <g clip-path="url(#map-clip)">
                    <HouseLayer />
                    <LightsLayer />
                    <BlindsLayer @select="handleSelection" />
                </g>

                <!-- Subtle border hinting the map boundary -->
                <rect :x="0.75" :y="0.75"
                      :width="mapDims.w - 1.5" :height="mapDims.h - 1.5"
                      :rx="mapDims.rx" :ry="mapDims.rx"
                      fill="none"
                      stroke="rgba(255,255,255,0.10)" stroke-width="1.5" />

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
            <Transition name="popup">
                <div
                    v-if="selectedBlind"
                    class="blinds-popup-overlay md:hidden"
                    @click.self="selectedId = null"
                >
                    <div class="blinds-popup">
                        <BlindsControl :id="selectedId" :device="selectedBlind" @close="selectedId = null" />
                    </div>
                </div>
            </Transition>
        </Teleport>

    </div>

</template>
