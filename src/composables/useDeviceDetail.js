import { ref, reactive, computed, nextTick } from 'vue'
import { api } from '@/config/api'
import { useDevices } from '@/config/devices'

export function useDeviceDetail() {

    const store = useDevices()

    const selectedDevice   = ref(null)
    const devicePrefs      = reactive({})
    const originalPrefs    = reactive({})
    const deviceMap        = reactive({})
    const originalMap      = reactive({})
    const firmwareList     = ref([])
    const selectedFirmware = ref(null)
    const savingPrefs      = ref(false)
    const savingMap        = ref(false)
    const flashingFirmware = ref(false)
    const focusedPrefKey   = ref(null)

    const prefLabels = {
        up_time:         'Tiempo de subida',
        down_time:       'Tiempo de bajada',
        down_pos:        'Posición de bajada',
        inverted_relays: 'Invertir relés',
    }
    const mapLabels   = { x: 'X', y: 'Y', width: 'Ancho', height: 'Alto' }
    const timeKeys    = new Set(['up_time', 'down_time'])
    const percentKeys = new Set(['down_pos'])

    const prefsChanged = computed(() =>
        Object.keys(devicePrefs).some(k => String(devicePrefs[k]) !== String(originalPrefs[k]))
    )
    const mapChanged = computed(() =>
        Object.keys(deviceMap).some(k => String(deviceMap[k]) !== String(originalMap[k]))
    )

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

    function resetObj(obj, source) {
        Object.keys(obj).forEach(k => delete obj[k])
        Object.assign(obj, source)
    }

    async function open(device) {
        selectedDevice.value = device
        resetObj(devicePrefs,   device.prefs ?? {})
        resetObj(originalPrefs, device.prefs ?? {})
        resetObj(deviceMap,     device.map   ?? {})
        resetObj(originalMap,   device.map   ?? {})
        selectedFirmware.value = null
        firmwareList.value = []
        try { firmwareList.value = await api.getFirmwares() } catch {}
    }

    function close() { selectedDevice.value = null }

    async function ping() {
        try { await api.sendCommand(selectedDevice.value.id, 'ping') }
        catch (e) { console.error('TPHome - Ping error:', e) }
    }

    async function getInfo() {
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
            close()
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
                if (typeof orig === 'number')       parsed[k] = Number(v)
                else if (typeof orig === 'boolean') parsed[k] = (v === 'true' || v === true)
                else parsed[k] = v
            }
            const config = await api.getConfig('devices')
            config[category][id].prefs = parsed
            await api.postConfig('devices', config)
            store.storage[category][id].prefs = parsed
            await api.sendPrefs(id, parsed)
            resetObj(originalPrefs, parsed)
        } catch (e) { console.error('TPHome - Save prefs error:', e) }
        finally { savingPrefs.value = false }
    }

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
            resetObj(originalMap, parsed)
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

    return {
        selectedDevice, devicePrefs, deviceMap,
        firmwareList, selectedFirmware,
        savingPrefs, savingMap, flashingFirmware, focusedPrefKey,
        prefLabels, mapLabels, timeKeys, percentKeys,
        prefsChanged, mapChanged,
        formatPrefDisplay, startEditPref,
        open, close, ping, getInfo, resetPosition, deleteDevice,
        savePrefs, saveMap, flashFirmware,
    }
}
