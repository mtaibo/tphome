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

    /* Function to get pending devices from api db */
    async getPending() {
        const response = await client.get('/devices/pending')
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

    async sendPrefs(id, prefs) {
        let path = `/admin/${id}/prefs`
        return client.post(path, prefs)
    },

    async getDeviceInfo(id) {
        return client.post(`/admin/${id}/info`)
    },

    async configurePending(mac, id, prefs) {
        return client.post('/devices/pending/configure', { mac, id, prefs })
    },

    async deleteDevice(id) {
        return client.delete(`/devices/${id}`)
    },

    async triggerUpdate() {
        return client.post('/update')
    },

    async uploadFirmware(file, metadata) {
        const formData = new FormData()
        formData.append('file', file)
        formData.append('name', metadata.name)
        formData.append('chip', metadata.chip)
        formData.append('target', metadata.target)
        formData.append('version', metadata.version)
        formData.append('notes', metadata.notes || '')

        const response = await client.post('/firmware/upload', formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
        })
        return response.data
    },

    async getFirmwares() {
        const response = await client.get('/firmware')
        return response.data
    },

    async activateFirmware(id) {
        return client.post(`/firmware/${id}/activate`)
    },

    async deleteFirmware(id) {
        return client.delete(`/firmware/${id}`)
    }
}
