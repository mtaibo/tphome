import { ref } from 'vue'
import { useDevices } from './devices'

const WS_URL = `ws://${window.location.host}/api/ws`

let socket = null
export const apiOnline = ref(true)

function connect() {
    socket = new WebSocket(WS_URL)

    socket.onopen = () => {
        console.log('[WS] Connected')
        apiOnline.value = true
    }

    socket.onmessage = (event) => {
        const { event: type, data } = JSON.parse(event.data)
        const store = useDevices()
        handle(store, type, data)
    }

    socket.onclose = () => {
        console.log('[WS] Disconnected, reconnecting in 3s...')
        apiOnline.value = false
        setTimeout(connect, 3000)
    }

    socket.onerror = (error) => console.error('[WS] Error:', error)
}

function handle(store, type, data) {
    switch (type) {

        case 'device_state': {
            const category = Object.keys(store.storage).find(cat => data.id in store.storage[cat])
            if (!category) return
            store.storage[category][data.id].state = {
                position:    data.state.position,
                motor_state: data.state.motor_state
            }
            break
        }

        case 'device_online':
        case 'device_offline': {
            const online = type === 'device_online'
            const category = Object.keys(store.storage).find(cat => data.id in store.storage[cat])
            if (!category) return
            store.storage[category][data.id].connection.online = online
            break
        }

        case 'device_info': {
            const category = Object.keys(store.storage).find(cat => data.id in store.storage[cat])
            if (!category) return
            store.storage[category][data.id].prefs = { ...data.prefs }
            break
        }
    }
}

export const socket_manager = { connect }