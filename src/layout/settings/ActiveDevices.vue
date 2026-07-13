<script setup>

    import { ref, computed, onMounted } from 'vue'
    import { Lightbulb, Blinds, Trash2, Radio, Info, Braces, ChevronDown, Download, Crosshair, Cpu, Settings } from 'lucide-vue-next'
    import { useRoute } from 'vue-router'

    import { useDevices } from '@/config/devices'
    import { api } from '@/config/api'
    import ConfigWizard from './ConfigWizard.vue'

    const store = useDevices()
    const route = useRoute()

    const expandedId = ref(null)

    const pendingDevices = ref([])
    const selectedPending = ref(null)

    async function fetchPending() {
        try {
            pendingDevices.value = (await api.getPending()).map(m => ({ mac: m }))
        } catch (error) {
            console.error('TPHome - Error fetching pending devices:', error)
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

    onMounted(() => {
        if (route.query.device) expandedId.value = route.query.device
        fetchPending()
    })

    function toggleExpanded(id) {
        expandedId.value = expandedId.value === id ? null : id
    }

    const allDevices = computed(() => {
        const lights = Object.entries(store.lights).map(([id, d]) => ({ id, ...d, type: 'Luz', category: 'lights' }))
        const blinds = Object.entries(store.blinds).map(([id, d]) => ({ id, ...d, type: 'Persiana', category: 'blinds' }))
        return [...blinds, ...lights]
    })

    async function pingDevice(id) {
        try { await api.sendCommand(id, 'ping') }
        catch (error) { console.error('TPHome - Ping error:', error) }
    }

    async function getDeviceInfo(id) {
        try { await api.getDeviceInfo(id) }
        catch (error) { console.error('TPHome - Info error:', error) }
    }

    async function sendPrefsDevice(id, prefs) {
        try { await api.sendPrefs(id, prefs) }
        catch (error) { console.error('TPHome - Prefs error:', error) }
    }

    async function resetPosition(id) {
        if (!confirm(`¿Reiniciar posición de ${id} al 50%?`)) return
        try { await api.resetPosition(id) }
        catch (error) { console.error('TPHome - Reset position error:', error) }
    }

    async function deleteDevice(id) {
        if (!confirm(`¿Borrar ${id}?`)) return
        try {
            await api.deleteDevice(id)
            await store.setup()
        } catch (error) {
            console.error('TPHome - Error deleting device:', error)
        }
    }

    async function updateFirmware(id) {
        if (!confirm(`¿Actualizar firmware de ${id}? El dispositivo descargará el firmware activo.`)) return
        try {
            const firmwares = await api.getFirmwares()
            const activeFw = firmwares.find(fw => fw.active)
            if (!activeFw) {
                alert('No hay firmware activo. Activa uno primero.')
                return
            }
            await api.sendOTA(id, activeFw.version)
        }
        catch (error) { console.error('TPHome - OTA error:', error) }
    }

</script>

<template>

    <div class="h-full flex flex-col p-8 gap-8 overflow-y-auto">

        <section v-if="pendingDevices.length > 0">
            <div class="flex items-center gap-3 mb-5">
                <div class="w-2 h-2 rounded-full bg-tp-off shadow-[0_0_6px_var(--color-tp-off)] animate-pulse"></div>
                <h2 class="text-sm font-bold uppercase tracking-widest text-tp-muted">
                    Sin configurar
                    <span class="text-tp-off font-mono ml-1.5">{{ pendingDevices.length }}</span>
                </h2>
            </div>

            <div class="space-y-2">
                <div
                    v-for="device in pendingDevices"
                    :key="device.mac"
                    class="flex items-center gap-4 px-4 py-3 rounded-xl bg-tp-surface border border-tp-off/30 hover:border-tp-off/50 transition-colors"
                >
                    <div class="w-2 h-2 rounded-full shrink-0 bg-tp-off shadow-[0_0_6px_var(--color-tp-off)] animate-pulse"></div>
                    <Cpu class="w-4 h-4 shrink-0 text-tp-muted" />
                    <span class="font-mono text-xs text-tp-muted flex-1">{{ device.mac }}</span>
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

        <section>
            <div v-if="allDevices.length === 0" class="text-sm text-tp-muted/50 italic px-1">
                No hay dispositivos configurados en el mapa.
            </div>

            <div v-else class="space-y-2">
                <div
                    v-for="device in allDevices"
                    :key="device.id"
                    class="rounded-xl bg-tp-surface border border-tp-border hover:border-tp-border/60 transition-colors overflow-hidden"
                >
                    <!-- Desktop layout -->
                    <div class="hidden md:block">
                        <div
                            class="flex items-center gap-4 px-4 py-3 cursor-pointer select-none"
                            @click="toggleExpanded(device.id)"
                        >
                            <component
                                :is="device.type === 'Luz' ? Lightbulb : Blinds"
                                class="w-4 h-4 shrink-0"
                                :class="device.type === 'Luz' ? 'text-tp-light-on/70' : 'text-tp-accent/70'"
                            />
                            <span class="font-mono text-xs text-tp-muted w-16 shrink-0">{{ device.id }}</span>
                            <span class="text-sm text-tp-text flex-1 truncate">{{ device.name }}</span>
                            <div
                                class="w-2 h-2 rounded-full shrink-0"
                                :class="device.connection?.online ? 'bg-tp-on shadow-[0_0_6px_var(--color-tp-on)]' : 'bg-tp-off'"
                            ></div>
                            <ChevronDown
                                class="w-4 h-4 shrink-0 text-tp-muted transition-transform duration-200"
                                :class="{ 'rotate-180': expandedId === device.id }"
                            />
                        </div>

                        <div
                            class="expand-content"
                            :class="{ 'expand-open': expandedId === device.id }"
                        >
                            <div class="border-t border-tp-border/50 px-4 py-2 bg-black/10">
                                <button
                                    @click.stop="pingDevice(device.id)"
                                    class="flex items-center gap-3 w-full px-3 py-2 rounded-lg text-sm text-tp-muted hover:text-tp-accent hover:bg-tp-accent/10 transition-all cursor-pointer"
                                >
                                    <Radio class="w-4 h-4 shrink-0" />
                                    <span>Ping</span>
                                </button>
                                <button
                                    @click.stop="sendPrefsDevice(device.id, device.prefs)"
                                    class="flex items-center gap-3 w-full px-3 py-2 rounded-lg text-sm text-tp-muted hover:text-tp-accent hover:bg-tp-accent/10 transition-all cursor-pointer"
                                >
                                    <Braces class="w-4 h-4 shrink-0" />
                                    <span>Mandar preferencias</span>
                                </button>
                                <button
                                    @click.stop="updateFirmware(device.id)"
                                    class="flex items-center gap-3 w-full px-3 py-2 rounded-lg text-sm text-tp-muted hover:text-tp-accent hover:bg-tp-accent/10 transition-all cursor-pointer"
                                >
                                    <Download class="w-4 h-4 shrink-0" />
                                    <span>Cambiar firmware</span>
                                </button>
                                <button
                                    @click.stop="getDeviceInfo(device.id)"
                                    class="flex items-center gap-3 w-full px-3 py-2 rounded-lg text-sm text-tp-muted hover:text-tp-accent hover:bg-tp-accent/10 transition-all cursor-pointer"
                                >
                                    <Info class="w-4 h-4 shrink-0" />
                                    <span>Actualizar información</span>
                                </button>
                                <button
                                    v-if="device.type === 'Persiana'"
                                    @click.stop="resetPosition(device.id)"
                                    class="flex items-center gap-3 w-full px-3 py-2 rounded-lg text-sm text-tp-muted hover:text-tp-accent hover:bg-tp-accent/10 transition-all cursor-pointer"
                                >
                                    <Crosshair class="w-4 h-4 shrink-0" />
                                    <span>Reiniciar posición</span>
                                </button>
                                <button
                                    @click.stop="deleteDevice(device.id)"
                                    class="flex items-center gap-3 w-full px-3 py-2 rounded-lg text-sm text-tp-muted hover:text-tp-off hover:bg-tp-off/10 transition-all cursor-pointer"
                                >
                                    <Trash2 class="w-4 h-4 shrink-0" />
                                    <span>Eliminar dispositivo</span>
                                </button>
                            </div>
                        </div>
                    </div>

                    <!-- Mobile layout -->
                    <div class="md:hidden">
                        <div
                            class="flex items-center gap-3 px-4 py-3 cursor-pointer select-none"
                            @click="toggleExpanded(device.id)"
                        >
                            <component
                                :is="device.type === 'Luz' ? Lightbulb : Blinds"
                                class="w-4 h-4 shrink-0"
                                :class="device.type === 'Luz' ? 'text-tp-light-on/70' : 'text-tp-accent/70'"
                            />
                            <span class="text-sm text-tp-text flex-1 truncate min-w-0">{{ device.name }}</span>
                            <span class="text-xs font-mono text-tp-muted shrink-0 whitespace-nowrap">{{ device.id }}</span>
                            <div
                                class="w-2 h-2 rounded-full shrink-0"
                                :class="device.connection?.online ? 'bg-tp-on shadow-[0_0_6px_var(--color-tp-on)]' : 'bg-tp-off'"
                            ></div>
                            <ChevronDown
                                class="w-4 h-4 shrink-0 text-tp-muted transition-transform duration-200"
                                :class="{ 'rotate-180': expandedId === device.id }"
                            />
                        </div>

                        <div
                            class="expand-content"
                            :class="{ 'expand-open': expandedId === device.id }"
                        >
                            <div class="border-t border-tp-border/50 px-4 py-2 bg-black/10">
                                <button
                                    @click.stop="pingDevice(device.id)"
                                    class="flex items-center gap-3 w-full px-3 py-2 rounded-lg text-sm text-tp-muted hover:text-tp-accent hover:bg-tp-accent/10 transition-all cursor-pointer"
                                >
                                    <Radio class="w-4 h-4 shrink-0" />
                                    <span>Ping</span>
                                </button>
                                <button
                                    @click.stop="sendPrefsDevice(device.id, device.prefs)"
                                    class="flex items-center gap-3 w-full px-3 py-2 rounded-lg text-sm text-tp-muted hover:text-tp-accent hover:bg-tp-accent/10 transition-all cursor-pointer"
                                >
                                    <Braces class="w-4 h-4 shrink-0" />
                                    <span>Mandar preferencias</span>
                                </button>
                                <button
                                    @click.stop="updateFirmware(device.id)"
                                    class="flex items-center gap-3 w-full px-3 py-2 rounded-lg text-sm text-tp-muted hover:text-tp-accent hover:bg-tp-accent/10 transition-all cursor-pointer"
                                >
                                    <Download class="w-4 h-4 shrink-0" />
                                    <span>Cambiar firmware</span>
                                </button>
                                <button
                                    @click.stop="getDeviceInfo(device.id)"
                                    class="flex items-center gap-3 w-full px-3 py-2 rounded-lg text-sm text-tp-muted hover:text-tp-accent hover:bg-tp-accent/10 transition-all cursor-pointer"
                                >
                                    <Info class="w-4 h-4 shrink-0" />
                                    <span>Actualizar información</span>
                                </button>
                                <button
                                    v-if="device.type === 'Persiana'"
                                    @click.stop="resetPosition(device.id)"
                                    class="flex items-center gap-3 w-full px-3 py-2 rounded-lg text-sm text-tp-muted hover:text-tp-accent hover:bg-tp-accent/10 transition-all cursor-pointer"
                                >
                                    <Crosshair class="w-4 h-4 shrink-0" />
                                    <span>Reiniciar posición</span>
                                </button>
                                <button
                                    @click.stop="deleteDevice(device.id)"
                                    class="flex items-center gap-3 w-full px-3 py-2 rounded-lg text-sm text-tp-muted hover:text-tp-off hover:bg-tp-off/10 transition-all cursor-pointer"
                                >
                                    <Trash2 class="w-4 h-4 shrink-0" />
                                    <span>Eliminar dispositivo</span>
                                </button>
                            </div>
                        </div>
                    </div>
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

<style scoped>
    .expand-content {
        max-height: 0;
        overflow: hidden;
        transition: max-height 0.4s ease-out;
    }

    .expand-open {
        max-height: 300px;
    }
</style>
