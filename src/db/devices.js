// src/stores/devices.js
import { defineStore } from 'pinia'
import { reactive } from 'vue'
import template from '@/db/devices.json'

export const useDevices = defineStore('devices', () => {

  // ── Almacén central ──────────────────────────────────────────────────────
  // Un dict reactivo: { B0101: { ...datosMergeados }, L0101: { ... }, ... }
  const devices = reactive({})

  // ── update() ─────────────────────────────────────────────────────────────
  // Llama a la API, mezcla con el template y construye devices.
  // Si ya existe un dispositivo, solo actualiza lo que haya cambiado.
  async function update() {
    const res  = await fetch('/api/devices')
    const list = await res.json()   // array de la API

    for (const apiDevice of list) {
      const id   = apiDevice.id
      const tmpl = findInTemplate(id)

      if (devices[id]) {
        // Ya existe: actualiza solo datos de API, no pisamos coords del template
        Object.assign(devices[id], apiDevice)
      } else {
        // Nuevo: merge completo template + API
        devices[id] = { ...tmpl, ...apiDevice }
      }
    }
  }

  // ── patch(id, data) ───────────────────────────────────────────────────────
  // Actualización rápida desde WebSocket.
  // Ej: patch('B0101', { state: { position: 50 } })
  function patch(id, data) {
    if (!devices[id]) return
    Object.assign(devices[id], data)
  }

  // ── getMap() ──────────────────────────────────────────────────────────────
  // Devuelve { lights: { L0101: { x, y, state } }, blinds: { B0101: { x, y, width, height, state } } }
  // Las referencias son reactivas porque devices es reactive().
  function getMap() {
    const lights = {}
    const blinds = {}

    for (const [id, d] of Object.entries(devices)) {
      if (d.type === 'L') {
        lights[id] = { x: d.x, y: d.y, state: d.state }
      } else if (d.type === 'B') {
        blinds[id] = { x: d.x, y: d.y, width: d.width, height: d.height, state: d.state }
      }
    }

    return { lights, blinds }
  }

  // ── provision(id) ─────────────────────────────────────────────────────────
  // Stub: implementa aquí el envío de prefs al dispositivo.
  async function provision(id) {
    const device = devices[id]
    if (!device) return

    // TODO: enviar device.prefs al dispositivo vía API
    console.log(`[TPHome] Provisioning ${id}`, device.prefs)
  }

  // ── Helpers ───────────────────────────────────────────────────────────────
  function findInTemplate(id) {
    for (const category of Object.values(template)) {
      if (category[id]) return category[id]
    }
    return {}
  }

  return { devices, update, patch, getMap, provision }
})