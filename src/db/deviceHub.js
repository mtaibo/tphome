import api from './api'

export const DeviceHub = {

    /* Function to update devices state */
    async update() {

        const response = await api.get('/devices')
        return response.data
    },

    /* Function to build commands requests */
    async sendCommand(deviceId, command, value = null) {

        let path = `/commands/${deviceId}/${command}`
        if (command === 'set' && value !== null) path = `/commands/${deviceId}/set/${value}`

        return api.post(path)
    }
}