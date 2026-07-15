<script setup>

    import { ref, computed, onMounted } from 'vue'
    import { Lightbulb, Blinds, Trash2, Radio, Info, Braces, ChevronDown, Download, Crosshair, Cpu, Settings, ChevronLeft } from 'lucide-vue-next'
    import { useRoute } from 'vue-router'

    import { useDevices } from '@/config/devices'
    import { api } from '@/config/api'
    import ConfigWizard from './ConfigWizard.vue'
    import Btn from '@/components/Btn.vue'

    const store = useDevices()
    const route = useRoute()

    const expandedId = ref(null)
    const lightsOpen = ref(true)
    const blindsOpen = ref(true)

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

    const lightDevices = computed(() =>
        Object.entries(store.storage.lights ?? {}).map(([id, d]) => ({ id, ...d, type: 'Luz', category: 'lights' }))
    )

    const blindDevices = computed(() =>
        Object.entries(store.storage.blinds ?? {}).map(([id, d]) => ({ id, ...d, type: 'Persiana', category: 'blinds' }))
    )

    const allDevices = computed(() => [...blindDevices.value, ...lightDevices.value])

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

    <div class="h-full flex flex-col">

        <div class="hidden md:flex items-center px-8 h-[72px] shrink-0">
            <Btn :pressing="false">
                <ChevronLeft class="w-[18px] h-[18px] text-tp-text/80" />
            </Btn>
        </div>

        <div class="flex-1 overflow-y-auto px-8 pb-8 flex flex-col gap-8">

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

                <!-- Blinds group -->
                <div v-if="blindDevices.length > 0" class="mb-6">
                    <div
                        class="px-1 pb-3 pt-1 select-none cursor-pointer"
                        @click="blindsOpen = !blindsOpen"
                    >
                        <p class="text-xs font-semibold text-white">Persianas</p>
                    </div>

                    <div v-if="blindsOpen" class="space-y-2">
                        <div
                            v-for="device in blindDevices"
                            :key="device.id"
                            class="device-card"
                        >
                            <!-- Desktop layout -->
                            <div class="hidden md:block">
                                <div
                                    class="flex items-center gap-4 px-4 py-3 cursor-pointer select-none"
                                    @click="toggleExpanded(device.id)"
                                >
                                    <Blinds class="w-4 h-4 shrink-0 text-tp-accent/70" />
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

                                <div class="expand-content" :class="{ 'expand-open': expandedId === device.id }">
                                    <div class="expand-panel px-4 py-2">
                                        <button @click.stop="pingDevice(device.id)" class="action-btn">
                                            <Radio class="w-4 h-4 shrink-0" /><span>Ping</span>
                                        </button>
                                        <button @click.stop="sendPrefsDevice(device.id, device.prefs)" class="action-btn">
                                            <Braces class="w-4 h-4 shrink-0" /><span>Mandar preferencias</span>
                                        </button>
                                        <button @click.stop="resetPosition(device.id)" class="action-btn">
                                            <Crosshair class="w-4 h-4 shrink-0" /><span>Reiniciar posición</span>
                                        </button>
                                        <button @click.stop="updateFirmware(device.id)" class="action-btn">
                                            <Download class="w-4 h-4 shrink-0" /><span>Cambiar firmware</span>
                                        </button>
                                        <button @click.stop="getDeviceInfo(device.id)" class="action-btn">
                                            <Info class="w-4 h-4 shrink-0" /><span>Actualizar información</span>
                                        </button>
                                        <button @click.stop="deleteDevice(device.id)" class="action-btn action-btn-danger">
                                            <Trash2 class="w-4 h-4 shrink-0" /><span>Eliminar dispositivo</span>
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
                                    <Blinds class="w-4 h-4 shrink-0 text-tp-accent/70" />
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

                                <div class="expand-content" :class="{ 'expand-open': expandedId === device.id }">
                                    <div class="expand-panel px-4 py-2">
                                        <button @click.stop="pingDevice(device.id)" class="action-btn">
                                            <Radio class="w-4 h-4 shrink-0" /><span>Ping</span>
                                        </button>
                                        <button @click.stop="sendPrefsDevice(device.id, device.prefs)" class="action-btn">
                                            <Braces class="w-4 h-4 shrink-0" /><span>Mandar preferencias</span>
                                        </button>
                                        <button @click.stop="resetPosition(device.id)" class="action-btn">
                                            <Crosshair class="w-4 h-4 shrink-0" /><span>Reiniciar posición</span>
                                        </button>
                                        <button @click.stop="updateFirmware(device.id)" class="action-btn">
                                            <Download class="w-4 h-4 shrink-0" /><span>Cambiar firmware</span>
                                        </button>
                                        <button @click.stop="getDeviceInfo(device.id)" class="action-btn">
                                            <Info class="w-4 h-4 shrink-0" /><span>Actualizar información</span>
                                        </button>
                                        <button @click.stop="deleteDevice(device.id)" class="action-btn action-btn-danger">
                                            <Trash2 class="w-4 h-4 shrink-0" /><span>Eliminar dispositivo</span>
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Lights group -->
                <div v-if="lightDevices.length > 0" class="mb-6">
                    <div
                        class="px-1 pb-3 pt-1 select-none cursor-pointer"
                        @click="lightsOpen = !lightsOpen"
                    >
                        <p class="text-xs font-semibold text-white">Luces</p>
                    </div>

                    <div v-if="lightsOpen" class="space-y-2">
                        <div
                            v-for="device in lightDevices"
                            :key="device.id"
                            class="device-card"
                        >
                            <!-- Desktop layout -->
                            <div class="hidden md:block">
                                <div
                                    class="flex items-center gap-4 px-4 py-3 cursor-pointer select-none"
                                    @click="toggleExpanded(device.id)"
                                >
                                    <Lightbulb class="w-4 h-4 shrink-0 text-tp-light-on/70" />
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

                                <div class="expand-content" :class="{ 'expand-open': expandedId === device.id }">
                                    <div class="expand-panel px-4 py-2">
                                        <button @click.stop="pingDevice(device.id)" class="action-btn">
                                            <Radio class="w-4 h-4 shrink-0" /><span>Ping</span>
                                        </button>
                                        <button @click.stop="sendPrefsDevice(device.id, device.prefs)" class="action-btn">
                                            <Braces class="w-4 h-4 shrink-0" /><span>Mandar preferencias</span>
                                        </button>
                                        <button @click.stop="updateFirmware(device.id)" class="action-btn">
                                            <Download class="w-4 h-4 shrink-0" /><span>Cambiar firmware</span>
                                        </button>
                                        <button @click.stop="getDeviceInfo(device.id)" class="action-btn">
                                            <Info class="w-4 h-4 shrink-0" /><span>Actualizar información</span>
                                        </button>
                                        <button @click.stop="deleteDevice(device.id)" class="action-btn action-btn-danger">
                                            <Trash2 class="w-4 h-4 shrink-0" /><span>Eliminar dispositivo</span>
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
                                    <Lightbulb class="w-4 h-4 shrink-0 text-tp-light-on/70" />
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

                                <div class="expand-content" :class="{ 'expand-open': expandedId === device.id }">
                                    <div class="expand-panel px-4 py-2">
                                        <button @click.stop="pingDevice(device.id)" class="action-btn">
                                            <Radio class="w-4 h-4 shrink-0" /><span>Ping</span>
                                        </button>
                                        <button @click.stop="sendPrefsDevice(device.id, device.prefs)" class="action-btn">
                                            <Braces class="w-4 h-4 shrink-0" /><span>Mandar preferencias</span>
                                        </button>
                                        <button @click.stop="updateFirmware(device.id)" class="action-btn">
                                            <Download class="w-4 h-4 shrink-0" /><span>Cambiar firmware</span>
                                        </button>
                                        <button @click.stop="getDeviceInfo(device.id)" class="action-btn">
                                            <Info class="w-4 h-4 shrink-0" /><span>Actualizar información</span>
                                        </button>
                                        <button @click.stop="deleteDevice(device.id)" class="action-btn action-btn-danger">
                                            <Trash2 class="w-4 h-4 shrink-0" /><span>Eliminar dispositivo</span>
                                        </button>
                                    </div>
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

    </div>

</template>

<style scoped>
    .device-card {
        border-radius: 14px;
        background: linear-gradient(
            145deg,
            rgba(255, 255, 255, 0.09) 0%,
            rgba(255, 255, 255, 0.04) 100%
        );
        backdrop-filter: blur(20px) saturate(180%);
        -webkit-backdrop-filter: blur(20px) saturate(180%);
        border: 0.5px solid rgba(255, 255, 255, 0.14);
        box-shadow:
            inset 0 1px 0 rgba(255, 255, 255, 0.20),
            inset 0 -0.5px 0 rgba(0, 0, 0, 0.12),
            0 4px 16px rgba(0, 0, 0, 0.18);
        overflow: hidden;
        transition: background 0.18s ease, box-shadow 0.18s ease;
    }

    .device-card:hover {
        background: linear-gradient(
            145deg,
            rgba(255, 255, 255, 0.13) 0%,
            rgba(255, 255, 255, 0.07) 100%
        );
        box-shadow:
            inset 0 1px 0 rgba(255, 255, 255, 0.26),
            inset 0 -0.5px 0 rgba(0, 0, 0, 0.12),
            0 6px 20px rgba(0, 0, 0, 0.24);
    }

    .expand-content {
        max-height: 0;
        overflow: hidden;
        transition: max-height 0.4s ease-out;
    }

    .expand-open {
        max-height: 300px;
    }

    .expand-panel {
        border-top: 0.5px solid rgba(255, 255, 255, 0.08);
        background: rgba(0, 0, 0, 0.12);
    }

    .action-btn {
        display: flex;
        align-items: center;
        gap: 12px;
        width: 100%;
        padding: 8px 12px;
        border-radius: 8px;
        font-size: 0.875rem;
        color: var(--color-tp-muted);
        transition: color 0.15s ease, background 0.15s ease;
        cursor: pointer;
    }

    .action-btn:hover {
        color: var(--color-tp-accent);
        background: color-mix(in srgb, var(--color-tp-accent) 10%, transparent);
    }

    .action-btn-danger:hover {
        color: var(--color-tp-off);
        background: color-mix(in srgb, var(--color-tp-off) 10%, transparent);
    }
</style>
