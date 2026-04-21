<script setup>
    
    import { ref } from 'vue'
    import { devices } from '../../../config/devices'
    const lights = ref(devices.lights)

    const toggleDevice = (device) => {
        device.on = !device.on
    }

</script>

<template>

    <g
        v-for="(device, id) in lights" 
        :key="id"
        :transform="`translate(${device.x}, ${device.y})`"
        class="cursor-pointer select-none"
        @click="toggleDevice(device)"
    >

        <!-- Outline circle -->
        <circle 
            r="10" 
            :class="[
                'transition-all duration-300 stroke-2',
                device.on 
                ? 'fill-yellow-400/20 stroke-yellow-400' 
                : 'fill-tp-surface/50 stroke-tp-border/20'
            ]"
        />
                        
        <!-- Inline circle -->
        <circle r="3" :class="device.on ? 'fill-yellow-400' : 'fill-muted'" />
                        
    </g>

</template>