<script setup>

    import { ref, watch } from 'vue'
    import { X, Check, Cpu } from 'lucide-vue-next'
    import { useMap } from '@/config/map'
    import { useDevices } from '@/config/devices'
    import { api } from '@/config/api'
    import HouseLayer  from '@/components/blueprint/Map.vue'
    import LightsLayer from '@/components/blueprint/Lights.vue'
    import BlindsLayer from '@/components/blueprint/Blinds.vue'
    import Btn from '@/components/Btn.vue'

    const props = defineProps({
        device: { type: Object, default: null }
    })
    const emit = defineEmits(['done', 'cancel'])

    const map   = useMap()
    const store = useDevices()

    const pickedId = ref(null)
    const picking  = ref(false)

    function onPick(id) { pickedId.value = id }

    async function confirm() {
        if (!pickedId.value) return
        picking.value = true
        try {
            const category = Object.keys(store.storage).find(cat => pickedId.value in store.storage[cat])
            if (!category) return
            await api.configurePending(props.device.mac, pickedId.value, store.storage[category][pickedId.value].prefs)
            emit('done')
        } catch (e) {
            console.error('TPHome - Config error:', e)
        } finally {
            picking.value = false
        }
    }

    watch(() => props.device, async (d) => {
        if (!d) { pickedId.value = null; return }
        if (Object.keys(store.storage).length === 0) await store.setup()
    }, { immediate: true })

</script>

<template>

    <Teleport to="body">
        <Transition name="popup">
            <div v-if="device" class="map-popup-overlay" @click.self="emit('cancel')">
                <div class="map-popup">

                    <!-- Header -->
                    <header class="px-5 pt-5 pb-4 flex items-center justify-between shrink-0">
                        <div class="flex items-center gap-3">
                            <div class="shrink-0 p-2 bg-tp-accent/10 rounded-[14px]">
                                <Cpu class="text-tp-accent w-5 h-5" />
                            </div>
                            <span class="text-base font-bold tracking-tight text-tp-text font-mono">{{ device.mac }}</span>
                        </div>
                        <Btn muted @click="emit('cancel')">
                            <X class="w-[15px] h-[15px] text-tp-muted" />
                        </Btn>
                    </header>

                    <!-- Blueprint -->
                    <div class="flex items-center justify-center px-5 pb-4 md:px-8 md:pb-6">
                        <svg
                            :viewBox="map.storage.viewBox ?? '0 0 0 0'"
                            class="w-full h-auto"
                            xmlns="http://www.w3.org/2000/svg"
                            :class="pickedId ? '' : 'cursor-crosshair'"
                        >
                            <HouseLayer />
                            <LightsLayer mode="config" @pick="onPick" />
                            <BlindsLayer mode="config" @pick="onPick" />
                        </svg>
                    </div>

                    <!-- Confirm (appears when a device is picked) -->
                    <Transition name="btn-fade">
                        <div v-if="pickedId" class="px-5 pb-5 md:px-8 md:pb-6 flex justify-end">
                            <button @click="confirm" :disabled="picking" class="action-primary">
                                <Check class="w-4 h-4 shrink-0" />
                                <span>{{ picking ? 'Asignando…' : 'Asignar' }}</span>
                            </button>
                        </div>
                    </Transition>

                </div>
            </div>
        </Transition>
    </Teleport>

</template>

<style scoped>
.map-popup-overlay {
    position: fixed;
    inset: 0;
    z-index: 60;
    display: flex;
    align-items: flex-end;
    justify-content: center;
    padding-bottom: 2rem;
    background: rgba(0, 0, 0, 0.32);
    backdrop-filter: blur(7px);
    -webkit-backdrop-filter: blur(7px);
}

@media (min-width: 768px) {
    .map-popup-overlay {
        align-items: center;
        padding-bottom: 0;
    }
}

.map-popup {
    width: 92vw;
    max-width: 48rem;
    max-height: 90vh;
    overflow-y: auto;
    border-radius: 32px;
    background: rgba(26, 26, 28, 0.88);
    backdrop-filter: blur(40px) saturate(180%);
    -webkit-backdrop-filter: blur(40px) saturate(180%);
    border: 0.5px solid rgba(255, 255, 255, 0.14);
    box-shadow:
        0 24px 80px rgba(0, 0, 0, 0.65),
        inset 0 1px 0 rgba(255, 255, 255, 0.12),
        inset 0 -1px 0 rgba(0, 0, 0, 0.2);
}

.popup-enter-active { transition: opacity 0.40s ease; }
.popup-leave-active { transition: opacity 0.42s ease; }
.popup-enter-from,
.popup-leave-to     { opacity: 0; }

.popup-enter-active .map-popup,
.popup-leave-active .map-popup { transform-origin: 50% 100%; }
@media (min-width: 768px) {
    .popup-enter-active .map-popup,
    .popup-leave-active .map-popup { transform-origin: 50% 50%; }
}
.popup-enter-active .map-popup {
    transition: transform 0.50s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.28s ease;
}
.popup-leave-active .map-popup {
    transition: transform 0.42s cubic-bezier(0.4, 0, 0.6, 1), opacity 0.38s ease;
}
.popup-enter-from .map-popup,
.popup-leave-to   .map-popup { transform: scale(0.08); opacity: 0; }

.btn-fade-enter-active,
.btn-fade-leave-active { transition: opacity 0.2s ease, transform 0.2s ease; }
.btn-fade-enter-from,
.btn-fade-leave-to     { opacity: 0; transform: translateY(4px); }
</style>
