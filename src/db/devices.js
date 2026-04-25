import { reactive, readonly } from 'vue'
import { api } from './api'
import devices from './devices.json'

const state = reactive({
    devices: [], 
    blueprint: blueprint, 
    isLoading: false,
    error: null
})

export const useDeviceStore = () => {
    
    const fetchDevices = async () => {
        state.isLoading = true
        try {
            const onlineDevices = await DeviceHub.update()
            
            state.devices = onlineDevices.map(device => ({
                ...device,
                config: state.blueprint[device.id] || {} 
            }))
        } catch (err) {
            state.error = "Error al sincronizar dispositivos"
        } finally {
            state.isLoading = false
        }
    }


    const configureNewDevice = async (newId) => {
        const configToApply = state.blueprint[newId]
        
        if (!configToApply) {
            console.error("Este ID no existe en el plano maestro")
            return
        }

        try {
            state.isLoading = true
            await DeviceHub.exec(newId, 'configure', configToApply)
            
            await fetchDevices()
        } catch (err) {
            state.error = "No se pudo configurar el dispositivo"
        } finally {
            state.isLoading = false
        }
    }

    const updateDeviceLocalState = (deviceId, newState) => {
        const device = state.devices.find(d => d.id === deviceId)
        if (device) {
            Object.assign(device.state, newState)
        }
    }

    return {
        state: readonly(state),
        fetchDevices,
        configureNewDevice,
        updateDeviceLocalState
    }
}