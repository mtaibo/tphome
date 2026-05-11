<script setup>

    import { onMounted } from 'vue';

    import Dashboard from './views/Dashboard.vue'

    import { useDevices } from './config/devices'
    import { useMap } from './config/map'

    const devices = useDevices()
    const map = useMap()

    onMounted(async () => { 
        await devices.setup() 
        await map.setup()
    })

</script>

<template>

    <Dashboard />

</template>