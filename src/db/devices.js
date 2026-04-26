import { reactive, readonly } from 'vue'
import { api } from './api'
import devicesConfig from './devices.json'

const devices = reactive([])

export const useDeviceStore = () => {

    /* Fill state var with api db devices */
    const updateDevices = async () => {
        try { devices = await api.getDevices()
        } catch (error) { console.error("Error en el store:", error) }
    }

    const getMapItems = () => {
        return state.devices.map(d => {
            const config = devicesConfig.lights[d.id] || devicesConfig.blinds[d.id] || {}
            return {
                id: d.id,
                x: config.x,
                y: config.y,
                online: d.online,
                type: d.type
            }
        })
    }

    const getControlCards = () => {
        return devices.map(d => ({
            id: d.id,
            name: d.name,
            state: d.state,
            online: d.online,
            type: d.type
        }))
    }

    return {
        devices: readonly(devices),
        updateDevices,
        getMapItems,
        getControlCards
    }
}