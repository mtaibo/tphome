<script setup>

    import { ref, computed, reactive, onMounted, nextTick, watch } from 'vue'
    import { Lightbulb, Blinds, Trash2, Radio, Info, ChevronRight, Crosshair, Cpu, Settings, ChevronLeft, Save, Zap } from 'lucide-vue-next'
    import { useDevices } from '@/config/devices'
    import { api } from '@/config/api'
    import { pendingDeviceId } from '@/config/sections.js'
    import ConfigWizard from './ConfigWizard.vue'
    import Btn from '@/components/Btn.vue'

    const store = useDevices()

    // --- List view ---

    const pendingDevices = ref([])
    const selectedPending = ref(null)

    async function fetchPending() {
        try {
            pendingDevices.value = (await api.getPending()).map(m => ({ mac: m }))
        } catch (error) {
            console.error('TPHome - Error fetching pending devices:', error)
        }
    }

    function startConfig(device) { selectedPending.value = device }
    function onConfigDone() { selectedPending.value = null; fetchPending(); store.setup() }
    function onConfigCancel() { selectedPending.value = null }

    onMounted(fetchPending)

    const lightDevices = computed(() =>
        Object.entries(store.storage.lights ?? {}).map(([id, d]) => ({ id, ...d, type: 'Luz', category: 'lights' }))
    )
    const blindDevices = computed(() =>
        Object.entries(store.storage.blinds ?? {}).map(([id, d]) => ({ id, ...d, type: 'Persiana', category: 'blinds' }))
    )
    const allDevices = computed(() => [...blindDevices.value, ...lightDevices.value])

    // --- Detail view ---

    const selectedDevice = ref(null)
    const devicePrefs = reactive({})
    const originalPrefs = reactive({})
    const deviceMap = reactive({})
    const originalMap = reactive({})
    const firmwareList = ref([])
    const selectedFirmware = ref(null)
    const prefLabels = {
        up_time:         'Tiempo de subida',
        down_time:       'Tiempo de bajada',
        down_pos:        'Posición de bajada',
        inverted_relays: 'Invertir relés',
    }

    const mapLabels = {
        x:      'X',
        y:      'Y',
        width:  'Ancho',
        height: 'Alto',
    }

    const prefsChanged = computed(() =>
        Object.keys(devicePrefs).some(k => String(devicePrefs[k]) !== String(originalPrefs[k]))
    )

    const mapChanged = computed(() =>
        Object.keys(deviceMap).some(k => String(deviceMap[k]) !== String(originalMap[k]))
    )

    const timeKeys = new Set(['up_time', 'down_time'])
    const percentKeys = new Set(['down_pos'])
    const focusedPrefKey = ref(null)

    function formatPrefDisplay(key, value) {
        if (timeKeys.has(key))    return (Number(value) / 100).toFixed(2) + ' s'
        if (percentKeys.has(key)) return (Number(value) / 100).toFixed(2) + ' %'
        return value
    }

    async function startEditPref(key) {
        focusedPrefKey.value = key
        await nextTick()
        document.querySelector(`[data-pref-input="${key}"]`)?.focus()
    }

    const savingPrefs = ref(false)
    const flashingFirmware = ref(false)

    async function openDevice(device) {
        selectedDevice.value = device
        Object.keys(devicePrefs).forEach(k => delete devicePrefs[k])
        Object.assign(devicePrefs, device.prefs ?? {})
        Object.keys(originalPrefs).forEach(k => delete originalPrefs[k])
        Object.assign(originalPrefs, device.prefs ?? {})
        Object.keys(deviceMap).forEach(k => delete deviceMap[k])
        Object.assign(deviceMap, device.map ?? {})
        Object.keys(originalMap).forEach(k => delete originalMap[k])
        Object.assign(originalMap, device.map ?? {})
        selectedFirmware.value = null
        firmwareList.value = []
        try { firmwareList.value = await api.getFirmwares() } catch {}
    }

    function closeDevice() { selectedDevice.value = null }

    async function pingDevice() {
        try { await api.sendCommand(selectedDevice.value.id, 'ping') }
        catch (e) { console.error('TPHome - Ping error:', e) }
    }

    async function getDeviceInfo() {
        try { await api.getDeviceInfo(selectedDevice.value.id) }
        catch (e) { console.error('TPHome - Info error:', e) }
    }

    async function resetPosition() {
        if (!confirm(`¿Reiniciar posición de ${selectedDevice.value.id} al 50%?`)) return
        try { await api.resetPosition(selectedDevice.value.id) }
        catch (e) { console.error('TPHome - Reset position error:', e) }
    }

    async function deleteDevice() {
        if (!confirm(`¿Borrar ${selectedDevice.value.name}?`)) return
        try {
            await api.deleteDevice(selectedDevice.value.id)
            closeDevice()
            await store.setup()
        } catch (e) { console.error('TPHome - Delete error:', e) }
    }

    async function savePrefs() {
        savingPrefs.value = true
        try {
            const { id, category } = selectedDevice.value
            const original = selectedDevice.value.prefs ?? {}
            const parsed = {}
            for (const [k, v] of Object.entries(devicePrefs)) {
                const orig = original[k]
                if (typeof orig === 'number') parsed[k] = Number(v)
                else if (typeof orig === 'boolean') parsed[k] = (v === 'true' || v === true)
                else parsed[k] = v
            }
            const config = await api.getConfig('devices')
            config[category][id].prefs = parsed
            await api.postConfig('devices', config)
            store.storage[category][id].prefs = parsed
            await api.sendPrefs(id, parsed)
            Object.keys(originalPrefs).forEach(k => delete originalPrefs[k])
            Object.assign(originalPrefs, parsed)
        } catch (e) { console.error('TPHome - Save prefs error:', e) }
        finally { savingPrefs.value = false }
    }

    const savingMap = ref(false)

    async function saveMap() {
        savingMap.value = true
        try {
            const { id, category } = selectedDevice.value
            const parsed = {}
            for (const [k, v] of Object.entries(deviceMap)) parsed[k] = Number(v)
            const config = await api.getConfig('devices')
            config[category][id].map = parsed
            await api.postConfig('devices', config)
            store.storage[category][id].map = parsed
            Object.keys(originalMap).forEach(k => delete originalMap[k])
            Object.assign(originalMap, parsed)
        } catch (e) { console.error('TPHome - Save map error:', e) }
        finally { savingMap.value = false }
    }

    async function flashFirmware() {
        if (!selectedFirmware.value) return
        flashingFirmware.value = true
        try { await api.sendOTA(selectedDevice.value.id, selectedFirmware.value) }
        catch (e) { console.error('TPHome - OTA error:', e) }
        finally { flashingFirmware.value = false }
    }

    watch(pendingDeviceId, (id) => {
        if (!id) return
        for (const [category, devices] of Object.entries(store.storage)) {
            if (id in devices) {
                openDevice({ ...devices[id], id, category })
                break
            }
        }
        pendingDeviceId.value = null
    }, { immediate: true })

</script>

<template>

    <div class="h-full flex flex-col">

        <!-- Desktop header -->
        <div v-if="selectedDevice" class="hidden md:flex items-center gap-4 px-8 h-[72px] shrink-0">
            <Btn :pressing="false" @click="closeDevice">
                <ChevronLeft class="w-[18px] h-[18px] text-tp-text/80" />
            </Btn>
            <component :is="selectedDevice.category === 'blinds' ? Blinds : Lightbulb" class="w-5 h-5 text-white shrink-0" />
            <span class="text-lg font-semibold text-tp-text">{{ selectedDevice.name }}</span>
            <div class="w-2 h-2 rounded-full shrink-0" :class="selectedDevice.connection?.online ? 'bg-tp-on shadow-[0_0_6px_var(--color-tp-on)]' : 'bg-tp-off'"></div>
        </div>

        <!-- LIST VIEW -->
        <div v-if="!selectedDevice" class="flex-1 overflow-y-auto px-8 pt-6 pb-8 flex flex-col gap-8">

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
                    No hay dispositivos configurados.
                </div>

                <!-- Blinds group -->
                <div v-if="blindDevices.length > 0" class="mb-6">
                    <div class="px-1 pb-3 pt-1 select-none cursor-default">
                        <p class="text-base font-semibold text-white">Persianas</p>
                    </div>
                    <div class="rounded-2xl overflow-hidden bg-[#111113] device-list">
                        <div
                            v-for="device in blindDevices"
                            :key="device.id"
                            class="flex items-center gap-4 px-4 py-3 select-none"
                            @click="openDevice(device)"
                        >
                            <div class="w-2 h-2 rounded-full shrink-0" :class="device.connection?.online ? 'bg-tp-on shadow-[0_0_6px_var(--color-tp-on)]' : 'bg-tp-off'"></div>
                            <span class="font-mono text-xs text-tp-muted shrink-0 hidden md:block">{{ device.id }}</span>
                            <span class="text-sm text-tp-text flex-1 truncate">{{ device.name }}</span>
                            <ChevronRight class="w-4 h-4 shrink-0 text-tp-muted/50" />
                        </div>
                    </div>
                </div>

                <!-- Lights group -->
                <div v-if="lightDevices.length > 0" class="mb-6">
                    <div class="px-1 pb-3 pt-1 select-none cursor-default">
                        <p class="text-base font-semibold text-white">Luces</p>
                    </div>
                    <div class="rounded-2xl overflow-hidden bg-[#111113] device-list">
                        <div
                            v-for="device in lightDevices"
                            :key="device.id"
                            class="flex items-center gap-4 px-4 py-3 select-none"
                            @click="openDevice(device)"
                        >
                            <div class="w-2 h-2 rounded-full shrink-0" :class="device.connection?.online ? 'bg-tp-on shadow-[0_0_6px_var(--color-tp-on)]' : 'bg-tp-off'"></div>
                            <span class="font-mono text-xs text-tp-muted shrink-0 hidden md:block">{{ device.id }}</span>
                            <span class="text-sm text-tp-text flex-1 truncate">{{ device.name }}</span>
                            <ChevronRight class="w-4 h-4 shrink-0 text-tp-muted/50" />
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

        <!-- DETAIL VIEW -->
        <div v-else class="flex-1 overflow-y-auto px-8 pb-8 flex flex-col gap-6">

            <!-- Mobile back + title -->
            <div class="md:hidden flex items-center gap-3 pt-4">
                <Btn :pressing="false" @click="closeDevice">
                    <ChevronLeft class="w-[18px] h-[18px] text-tp-text/80" />
                </Btn>
                <span class="text-lg font-semibold text-tp-text">{{ selectedDevice.name }}</span>
            </div>

            <!-- Actions -->
            <div class="pt-2">
                <p class="text-base font-semibold text-white px-1 pb-3">Acciones</p>
                <div class="rounded-2xl overflow-hidden bg-[#111113] device-list">
                    <button @click="pingDevice()" class="action-row">
                        <Radio class="w-4 h-4 shrink-0" /><span>Ping</span>
                    </button>
                    <button @click="getDeviceInfo()" class="action-row">
                        <Info class="w-4 h-4 shrink-0" /><span>Actualizar información</span>
                    </button>
                    <button v-if="selectedDevice.category === 'blinds'" @click="resetPosition()" class="action-row">
                        <Crosshair class="w-4 h-4 shrink-0" /><span>Reiniciar posición</span>
                    </button>
                    <button @click="deleteDevice()" class="action-row action-row-danger">
                        <Trash2 class="w-4 h-4 shrink-0" /><span>Eliminar dispositivo</span>
                    </button>
                </div>
            </div>

            <!-- Prefs + Firmware side by side -->
            <div class="flex gap-6 items-start">

                <!-- Prefs editor -->
                <div v-if="Object.keys(devicePrefs).length > 0" class="flex-1 min-w-0">
                    <p class="text-base font-semibold text-white px-1 pb-3">Preferencias</p>
                    <div class="rounded-2xl overflow-hidden bg-[#111113] device-list mb-3">
                        <div
                            v-for="(value, key) in devicePrefs"
                            :key="key"
                            class="flex items-center gap-4 px-4 py-3"
                        >
                            <span class="text-sm text-tp-text flex-1">{{ prefLabels[key] ?? key }}</span>
                            <div
                                v-if="typeof value === 'boolean'"
                                class="pref-checkbox select-none"
                                :class="devicePrefs[key] ? 'pref-checkbox--on' : ''"
                                @click="devicePrefs[key] = !devicePrefs[key]"
                            />
                            <div
                                v-else-if="(timeKeys.has(key) || percentKeys.has(key)) && focusedPrefKey !== key"
                                class="pref-input pref-input-display"
                                @click="startEditPref(key)"
                            >{{ formatPrefDisplay(key, devicePrefs[key]) }}</div>
                            <input
                                v-else
                                v-model="devicePrefs[key]"
                                class="pref-input"
                                :data-pref-input="key"
                                :type="typeof value === 'number' ? 'number' : 'text'"
                                @blur="focusedPrefKey = null"
                            />
                        </div>
                    </div>
                    <Transition name="btn-fade">
                        <button v-if="prefsChanged || savingPrefs" @click="savePrefs()" class="action-primary">
                            <Save class="w-4 h-4 shrink-0" />
                            <span>{{ savingPrefs ? 'Guardando…' : 'Guardar y enviar' }}</span>
                        </button>
                    </Transition>
                </div>

                <!-- Map editor -->
                <div v-if="Object.keys(deviceMap).length > 0" class="flex-1 min-w-0">
                    <p class="text-base font-semibold text-white px-1 pb-3">Posición</p>
                    <div class="rounded-2xl overflow-hidden bg-[#111113] device-list mb-3">
                        <div
                            v-for="(value, key) in deviceMap"
                            :key="key"
                            class="flex items-center gap-4 px-4 py-3"
                        >
                            <span class="text-sm text-tp-text flex-1">{{ mapLabels[key] ?? key }}</span>
                            <input
                                v-model="deviceMap[key]"
                                type="number"
                                class="pref-input"
                            />
                        </div>
                    </div>
                    <Transition name="btn-fade">
                        <button v-if="mapChanged || savingMap" @click="saveMap()" class="action-primary">
                            <Save class="w-4 h-4 shrink-0" />
                            <span>{{ savingMap ? 'Guardando…' : 'Guardar y enviar' }}</span>
                        </button>
                    </Transition>
                </div>

                <!-- Firmware selector -->
                <div class="flex-1 min-w-0">
                    <p class="text-base font-semibold text-white px-1 pb-3">Firmware</p>
                    <div v-if="firmwareList.length === 0" class="text-sm text-tp-muted/50 italic px-1 mb-3">
                        No hay firmwares disponibles.
                    </div>
                    <div v-else class="rounded-2xl overflow-hidden bg-[#111113] device-list mb-3">
                        <div
                            v-for="fw in firmwareList"
                            :key="fw.version"
                            class="flex items-center gap-4 px-4 py-3 select-none"
                            @click="selectedFirmware = selectedFirmware === fw.version ? null : fw.version"
                        >
                            <div class="w-4 h-4 rounded-full border border-tp-muted/40 flex items-center justify-center shrink-0">
                                <div v-if="selectedFirmware === fw.version" class="w-2 h-2 rounded-full bg-tp-accent"></div>
                            </div>
                            <div class="flex-1 min-w-0">
                                <p class="text-sm text-tp-text truncate">{{ fw.name }}</p>
                                <p class="text-xs font-mono text-tp-muted">v{{ fw.version }} · {{ fw.chip }}</p>
                            </div>
                            <span v-if="fw.active" class="text-xs text-tp-on font-mono uppercase tracking-wider shrink-0">Activo</span>
                        </div>
                    </div>
                    <Transition name="btn-fade">
                        <button v-if="selectedFirmware || flashingFirmware" @click="flashFirmware()" class="action-primary">
                            <Zap class="w-4 h-4 shrink-0" />
                            <span>{{ flashingFirmware ? 'Subiendo…' : 'Subir firmware' }}</span>
                        </button>
                    </Transition>
                </div>

            </div>

        </div>

    </div>

</template>

<style scoped>
    .device-list > div {
        position: relative;
    }
    .device-list > div + div::before {
        content: '';
        position: absolute;
        top: 0;
        left: 16px;
        right: 16px;
        height: 0.5px;
        background: rgba(255, 255, 255, 0.06);
        pointer-events: none;
    }

    .action-row {
        display: flex;
        align-items: center;
        gap: 12px;
        width: 100%;
        padding: 12px 16px;
        font-size: 0.875rem;
        color: var(--color-tp-muted);
        transition: color 0.15s ease, background 0.15s ease;
        cursor: default;
        text-align: left;
    }
    .action-row:hover {
        color: var(--color-tp-text);
    }
    .action-row-danger:hover {
        color: var(--color-tp-text);
    }

    .pref-input-display {
        cursor: default;
        display: flex;
        align-items: center;
        justify-content: flex-end;
    }

    .pref-checkbox {
        position: relative;
        width: 20px;
        height: 20px;
        background: rgba(255, 255, 255, 0.06);
        border: 0.5px solid rgba(255, 255, 255, 0.12);
        border-radius: 8px;
        cursor: default;
        transition: background 0.15s ease, border-color 0.15s ease;
        flex-shrink: 0;
    }
    .pref-checkbox--on {
        background: var(--color-tp-accent);
        border-color: var(--color-tp-accent);
    }

    .pref-input {
        cursor: default;
        background: rgba(255, 255, 255, 0.06);
        border: 0.5px solid rgba(255, 255, 255, 0.12);
        border-radius: 8px;
        padding: 5px 10px;
        font-size: 0.8125rem;
        font-family: inherit;
        color: var(--color-tp-text);
        width: 80px;
        text-align: right;
        outline: none;
        transition: border-color 0.15s ease;
    }
    .pref-input:focus {
        outline: none;
    }
    .pref-input::-webkit-outer-spin-button,
    .pref-input::-webkit-inner-spin-button {
        -webkit-appearance: none;
    }
    .pref-input[type=number] {
        -moz-appearance: textfield;
    }

    .action-primary {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 10px 18px;
        border-radius: 14px;
        background: linear-gradient(
            145deg,
            rgba(255, 255, 255, 0.14) 0%,
            rgba(255, 255, 255, 0.07) 50%,
            rgba(255, 255, 255, 0.10) 100%
        );
        backdrop-filter: blur(24px) saturate(200%);
        -webkit-backdrop-filter: blur(24px) saturate(200%);
        border: 0.5px solid rgba(255, 255, 255, 0.22);
        box-shadow:
            inset 0 1px 0 rgba(255, 255, 255, 0.36),
            inset 0 -0.5px 0 rgba(0, 0, 0, 0.18),
            0 4px 12px rgba(0, 0, 0, 0.24),
            0 1px 3px rgba(0, 0, 0, 0.14);
        color: var(--color-tp-text);
        font-size: 0.875rem;
        font-weight: 500;
        cursor: default;
        transition: background 0.18s ease, box-shadow 0.18s ease;
    }
    .action-primary:hover {
        background: linear-gradient(
            145deg,
            rgba(255, 255, 255, 0.20) 0%,
            rgba(255, 255, 255, 0.11) 50%,
            rgba(255, 255, 255, 0.16) 100%
        );
        box-shadow:
            inset 0 1px 0 rgba(255, 255, 255, 0.42),
            inset 0 -0.5px 0 rgba(0, 0, 0, 0.18),
            0 6px 18px rgba(0, 0, 0, 0.30),
            0 1px 3px rgba(0, 0, 0, 0.14);
    }

    .btn-fade-enter-active,
    .btn-fade-leave-active {
        transition: opacity 0.2s ease, transform 0.2s ease;
    }
    .btn-fade-enter-from,
    .btn-fade-leave-to {
        opacity: 0;
        transform: translateY(4px);
    }
</style>
