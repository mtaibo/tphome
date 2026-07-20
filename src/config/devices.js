import { defineStore } from 'pinia'
import { reactive, computed } from 'vue'

import { api } from './api'

export const useDevices = defineStore('devices', () => {

    const storage        = reactive({})
    const unconfigured   = computed(() => Object.keys(storage).length === 0)
    const blinds         = computed(() =>
        Object.fromEntries(
            Object.entries(storage.blinds ?? {}).filter(([, d]) => d.state != null)
        )
    )
    const lights         = computed(() =>
        Object.fromEntries(
            Object.entries(storage.lights ?? {}).filter(([, d]) => d.state != null)
        )
    )
    const active         = computed(() =>
        Object.values(storage.blinds ?? {}).filter(d => d.connection?.online).length
    )

    async function setup() {
        try {
            const config = await api.getConfig('devices')
            if (Object.keys(config).length === 0) return

            for (const device of Object.keys(storage)) delete storage[device]

            for (const [category, devices] of Object.entries(config)) {
                if (!storage[category]) storage[category] = {}
                for (const [id, device] of Object.entries(devices)) {
                    storage[category][id] = {
                        name:       device.name,
                        map:        { ...device.map },
                        prefs:      { ...device.prefs },
                        state:      null,
                        connection: null,
                    }
                }
            }

            await update()
        } catch (error) { console.error('TPHome - Setup error:', error) }
    }

    async function update() {
        try {
            const devices = await api.getDevices()
            for (const device of devices) {
                const category = Object.keys(storage).find(cat => device.id in storage[cat])
                if (!category) continue

                storage[category][device.id].connection = { ...device.connection }
                storage[category][device.id].state      = { ...device.state }

                const configPrefs  = storage[category][device.id].prefs
                const currentPrefs = device.prefs
                const notSync = Object.keys(configPrefs).some(k => configPrefs[k] !== currentPrefs[k])
                if (notSync) await api.sendPrefs(device.id, configPrefs)
            }
        } catch (error) { console.error('TPHome - Update error:', error) }
    }

    return { storage, unconfigured, blinds, lights, active, setup, update }
})
