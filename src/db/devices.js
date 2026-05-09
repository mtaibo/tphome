import { defineStore } from 'pinia'
import { reactive, computed } from 'vue'

import { api } from './api'

export const useDevices = defineStore('devices', () => {

    const storage = reactive({})
    const unconfigured = computed(() => Object.keys(storage).length === 0)

    /* Serve the blinds on the store with a filter for null state blinds (not available on API) */
    const blinds = computed(() => 
        Object.fromEntries(
            Object.entries(storage.blinds ?? {}).filter(([, d]) => d.state !== null)
        )
    )

    /* Serve the lights on the store with a filter for null state lights (not available on API) */
    const lights = computed(() => 
        Object.fromEntries(
            Object.entries(storage.lights ?? {}).filter(([, d]) => d.state !== null)
        )
    )

    async function setup() {

        try { // Show errors if something fails

            /* Get the devices config json, if there is no config file, return setup() function */
            const config = await api.getConfig('devices')
            if (Object.keys(config).length === 0) return

            for (const device of Object.keys(storage)) delete storage[device] // Clear current storage

            /* Loop that goes through each devices category: lights, blinds, switches */
            for (const [category, devices] of Object.entries(config)) {

                if (!storage[category]) storage[category] = {}

                /* For each device on each category, stablish a new key on storage */
                for (const [id, device] of Object.entries(devices)) {

                    storage[category][id] = {
                        name:  device.name,

                        map:   { ...device.map },
                        prefs: { ...device.prefs },

                        state:      null, // State will be filled on update()
                        connection: null, // Connection will be filled on update()
                    }
                }
            }

            await update() // Call to update function to fill state and connection on every available device
        
        } catch (error) { console.error('TPHome - Setup error:', error) }
    }

    /* Function to sync devices on storage with real devices and get its state from api */
    async function update() {

        try { // Show errors if something fails

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

    return { storage, unconfigured, blinds, setup, update }
})