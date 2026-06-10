<script setup>

    import { ref, computed, onMounted, reactive } from 'vue'
    import { Lightbulb, Blinds, Save, ChevronDown, Trash2, RotateCcw } from 'lucide-vue-next'

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
                const rawPrefs = device.prefs ?? {}
                const prefs = {
                    inverted_relays: !!rawPrefs.inverted_relays,
                    up_time: rawPrefs.up_time != null ? formatTime(rawPrefs.up_time) : '',
                    down_time: rawPrefs.down_time != null ? formatTime(rawPrefs.down_time) : '',
                    down_pos: rawPrefs.down_pos != null ? formatPosition(rawPrefs.down_pos) : ''
                }
                devices.push(reactive({
                    id,
                    name: device.name ?? '',
                    category,
                    type: category === 'lights' ? 'Luz' : category === 'blinds' ? 'Persiana' : category,
                    mapX: device.map?.x ?? '',
                    mapY: device.map?.y ?? '',
                    prefs,
                    originalName: device.name ?? '',
                    originalMapX: device.map?.x ?? '',
                    originalMapY: device.map?.y ?? '',
                    originalPrefs: JSON.stringify(prefs),
                    dirty: false
                }))
            }
        }
        return devices
    })

    function formatTime(raw) {
        return (raw / 100).toFixed(1)
    }

    function formatPosition(raw) {
        return Math.round(raw / 100)
    }

    function parseTime(value) {
        if (value === '' || isNaN(value)) return 0
        return Math.round(Number(String(value).replace(',', '.')) * 100)
    }

    function parsePosition(value) {
        if (value === '' || isNaN(value)) return 0
        return Math.round(Number(String(value).replace(',', '.')) * 100)
    }

    function normalizeInput(value) {
        return String(value).replace(',', '.')
    }

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
        checkDirty(device)
    }

    function markDirty(device) {
        checkDirty(device)
    }

    function checkDirty(device) {
        const originalPrefs = JSON.parse(device.originalPrefs)
        const prefsChanged = JSON.stringify(device.prefs) !== JSON.stringify(originalPrefs)
        const nameChanged = device.name !== device.originalName
        const mapXChanged = device.mapX !== device.originalMapX
        const mapYChanged = device.mapY !== device.originalMapY
        device.dirty = prefsChanged || nameChanged || mapXChanged || mapYChanged
    }

    function hasChanges(device) {
        return device.dirty
    }

    function resetDevice(device) {
        device.name = device.originalName
        device.mapX = device.originalMapX
        device.mapY = device.originalMapY
        device.prefs = JSON.parse(device.originalPrefs)
        device.dirty = false
    }

    async function saveDevice(device) {
        if (!config.value) return
        const cat = device.category
        if (!config.value[cat]?.[device.id]) return

        config.value[cat][device.id].name = device.name
        config.value[cat][device.id].prefs = {
            ...device.prefs,
            up_time: parseTime(device.prefs.up_time),
            down_time: parseTime(device.prefs.down_time),
            down_pos: parsePosition(device.prefs.down_pos)
        }
        config.value[cat][device.id].map = {
            ...config.value[cat][device.id].map,
            x: device.mapX,
            y: device.mapY
        }

        try {
            saving.value = true
            await api.postConfig('devices', config.value)
            await store.setup()
            device.originalName = device.name
            device.originalMapX = device.mapX
            device.originalMapY = device.mapY
            device.originalPrefs = JSON.stringify({ ...device.prefs })
            device.dirty = false
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

    onMounted(fetchConfig)

</script>

<template>

    <div class="h-full flex flex-col p-4 md:p-8 gap-4 md:gap-8 overflow-y-auto">

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
                        class="flex items-center gap-2 md:gap-4 px-3 md:px-4 py-3 cursor-pointer select-none"
                        @click="toggleExpanded(device.id)"
                    >
                        <component
                            :is="device.type === 'Luz' ? Lightbulb : Blinds"
                            class="w-4 h-4 shrink-0"
                            :class="device.type === 'Luz' ? 'text-tp-light-on/70' : 'text-tp-accent/70'"
                        />
                        <span class="font-mono text-xs text-muted w-16 shrink-0">{{ device.id }}</span>
                        <span class="text-sm text-tp-text-primary flex-1 truncate">{{ device.name }}</span>
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
                        <div class="border-t border-tp-border/50 px-3 md:px-4 py-4 bg-black/10 space-y-4">
                            <!-- Name -->
                            <div class="flex flex-col md:flex-row md:items-center gap-1.5 md:gap-3">
                                <label class="text-xs font-mono text-muted/60 w-full md:w-24 shrink-0">Nombre</label>
                                <input
                                    v-model="device.name"
                                    @input="markDirty(device)"
                                    class="w-full bg-tp-bg text-sm text-muted border border-tp-border/30 rounded-lg px-3 py-2 outline-none focus:border-tp-accent/50"
                                    placeholder="Nombre del dispositivo"
                                />
                            </div>

                            <!-- Position -->
                            <div class="flex flex-col md:flex-row md:items-center gap-1.5 md:gap-3">
                                <label class="text-xs font-mono text-muted/60 w-full md:w-24 shrink-0">Posicion</label>
                                <div class="flex items-center gap-2">
                                     <div class="flex items-center gap-1.5">
                                         <span class="text-xs font-mono text-muted/40 font-bold">X</span>
                                           <input
                                               v-model.number="device.mapX"
                                               @input="markDirty(device)"
                                               type="number"
                                             class="w-20 bg-tp-bg text-sm font-mono text-muted border border-tp-border/30 rounded-lg px-3 py-2 outline-none focus:border-tp-accent/50 [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
                                         />
                                     </div>
                                     <div class="flex items-center gap-1.5">
                                         <span class="text-xs font-mono text-muted/40 font-bold">Y</span>
                                           <input
                                               v-model.number="device.mapY"
                                               @input="markDirty(device)"
                                               type="number"
                                             class="w-20 bg-tp-bg text-sm font-mono text-muted border border-tp-border/30 rounded-lg px-3 py-2 outline-none focus:border-tp-accent/50 [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
                                         />
                                     </div>
                                </div>
                            </div>

                            <!-- Blinds prefs -->
                            <template v-if="device.category === 'blinds'">
                                <div class="space-y-3">
                                     <div class="flex flex-col md:flex-row md:items-center gap-1.5 md:gap-2">
                                         <span class="text-xs font-mono text-muted/60 w-full md:w-36 shrink-0">Tiempo de Subida</span>
                                          <input
                                              :value="device.prefs.up_time"
                                              @input="updatePref(device, 'up_time', normalizeInput($event.target.value))"
                                              type="text"
                                              inputmode="decimal"
                                              placeholder="Segundos"
                                              class="w-24 bg-tp-bg text-sm font-mono text-muted border border-tp-border/30 rounded-lg px-3 py-2 outline-none focus:border-tp-accent/50"
                                          />
                                         <span class="text-xs text-muted/40 shrink-0">seg</span>
                                     </div>
                                     <div class="flex flex-col md:flex-row md:items-center gap-1.5 md:gap-2">
                                         <span class="text-xs font-mono text-muted/60 w-full md:w-36 shrink-0">Tiempo de Bajada</span>
                                          <input
                                              :value="device.prefs.down_time"
                                              @input="updatePref(device, 'down_time', normalizeInput($event.target.value))"
                                              type="text"
                                              inputmode="decimal"
                                              placeholder="Segundos"
                                              class="w-24 bg-tp-bg text-sm font-mono text-muted border border-tp-border/30 rounded-lg px-3 py-2 outline-none focus:border-tp-accent/50"
                                          />
                                         <span class="text-xs text-muted/40 shrink-0">seg</span>
                                     </div>
                                     <div class="flex flex-col md:flex-row md:items-center gap-1.5 md:gap-2">
                                         <span class="text-xs font-mono text-muted/60 w-full md:w-36 shrink-0">Posicion de Bajada</span>
                                         <input
                                             :value="device.prefs.down_pos"
                                             @input="updatePref(device, 'down_pos', Math.min(100, Math.max(0, Number($event.target.value))))"
                                             type="number"
                                             min="0"
                                             max="100"
                                             step="1"
                                             placeholder="0-100"
                                             class="w-24 bg-tp-bg text-sm font-mono text-muted border border-tp-border/30 rounded-lg px-3 py-2 outline-none focus:border-tp-accent/50 [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
                                         />
                                         <span class="text-xs text-muted/40 shrink-0">%</span>
                                     </div>
                                    <div class="flex flex-col md:flex-row md:items-center gap-1.5 md:gap-2">
                                        <span class="text-xs font-mono text-muted/60 w-full md:w-36 shrink-0">Reles Invertidos</span>
                                        <button
                                            type="button"
                                            @click.stop="updatePref(device, 'inverted_relays', !device.prefs.inverted_relays)"
                                            class="w-5 h-5 rounded border flex items-center justify-center shrink-0 transition-colors cursor-pointer"
                                            :class="device.prefs.inverted_relays
                                                ? 'bg-tp-accent border-tp-accent'
                                                : 'bg-tp-bg border-tp-border/50'"
                                        >
                                            <svg v-if="device.prefs.inverted_relays" class="w-3 h-3 text-tp-text-primary" viewBox="0 0 14 14" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                                                <polyline points="2.5 7 5.5 10.5 11.5 3.5" />
                                            </svg>
                                        </button>
                                    </div>
                                </div>
                            </template>

                            <!-- Actions -->
                            <div class="flex flex-wrap items-center gap-2 pt-2">
                                <button
                                    @click.stop="saveDevice(device)"
                                    :disabled="!hasChanges(device) || saving"
                                    class="flex items-center gap-1.5 px-4 py-2 rounded-lg text-xs font-bold uppercase tracking-wider transition-all cursor-pointer"
                                    :class="hasChanges(device) && !saving
                                        ? 'bg-tp-accent/20 text-tp-accent border border-tp-accent/30 hover:bg-tp-accent/30'
                                        : 'bg-tp-border/10 text-muted/30 border border-tp-border/20 cursor-not-allowed'"
                                >
                                    <Save class="w-3.5 h-3.5" />
                                    {{ saving ? 'Guardando...' : 'Guardar' }}
                                </button>
                                 <button
                                     @click.stop="resetDevice(device)"
                                     :disabled="!hasChanges(device)"
                                     class="flex items-center gap-1.5 px-4 py-2 rounded-lg text-xs font-bold uppercase tracking-wider transition-all cursor-pointer"
                                     :class="hasChanges(device)
                                         ? 'text-muted/60 hover:text-muted hover:bg-tp-text-primary/5 border border-tp-border/20'
                                         : 'text-muted/30 border border-tp-border/20 cursor-not-allowed'"
                                 >
                                     <RotateCcw class="w-3.5 h-3.5" />
                                     Resetear
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
