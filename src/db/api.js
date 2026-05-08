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

    /* Function to get the devices or the map config json file */
    async getConfig(subject) {
        let path = `/config/${subject}`
        const response = await client.get(path)
        return response.data
    },

    /* Function to publish the devices or the map new config json file */
    async postConfig(subject, newConfig) {
        let path = `/config/${subject}`
        return client.post(path, newConfig)
    },

    /* Function to build commands requests */
    async sendCommand(id, command, value = null) {

        let path = `/commands/${id}/${command}`
        if (command === 'set' && value !== null) path = `/commands/${id}/set/${value}`

        return client.post(path)
    },
}