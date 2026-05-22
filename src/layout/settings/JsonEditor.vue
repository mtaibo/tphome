<script setup>

    import { ref, computed, onMounted } from 'vue'
    import { Lightbulb, Blinds, Save, ChevronDown, ChevronRight, Trash2, Plus } from 'lucide-vue-next'

    import { useDevices } from '@/config/devices'
    import { api } from '@/config/api'

    const store = useDevices()

    const config = ref(null)
    const loading = ref(false)
    const saving = ref(false)
    const expandedPrefs = ref({})

    const allDevices = computed(() => {
        if (!config.value) return []
        const devices = []
        for (const [category, categoryDevices] of Object.entries(config.value)) {
            for (const [id, device] of Object.entries(categoryDevices)) {
                devices.push({
                    id,
                    name: device.name ?? '',
                    category,
                    type: category === 'lights' ? 'Luz' : category === 'blinds' ? 'Persiana' : category,
                    mapX: device.map?.x ?? '',
                    mapY: device.map?.y ?? '',
                    prefs: { ...device.prefs },
                    originalPrefs: JSON.stringify(device.prefs)
                })
            }
        }
        return devices
    })

    async function fetchConfig() {
        try {
            loading.value = true
            config.value = await api.getConfig('devices')
        } catch (error) {
            console.error('TPHome - Error fetching config:', error)
        } finally {
            loading.value = false
        }
    }

    function togglePrefs(id) {
        expandedPrefs.value[id] = !expandedPrefs.value[id]
    }

    function updatePref(device, key, value) {
        device.prefs[key] = value
    }

    function addPref(device) {
        const key = prompt('Nombre de la preferencia:')
        if (!key || key in device.prefs) return
        const value = prompt('Valor:')
        if (value === null) return
        device.prefs[key] = value
    }

    function removePref(device, key) {
        delete device.prefs[key]
    }

    async function saveDevice(device) {
        if (!config.value) return
        const cat = device.category
        if (!config.value[cat]?.[device.id]) return

        config.value[cat][device.id].name = device.name
        config.value[cat][device.id].prefs = { ...device.prefs }
        config.value[cat][device.id].map = {
            ...config.value[cat][device.id].map,
            x: device.mapX,
            y: device.mapY
        }

        try {
            saving.value = true
            await api.postConfig('devices', config.value)
            await store.setup()
            device.originalPrefs = JSON.stringify(device.prefs)
        } catch (error) {
            console.error('TPHome - Error saving config:', error)
        } finally {
            saving.value = false
        }
    }

    async function deleteDevice(device) {
        if (!confirm(`¿Borrar ${device.id} del JSON de configuracion?`)) return
        if (!config.value) return

        delete config.value[device.category][device.id]

        try {
            await api.postConfig('devices', config.value)
            await store.setup()
            await fetchConfig()
        } catch (error) {
            console.error('TPHome - Error deleting device:', error)
        }
    }

    function hasChanges(device) {
        return JSON.stringify(device.prefs) !== device.originalPrefs
    }

    onMounted(fetchConfig)

</script>

<template>

    <div class="h-full flex flex-col p-8 gap-8 overflow-y-auto">

        <section>
            <div class="flex items-center gap-3 mb-5">
                <div class="w-2 h-2 rounded-full bg-blue-400 shadow-[0_0_6px_var(--color-blue-400)]"></div>
                <h2 class="text-sm font-bold uppercase tracking-widest text-muted">
                    JSON de Configuracion
                    <span class="text-tp-accent font-mono ml-1.5">{{ allDevices.length }}</span>
                </h2>
            </div>

            <div v-if="loading" class="text-sm text-muted/50 italic px-1">Cargando...</div>

            <div v-else-if="allDevices.length === 0" class="text-sm text-muted/50 italic px-1">
                No hay dispositivos en el JSON de configuracion.
            </div>

            <div v-else class="space-y-3">
                <div
                    v-for="device in allDevices"
                    :key="device.id"
                    class="rounded-xl bg-tp-surface border border-tp-border overflow-hidden"
                >
                    <div class="flex items-center gap-4 px-4 py-3">
                        <button
                            @click="togglePrefs(device.id)"
                            class="p-1 rounded hover:bg-tp-border/20 transition-colors cursor-pointer"
                        >
                            <ChevronRight v-if="!expandedPrefs[device.id]" class="w-4 h-4 text-muted" />
                            <ChevronDown v-else class="w-4 h-4 text-muted" />
                        </button>

                        <component
                            :is="device.type === 'Luz' ? Lightbulb : Blinds"
                            class="w-4 h-4 shrink-0"
                            :class="device.type === 'Luz' ? 'text-yellow-400/70' : 'text-tp-accent/70'"
                        />

                        <span class="font-mono text-xs text-muted w-16 shrink-0">{{ device.id }}</span>

                        <input
                            v-model="device.name"
                            class="flex-1 bg-transparent text-sm text-white border-none outline-none focus:ring-1 focus:ring-tp-accent/30 rounded px-1"
                            placeholder="Nombre"
                        />

                        <span class="text-[10px] font-mono uppercase tracking-wider text-muted/50 w-20 shrink-0">{{ device.type }}</span>

                        <div class="flex items-center gap-1 w-24 shrink-0">
                            <span class="text-[10px] text-muted/40 mr-1">X:</span>
                            <input
                                v-model.number="device.mapX"
                                type="number"
                                class="w-12 bg-transparent text-xs font-mono text-muted border border-tp-border/30 rounded px-1 py-0.5 outline-none focus:border-tp-accent/50"
                            />
                            <span class="text-[10px] text-muted/40 ml-1 mr-1">Y:</span>
                            <input
                                v-model.number="device.mapY"
                                type="number"
                                class="w-12 bg-transparent text-xs font-mono text-muted border border-tp-border/30 rounded px-1 py-0.5 outline-none focus:border-tp-accent/50"
                            />
                        </div>

                        <button
                            @click="saveDevice(device)"
                            :disabled="!hasChanges(device) || saving"
                            class="flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg text-xs font-bold uppercase tracking-wider transition-all cursor-pointer"
                            :class="hasChanges(device) && !saving
                                ? 'bg-tp-ok/20 text-tp-ok border border-tp-ok/30 hover:bg-tp-ok/30'
                                : 'bg-tp-border/10 text-muted/30 border border-tp-border/20 cursor-not-allowed'"
                        >
                            <Save class="w-3 h-3" />
                            {{ saving ? '...' : '' }}
                        </button>

                        <button
                            @click="deleteDevice(device)"
                            class="flex items-center justify-center w-8 h-8 rounded-lg text-muted hover:text-tp-danger hover:bg-tp-danger/10 transition-all shrink-0 cursor-pointer"
                        >
                            <Trash2 class="w-4 h-4" />
                        </button>
                    </div>

                    <div v-if="expandedPrefs[device.id]" class="px-4 pb-3 pt-0 border-t border-tp-border/30">
                        <div class="flex items-center gap-2 mt-3 mb-2">
                            <span class="text-[10px] font-mono uppercase tracking-widest text-muted/50">Preferencias</span>
                            <button
                                @click="addPref(device)"
                                class="flex items-center gap-1 px-2 py-0.5 rounded text-[10px] font-mono uppercase text-tp-accent/70 hover:text-tp-accent hover:bg-tp-accent/10 transition-colors cursor-pointer"
                            >
                                <Plus class="w-3 h-3" />
                                Anadir
                            </button>
                        </div>

                        <div class="space-y-1.5">
                            <div
                                v-for="(value, key) in device.prefs"
                                :key="key"
                                class="flex items-center gap-2"
                            >
                                <span class="text-xs font-mono text-muted/60 w-28 shrink-0 truncate" :title="key">{{ key }}</span>
                                <input
                                    :value="value"
                                    @input="updatePref(device, key, $event.target.value)"
                                    class="flex-1 bg-tp-bg text-xs font-mono text-white border border-tp-border/30 rounded px-2 py-1 outline-none focus:border-tp-accent/50"
                                />
                                <button
                                    @click="removePref(device, key)"
                                    class="p-1 rounded text-muted/40 hover:text-tp-danger hover:bg-tp-danger/10 transition-colors cursor-pointer"
                                >
                                    <Trash2 class="w-3 h-3" />
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>

    </div>

</template>
