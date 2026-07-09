<script setup>

    import { ref, onMounted } from 'vue'
    import { Cpu, Settings } from 'lucide-vue-next'

    import { useDevices } from '@/config/devices'
    import { api } from '@/config/api'
    import ConfigWizard from './ConfigWizard.vue'

    const store = useDevices()

    const pendingDevices = ref([])
    const loading = ref(false)
    const selectedPending = ref(null)

    async function fetchPending() {
        try {
            loading.value = true
            pendingDevices.value = (await api.getPending()).map(m => ({ mac: m }))
        } catch (error) {
            console.error('TPHome - Error fetching pending devices:', error)
        } finally {
            loading.value = false
        }
    }

    function startConfig(device) {
        selectedPending.value = device
    }

    function onConfigDone() {
        selectedPending.value = null
        fetchPending()
        store.setup()
    }

    function onConfigCancel() {
        selectedPending.value = null
    }

    onMounted(fetchPending)

</script>

<template>

    <div class="h-full flex flex-col p-8 gap-8 overflow-y-auto">

        <section>
            <div class="flex items-center gap-3 mb-5">
                <div class="w-2 h-2 rounded-full bg-tp-accent shadow-[0_0_6px_var(--color-tp-accent)] animate-pulse"></div>
                <h2 class="text-sm font-bold uppercase tracking-widest text-tp-muted">
                    Pendientes
                    <span class="text-tp-accent font-mono ml-1.5">{{ pendingDevices.length }}</span>
                </h2>
            </div>

            <div v-if="loading" class="text-sm text-tp-muted/50 italic px-1">Cargando...</div>

            <div v-else-if="pendingDevices.length === 0" class="text-sm text-tp-muted/50 italic px-1">
                No hay dispositivos pendientes de configurar.
            </div>

            <div v-else class="space-y-2">
                <div
                    v-for="device in pendingDevices"
                    :key="device.mac"
                    class="flex items-center gap-4 px-4 py-3 rounded-xl bg-tp-surface border border-tp-border hover:border-tp-accent/30 transition-colors"
                >
                    <Cpu class="w-4 h-4 shrink-0 text-tp-accent" />
                    <span class="font-mono text-xs text-tp-muted flex-1">{{ device.mac }}</span>
                    <span class="text-2xs font-mono uppercase tracking-wider text-tp-muted/50 w-20 shrink-0 truncate">{{ device.chip ?? 'desconocido' }}</span>
                    <button
                        @click="startConfig(device)"
                        class="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-tp-accent/10 border border-tp-accent/20 text-tp-accent hover:bg-tp-accent/20 transition-all text-xs font-bold uppercase tracking-wider cursor-pointer"
                    >
                        <Settings class="w-3.5 h-3.5" />
                        Configurar
                    </button>
                </div>
            </div>
        </section>

        <ConfigWizard
            v-if="selectedPending"
            :device="selectedPending"
            @done="onConfigDone"
            @cancel="onConfigCancel"
        />

    </div>

</template>
