<script setup>

    import { ref, computed, onMounted } from 'vue'
    import { Lightbulb, Blinds, Save, ChevronDown, Trash2 } from 'lucide-vue-next'

    import { useDevices } from '@/config/devices'
    import { api } from '@/config/api'

    const store = useDevices()

    const config = ref(null)
    const loading = ref(false)
    const saving = ref(false)
    const expandedId = ref(null)

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

    function toggleExpanded(id) {
        expandedId.value = expandedId.value === id ? null : id
    }

    function updatePref(device, key, value) {
        device.prefs[key] = value
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
                <div class="w-2 h-2 rounded-full bg-tp-accent shadow-[0_0_6px_var(--color-tp-accent)]"></div>
                <h2 class="text-sm font-bold uppercase tracking-widest text-muted">
                    JSON de Configuracion
                    <span class="text-tp-accent font-mono ml-1.5">{{ allDevices.length }}</span>
                </h2>
            </div>

            <div v-if="loading" class="text-sm text-muted/50 italic px-1">Cargando...</div>

            <div v-else-if="allDevices.length === 0" class="text-sm text-muted/50 italic px-1">
                No hay dispositivos en el JSON de configuracion.
            </div>

            <div v-else class="space-y-2">
                <div
                    v-for="device in allDevices"
                    :key="device.id"
                    class="rounded-xl bg-tp-surface border border-tp-border hover:border-tp-border/60 transition-colors overflow-hidden"
                >
                    <!-- Main row (clickable) -->
                    <div
                        class="flex items-center gap-4 px-4 py-3 cursor-pointer select-none"
                        @click="toggleExpanded(device.id)"
                    >
                        <component
                            :is="device.type === 'Luz' ? Lightbulb : Blinds"
                            class="w-4 h-4 shrink-0"
                            :class="device.type === 'Luz' ? 'text-yellow-400/70' : 'text-tp-accent/70'"
                        />
                        <span class="font-mono text-xs text-muted w-16 shrink-0">{{ device.id }}</span>
                        <span class="text-sm text-white flex-1 truncate">{{ device.name }}</span>
                        <ChevronDown
                            class="w-4 h-4 shrink-0 text-muted transition-transform duration-200"
                            :class="{ 'rotate-180': expandedId === device.id }"
                        />
                    </div>

                    <!-- Expanded content -->
                    <div
                        class="expand-content"
                        :class="{ 'expand-open': expandedId === device.id }"
                    >
                        <div class="border-t border-tp-border/50 px-4 py-4 bg-black/10 space-y-4">
                            <!-- Name -->
                            <div class="flex items-center gap-3">
                                <label class="text-xs font-mono text-muted/60 w-24 shrink-0">Nombre</label>
                                <input
                                    v-model="device.name"
                                    class="flex-1 bg-tp-bg text-sm text-white border border-tp-border/30 rounded-lg px-3 py-2 outline-none focus:border-tp-accent/50"
                                    placeholder="Nombre del dispositivo"
                                />
                            </div>

                            <!-- Position -->
                            <div class="flex items-center gap-3">
                                <label class="text-xs font-mono text-muted/60 w-24 shrink-0">Posicion</label>
                                <div class="flex items-center gap-2">
                                    <div class="flex items-center gap-1.5">
                                        <span class="text-xs font-mono text-muted/40 font-bold">X</span>
                                        <input
                                            v-model.number="device.mapX"
                                            type="number"
                                            class="w-20 bg-tp-bg text-sm font-mono text-muted border border-tp-border/30 rounded-lg px-3 py-2 outline-none focus:border-tp-accent/50 [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
                                        />
                                    </div>
                                    <div class="flex items-center gap-1.5">
                                        <span class="text-xs font-mono text-muted/40 font-bold">Y</span>
                                        <input
                                            v-model.number="device.mapY"
                                            type="number"
                                            class="w-20 bg-tp-bg text-sm font-mono text-muted border border-tp-border/30 rounded-lg px-3 py-2 outline-none focus:border-tp-accent/50 [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
                                        />
                                    </div>
                                </div>
                            </div>

                            <!-- Preferences -->
                            <div>
                                <label class="text-xs font-mono text-muted/60 w-24 shrink-0 block mb-2">Preferencias</label>

                                <div class="space-y-1.5 ml-24">
                                    <div class="flex items-center gap-2">
                                        <span class="text-xs font-mono text-muted/60 w-36 shrink-0">Tiempo de Subida</span>
                                        <input
                                            :value="device.prefs.up_time"
                                            @input="updatePref(device, 'up_time', Number($event.target.value))"
                                            type="number"
                                            min="0"
                                            step="0.1"
                                            placeholder="Segundos"
                                            class="flex-1 bg-tp-bg text-sm font-mono text-white border border-tp-border/30 rounded-lg px-3 py-2 outline-none focus:border-tp-accent/50 [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
                                        />
                                        <span class="text-xs text-muted/40 shrink-0">seg</span>
                                    </div>
                                    <div class="flex items-center gap-2">
                                        <span class="text-xs font-mono text-muted/60 w-36 shrink-0">Tiempo de Bajada</span>
                                        <input
                                            :value="device.prefs.down_time"
                                            @input="updatePref(device, 'down_time', Number($event.target.value))"
                                            type="number"
                                            min="0"
                                            step="0.1"
                                            placeholder="Segundos"
                                            class="flex-1 bg-tp-bg text-sm font-mono text-white border border-tp-border/30 rounded-lg px-3 py-2 outline-none focus:border-tp-accent/50 [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
                                        />
                                        <span class="text-xs text-muted/40 shrink-0">seg</span>
                                    </div>
                                    <div class="flex items-center gap-2">
                                        <span class="text-xs font-mono text-muted/60 w-36 shrink-0">Posicion de Bajada</span>
                                        <input
                                            :value="device.prefs.down_pos"
                                            @input="updatePref(device, 'down_pos', Math.min(100, Math.max(0, Number($event.target.value))))"
                                            type="number"
                                            min="0"
                                            max="100"
                                            placeholder="0-100"
                                            class="flex-1 bg-tp-bg text-sm font-mono text-white border border-tp-border/30 rounded-lg px-3 py-2 outline-none focus:border-tp-accent/50 [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
                                        />
                                        <span class="text-xs text-muted/40 shrink-0">%</span>
                                    </div>
                                    <div class="flex items-center gap-2">
                                        <span class="text-xs font-mono text-muted/60 w-36 shrink-0">Reles Invertidos</span>
                                        <select
                                            :value="device.prefs.inverted_relays"
                                            @change="updatePref(device, 'inverted_relays', $event.target.value === 'true')"
                                            class="flex-1 bg-tp-bg text-sm font-mono text-white border border-tp-border/30 rounded-lg px-3 py-2 outline-none focus:border-tp-accent/50"
                                        >
                                            <option :value="true">true</option>
                                            <option :value="false">false</option>
                                        </select>
                                    </div>
                                </div>
                            </div>

                            <!-- Actions -->
                            <div class="flex items-center gap-2 pt-2">
                                <button
                                    @click.stop="saveDevice(device)"
                                    :disabled="!hasChanges(device) || saving"
                                    class="flex items-center gap-1.5 px-4 py-2 rounded-lg text-xs font-bold uppercase tracking-wider transition-all cursor-pointer"
                                    :class="hasChanges(device) && !saving
                                        ? 'bg-tp-ok/20 text-tp-ok border border-tp-ok/30 hover:bg-tp-ok/30'
                                        : 'bg-tp-border/10 text-muted/30 border border-tp-border/20 cursor-not-allowed'"
                                >
                                    <Save class="w-3.5 h-3.5" />
                                    {{ saving ? 'Guardando...' : 'Guardar' }}
                                </button>
                                <button
                                    @click.stop="deleteDevice(device)"
                                    class="flex items-center gap-1.5 px-4 py-2 rounded-lg text-xs font-bold uppercase tracking-wider text-muted/50 hover:text-tp-danger hover:bg-tp-danger/10 border border-tp-border/20 transition-all cursor-pointer"
                                >
                                    <Trash2 class="w-3.5 h-3.5" />
                                    Eliminar
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>

    </div>

</template>

<style scoped>
    .expand-content {
        max-height: 0;
        overflow: hidden;
        transition: max-height 0.4s ease-out;
    }

    .expand-open {
        max-height: 800px;
    }
</style>
