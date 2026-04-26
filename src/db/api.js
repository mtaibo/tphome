import axios from 'axios'

const client = axios.create({
    baseURL: '/api',
    headers: {
        'Content-Type': 'application/json'
    }
})

export const api = {

    /* Function to get devices from api db */
    async getDevices() {
        const response = await client.get('/devices')
        return response.data
    },

    /* Function to build commands requests */
    async sendCommand(deviceId, command, value = null) {

        let path = `/commands/${deviceId}/${command}`
        if (command === 'set' && value !== null) path = `/commands/${deviceId}/set/${value}`

        return client.post(path)
    }
}