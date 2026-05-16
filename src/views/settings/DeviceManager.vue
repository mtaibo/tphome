<script setup>

    import { ref, onMounted, computed } from 'vue'
    import { Lightbulb, Blinds, Trash2, Settings, Cpu } from 'lucide-vue-next'

    import { useDevices } from '../../config/devices'
    import { api } from '../../config/api'
    import ConfigWizard from './ConfigWizard.vue'

    const store = useDevices()

    const pendingDevices = ref([])
    const loading = ref(false)
    const selectedPending = ref(null)

    const configuredLights = computed(() =>
        Object.entries(store.storage.lights ?? {}).map(([id, d]) => ({ id, ...d, type: 'Luz' }))
    )
    const configuredBlinds = computed(() =>
        Object.entries(store.storage.blinds ?? {}).map(([id, d]) => ({ id, ...d, type: 'Persiana' }))
    )
    const allConfigured = computed(() =>
        [...configuredBinds.value, ...configuredLights.value]
    )

    async function fetchPending() {
        try {
            loading.value = true
            pendingDevices.value = await api.getPendingDevices()
        } catch (error) {
            console.error('TPHome - Error fetching pending devices:', error)
        } finally {
            loading.value = false
        }
    }

    async function deleteDevice(category, id) {
        if (!confirm(`¿Borrar ${id}?`)) return
        try {
            const config = await api.getConfig('devices')
            delete config[category][id]
            await api.postConfig('devices', config)
            await store.setup()
        } catch (error) {
            console.error('TPHome - Error deleting device:', error)
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

        <!-- Configured devices -->
        <section>
            <div class="flex items-center gap-3 mb-5">
                <div class="w-2 h-2 rounded-full bg-tp-ok shadow-[0_0_6px_var(--color-tp-ok)]"></div>
                <h2 class="text-sm font-bold uppercase tracking-widest text-muted">
                    Configurados
                    <span class="text-tp-accent font-mono ml-1.5">{{ allConfigured.length }}</span>
                </h2>
            </div>

            <div v-if="allConfigured.length === 0" class="text-sm text-muted/50 italic px-1">
                No hay dispositivos configurados.
            </div>

            <div v-else class="space-y-2">
                <div
                    v-for="device in allConfigured"
                    :key="device.id"
                    class="flex items-center gap-4 px-4 py-3 rounded-xl bg-tp-surface border border-tp-border hover:border-tp-border/60 transition-colors"
                >
                    <component
                        :is="device.type === 'Luz' ? Lightbulb : Blinds"
                        class="w-4 h-4 shrink-0"
                        :class="device.type === 'Luz' ? 'text-yellow-400/70' : 'text-tp-accent/70'"
                    />
                    <span class="font-mono text-xs text-muted w-16 shrink-0">{{ device.id }}</span>
                    <span class="text-sm text-white flex-1 truncate">{{ device.name }}</span>
                    <span class="text-[10px] font-mono uppercase tracking-wider text-muted/50 w-16 shrink-0">{{ device.type }}</span>
                    <button
                        @click="deleteDevice(device.type === 'Persiana' ? 'blinds' : 'lights', device.id)"
                        class="flex items-center justify-center w-8 h-8 rounded-lg text-muted hover:text-tp-danger hover:bg-tp-danger/10 transition-all shrink-0 cursor-pointer"
                    >
                        <Trash2 class="w-4 h-4" />
                    </button>
                </div>
            </div>
        </section>

        <!-- Pending devices -->
        <section>
            <div class="flex items-center gap-3 mb-5">
                <div class="w-2 h-2 rounded-full bg-tp-accent shadow-[0_0_6px_var(--color-tp-accent)] animate-pulse"></div>
                <h2 class="text-sm font-bold uppercase tracking-widest text-muted">
                    Pendientes
                    <span class="text-tp-accent font-mono ml-1.5">{{ pendingDevices.length }}</span>
                </h2>
            </div>

            <div v-if="loading" class="text-sm text-muted/50 italic px-1">Cargando...</div>

            <div v-else-if="pendingDevices.length === 0" class="text-sm text-muted/50 italic px-1">
                No hay dispositivos pendientes de configurar.
            </div>

            <div v-else class="space-y-2">
                <div
                    v-for="device in pendingDevices"
                    :key="device.mac"
                    class="flex items-center gap-4 px-4 py-3 rounded-xl bg-tp-surface border border-tp-border hover:border-tp-accent/30 transition-colors"
                >
                    <Cpu class="w-4 h-4 shrink-0 text-tp-accent" />
                    <span class="font-mono text-xs text-muted flex-1">{{ device.mac }}</span>
                    <span class="text-[10px] font-mono uppercase tracking-wider text-muted/50 w-20 shrink-0 truncate">{{ device.chip ?? 'desconocido' }}</span>
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

        <!-- Config Wizard Modal -->
        <ConfigWizard
            v-if="selectedPending"
            :device="selectedPending"
            @done="onConfigDone"
            @cancel="onConfigCancel"
        />

    </div>

</template>
