<script setup>

    import { ref, watch } from 'vue'
    import { X, Check, ArrowLeft } from 'lucide-vue-next'
    import { useMap } from '@/config/map'
    import { useDevices } from '@/config/devices'
    import { api } from '@/config/api'
    import HouseLayer  from '@/components/blueprint/Map.vue'
    import LightsLayer from '@/components/blueprint/Lights.vue'
    import BlindsLayer from '@/components/blueprint/Blinds.vue'

    const props = defineProps({
        device: { type: Object, default: null }
    })
    const emit = defineEmits(['done', 'cancel'])

    const map   = useMap()
    const store = useDevices()

    const pickedId = ref(null)
    const picking  = ref(false)
    const error    = ref(null)

    function onPick(id) { pickedId.value = id; error.value = null }

    async function confirm() {
        if (!pickedId.value) return
        error.value = null
        picking.value = true
        try {
            const category = Object.keys(store.storage).find(cat => pickedId.value in store.storage[cat])
            if (!category) { error.value = `No se encontró ${pickedId.value} en la configuración`; return }
            await api.configurePending(props.device.mac, pickedId.value, store.storage[category][pickedId.value].prefs)
            emit('done')
        } catch (err) {
            error.value = `Error al configurar: ${err.message}`
            console.error('TPHome - Config error:', err)
        } finally {
            picking.value = false
        }
    }

    watch(() => props.device, async (d) => {
        if (!d) { pickedId.value = null; error.value = null; return }
        if (Object.keys(store.storage).length === 0) await store.setup()
    }, { immediate: true })

</script>

<template>

    <Teleport to="body">
        <Transition name="popup">
            <div v-if="device" class="map-popup-overlay" @click.self="emit('cancel')">
                <div class="map-popup">

                    <!-- Header -->
                    <header class="h-16 px-6 flex items-center justify-between shrink-0 border-b border-white/10">
                        <div class="flex items-center gap-4">
                            <button @click="emit('cancel')" class="flex items-center gap-2 text-tp-muted hover:text-tp-text transition-colors text-sm cursor-pointer">
                                <ArrowLeft class="w-4 h-4" />
                                Volver
                            </button>
                            <div class="h-5 w-px bg-white/10"></div>
                            <span class="text-sm text-tp-text font-medium">Asignar dispositivo</span>
                        </div>
                        <div class="flex items-center gap-3">
                            <span class="font-mono text-2xs text-tp-muted/60 truncate max-w-40">{{ device.mac }}</span>
                            <button @click="emit('cancel')" class="p-1.5 rounded-lg text-tp-muted hover:text-tp-text hover:bg-white/10 transition-colors cursor-pointer">
                                <X class="w-4 h-4" />
                            </button>
                        </div>
                    </header>

                    <!-- Instruction / error bar -->
                    <div class="px-6 py-3 text-[11px] font-mono uppercase tracking-widest border-b shrink-0 transition-colors"
                         :class="error ? 'text-tp-off bg-tp-off/10 border-tp-off/20' : 'text-tp-muted/50 border-white/5'">
                        {{ error ?? (pickedId ? 'Dispositivo seleccionado: ' + pickedId : 'Haz clic en un dispositivo del plano para asignarlo') }}
                    </div>

                    <!-- Blueprint -->
                    <div class="flex-1 flex items-center justify-center p-5 md:p-10 min-h-0">
                        <svg
                            :viewBox="map.storage.viewBox ?? '0 0 0 0'"
                            class="w-full h-auto max-w-3xl"
                            xmlns="http://www.w3.org/2000/svg"
                            :class="pickedId ? '' : 'cursor-crosshair'"
                        >
                            <HouseLayer />
                            <LightsLayer mode="config" @pick="onPick" />
                            <BlindsLayer mode="config" @pick="onPick" />
                        </svg>
                    </div>

                    <!-- Footer -->
                    <footer class="h-16 px-6 flex items-center justify-end gap-3 shrink-0 border-t border-white/10">
                        <button @click="emit('cancel')" class="px-4 py-2 rounded-lg text-sm text-tp-muted hover:text-tp-text hover:bg-white/10 transition-colors cursor-pointer">
                            Cancelar
                        </button>
                        <button
                            @click="confirm"
                            :disabled="!pickedId || picking"
                            class="flex items-center gap-2 px-5 py-2 rounded-lg text-sm font-bold uppercase tracking-wider transition-all"
                            :class="pickedId && !picking
                                ? 'bg-tp-on/20 text-tp-on border border-tp-on/30 hover:bg-tp-on/30 cursor-pointer'
                                : 'bg-white/5 text-tp-muted/30 border border-white/10 cursor-not-allowed'"
                        >
                            <Check class="w-4 h-4" />
                            {{ picking ? 'Asignando...' : 'Asignar' }}
                        </button>
                    </footer>

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
    align-items: center;
    justify-content: center;
    padding: 1.5rem;
    background: rgba(0, 0, 0, 0.50);
    backdrop-filter: blur(7px);
    -webkit-backdrop-filter: blur(7px);
}

.map-popup {
    width: 100%;
    max-width: 56rem;
    max-height: 90vh;
    display: flex;
    flex-direction: column;
    border-radius: 32px;
    overflow: hidden;
    background: rgba(26, 26, 28, 0.92);
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
.popup-leave-active .map-popup { transform-origin: 50% 50%; }
.popup-enter-active .map-popup {
    transition: transform 0.50s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.28s ease;
}
.popup-leave-active .map-popup {
    transition: transform 0.42s cubic-bezier(0.4, 0, 0.6, 1), opacity 0.38s ease;
}
.popup-enter-from .map-popup,
.popup-leave-to   .map-popup { transform: scale(0.94); opacity: 0; }
</style>
