import { defineStore } from 'pinia'
import { reactive, computed } from 'vue'

import { api } from './api'

// ── Estructura esperada del JSON importado ────────────────────────────────
const REQUIRED_CATEGORIES = ['lights', 'blinds', 'switches']
const REQUIRED_FIELDS = {
  lights:   ['id', 'name', 'map', 'prefs'],
  blinds:   ['id', 'name', 'map', 'prefs'],
  switches: ['id', 'name', 'map', 'prefs'],
}
const REQUIRED_PREFS = ['upTime', 'downTime', 'downPosition', 'invertedRelays']
const REQUIRED_MAP   = ['x', 'y']

export const devices = defineStore('devices', () => {

    const storage = reactive({}) // Variable where every active device on api is stored with all device properties.
    const unconfigured = computed(() => Object.keys(storage).length === 0) // Computed flag for empty devices storage.

    /*  */
    async function setup() {

        try { // Show errors if something fails

            const devicesConfig = await api.getConfig('devices')
            if (Object.keys(devicesConfig).length === 0) return // No devices config file
            for (const device of Object.keys(storage)) delete storage[device] // Clear current storage


            /* Loop that goes through each devices category: lights, blinds, switches */
            for (const [category, categoryDevices] of Object.entries(devicesConfig)) {

                /* For each device on each category, stablish a new key on storage */
                for (const device of Object.values(categoryDevices)) {

                    storage[device.id] = {
                        id:    device.id,
                        name:  device.name,
                        map:   { ...device.map },
                        prefs: { ...device.prefs },
                        state: null, // State will be taken from API with another GET on update()
                    }
                }
            }

            await update()

        
        } catch (err) { console.error('TPHome - Setup error:', err) }
    }

    /* Function to sync devices on storage with real devices and get its state from api */
    async function update() {

        try {

            const devicesState = await api.getState()

            await Promise.all(devicesState.map(async (device) => {

                const nameChanged = device.name !== storage[device.id].name;
                const prefsChanged = JSON.stringify(device.prefs) !== JSON.stringify(storage[device.id].prefs);

                if (nameChanged) await api.postName(device.id, storage[device.id].name);
                if (prefsChanged) await api.postPrefs(device.id, storage[device.id].prefs);
                
                storage[device.id].state = { ...device.state };
            }))

        } catch (err) { console.error('TPHome - Update Error:', err) }
    }

    /* Fast function to change only state */
    function patch(id, state) {

        if (!devices[id]) return
        devices[id].state = { ...state }
    }

  // ── importConfig(json) ────────────────────────────────────────────────────
  // Valida el JSON, lo manda a la API y relanza setup().
  async function importConfig(json) {
    const error = validateConfig(json)
    if (error) throw new Error(error)

    await api.postConfig(json)  // POST /config/devices
    await setup()
  }

  // ── validateConfig(json) ──────────────────────────────────────────────────
  // Devuelve un string de error si el JSON no es válido, null si es correcto.
  function validateConfig(json) {
    if (!json || typeof json !== 'object') return 'El JSON no es válido'

    for (const category of REQUIRED_CATEGORIES) {
      if (!json[category] || typeof json[category] !== 'object') {
        return `Falta la categoría "${category}"`
      }

      for (const [id, device] of Object.entries(json[category])) {
        for (const field of REQUIRED_FIELDS[category]) {
          if (!(field in device)) return `Dispositivo "${id}": falta el campo "${field}"`
        }

        for (const coord of REQUIRED_MAP) {
          if (!(coord in device.map)) return `Dispositivo "${id}": falta map.${coord}`
        }

        if (category === 'blinds') {
          for (const pref of REQUIRED_PREFS) {
            if (!(pref in device.prefs)) return `Dispositivo "${id}": falta prefs.${pref}`
          }
        }
      }
    }

    return null
  }

  return { devices, unconfigured, setup, update, patch, importConfig }
})