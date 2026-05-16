<script setup>

    import { ref } from 'vue'
    import { X, Check, ArrowLeft } from 'lucide-vue-next'

    import { useMap } from '../../config/map'
    import { useDevices } from '../../config/devices'
    import { api } from '../../config/api'

    import HouseLayer  from '../../components/blueprint-layers/HouseLayer.vue'
    import LightsLayer from '../../components/blueprint-layers/LightsLayer.vue'
    import BlindsLayer from '../../components/blueprint-layers/BlindsLayer.vue'

    const props = defineProps({
        device: { type: Object, required: true }
    })
    const emit = defineEmits(['done', 'cancel'])

    const map = useMap()
    const store = useDevices()

    const pickedId = ref(null)
    const picking = ref(false)

    function onPick(id) {
        pickedId.value = id
    }

    async function confirm() {
        if (!pickedId.value) return
        picking.value = true
        try {
            const category = Object.keys(store.storage).find(cat => pickedId.value in store.storage[cat])
            if (!category) return
            const prefs = store.storage[category][pickedId.value].prefs
            await api.configurePendingDevice(props.device.mac, pickedId.value, prefs)
            emit('done')
        } catch (error) {
            console.error('TPHome - Config error:', error)
        } finally {
            picking.value = false
        }
    }

</script>

<template>

    <div class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm">
        <div class="relative w-full max-w-3xl mx-4 bg-tp-surface border border-tp-border rounded-2xl shadow-2xl flex flex-col max-h-[90vh]">

            <!-- Header -->
            <header class="h-16 px-6 flex items-center justify-between shrink-0 border-b border-tp-border">
                <div class="flex items-center gap-4">
                    <button
                        @click="emit('cancel')"
                        class="flex items-center gap-2 text-muted hover:text-white transition-colors text-sm cursor-pointer"
                    >
                        <ArrowLeft class="w-4 h-4" />
                        Volver
                    </button>
                    <div class="h-5 w-px bg-tp-border"></div>
                    <span class="text-sm text-white font-medium">Asignar dispositivo</span>
                </div>

                <div class="flex items-center gap-3">
                    <span class="font-mono text-[10px] text-muted/60 truncate max-w-40">{{ device.mac }}</span>
                    <button
                        @click="emit('cancel')"
                        class="p-1.5 rounded-lg text-muted hover:text-white hover:bg-tp-border/20 transition-colors cursor-pointer"
                    >
                        <X class="w-4 h-4" />
                    </button>
                </div>
            </header>

            <!-- Instruction -->
            <div class="px-6 py-3 text-[11px] font-mono uppercase tracking-widest text-muted/50 border-b border-tp-border/50 shrink-0">
                {{ pickedId ? 'Dispositivo seleccionado: ' + pickedId : 'Haz clic en un dispositivo del plano para asignarlo' }}
            </div>

            <!-- SVG Blueprint -->
            <div class="flex-1 flex items-center justify-center p-6 min-h-0">
                <svg
                    :viewBox="map.storage.viewBox ?? '0 0 0 0'"
                    class="w-full h-auto max-w-xl drop-shadow-2xl"
                    xmlns="http://www.w3.org/2000/svg"
                    :class="pickedId ? '' : 'cursor-crosshair'"
                >
                    <HouseLayer />
                    <LightsLayer mode="config" @pick="onPick" />
                    <BlindsLayer mode="config" @pick="onPick" />
                </svg>
            </div>

            <!-- Footer -->
            <footer class="h-16 px-6 flex items-center justify-end gap-3 shrink-0 border-t border-tp-border">
                <button
                    @click="emit('cancel')"
                    class="px-4 py-2 rounded-lg text-sm text-muted hover:text-white hover:bg-tp-border/20 transition-colors cursor-pointer"
                >
                    Cancelar
                </button>
                <button
                    @click="confirm"
                    :disabled="!pickedId || picking"
                    class="flex items-center gap-2 px-5 py-2 rounded-lg text-sm font-bold uppercase tracking-wider transition-all cursor-pointer"
                    :class="pickedId && !picking
                        ? 'bg-tp-ok/20 text-tp-ok border border-tp-ok/30 hover:bg-tp-ok/30'
                        : 'bg-tp-border/10 text-muted/30 border border-tp-border/20 cursor-not-allowed'"
                >
                    <Check class="w-4 h-4" />
                    {{ picking ? 'Asignando...' : 'Asignar' }}
                </button>
            </footer>

        </div>
    </div>

</template>
