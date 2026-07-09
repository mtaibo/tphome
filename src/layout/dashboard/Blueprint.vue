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

    <div class="h-full w-full overflow-hidden min-h-0">

        <!-- Blueprint -->
        <div class="flex items-center justify-center p-5 md:p-10 h-full">
            <svg
                :viewBox="map.storage.viewBox ?? '0 0 0 0'"
                class="w-full h-auto max-w-3xl"
                xmlns="http://www.w3.org/2000/svg"
            >
                <HouseLayer />
                <LightsLayer />
                <BlindsLayer @select="handleSelection" />
            </svg>
        </div>

        <!-- Popup (bottom sheet on mobile, centered modal on desktop) -->
        <Teleport to="body">
            <Transition name="popup">
                <div
                    v-if="selectedBlind"
                    class="blinds-popup-overlay"
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
