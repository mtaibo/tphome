import { defineStore } from 'pinia'
import { reactive, computed } from 'vue'

import { api } from './api'

// ── Estructura esperada del JSON importado ────────────────────────────────
const REQUIRED_CATEGORIES = ['lights', 'blinds', 'switches']
const REQUIRED_FIELDS = {
  lights:   ['id', 'name', 'map'],
  blinds:   ['id', 'name', 'map', 'prefs'],
  switches: ['id', 'name', 'map'],
}
const REQUIRED_PREFS = ['upTime', 'downTime', 'downPosition', 'invertedRelays']
const REQUIRED_MAP   = ['x', 'y']

export const useDevices = defineStore('devices', () => {

  // ── Estado ────────────────────────────────────────────────────────────────
  const devices = reactive({})

  const unconfigured = computed(() => Object.keys(devices).length === 0)

  // ── setup() ───────────────────────────────────────────────────────────────
  // Carga la config de /config/devices y construye el store.
  // Si la API no devuelve nada, devices queda vacío → unconfigured = true.
  // Si hay config válida, llama a update() para rellenar el state inicial.
  async function setup() {
    try {
      const config = await api.getConfig()  // GET /config/devices

      if (!config || Object.keys(config).length === 0) return

      // Vacia el store antes de reconstruir (útil en re-setup tras importar)
      for (const key of Object.keys(devices)) delete devices[key]

      for (const [category, categoryDevices] of Object.entries(config)) {
        for (const device of Object.values(categoryDevices)) {
          devices[device.id] = {
            id:    device.id,
            name:  device.name,
            map:   { ...device.map },
            prefs: device.prefs ? { ...device.prefs } : null,
            state: null,  // se rellena en update()
          }
        }
      }

      await update()

    } catch (err) {
      console.error('[TPHome] Error en setup():', err)
    }
  }

  // ── update() ──────────────────────────────────────────────────────────────
  // Pide el state actual de todos los dispositivos a la API.
  // Solo actualiza state y prefs, nunca toca name, map ni id.
  async function update() {
    try {
      const apiDevices = await api.getDevices()  // GET /api/devices

      for (const apiDevice of apiDevices) {
        if (!devices[apiDevice.id]) continue  // dispositivo no está en config, ignorar

        if (apiDevice.state !== undefined) devices[apiDevice.id].state = { ...apiDevice.state }
        if (apiDevice.prefs !== undefined) devices[apiDevice.id].prefs = { ...apiDevice.prefs }
      }

    } catch (err) {
      console.error('[TPHome] Error en update():', err)
    }
  }

  // ── patch(id, state) ──────────────────────────────────────────────────────
  // Actualización rápida desde WebSocket. Solo toca state.
  // Ej: patch('B0101', { position: 50, motorState: 'moving', online: true, lastSeen: '...' })
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