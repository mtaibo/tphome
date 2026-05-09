<script setup>
    
    import { computed } from 'vue'
    import { useDevices } from '../db/devices'

    /* Get stored devices and filter them by its state. Null state indicates device not available on API */
    const store = useDevices()
    const lights = computed(() =>
        Object.fromEntries(
            Object.entries(store.lights ?? {}).filter(([, d]) => d.state !== null)
        )
    )

    const toggleLight = (light) => { light.state.on = !light.state.on }

</script>

<template>

    <g
        v-for="(light, id) in lights" 
        :key="id"
        :transform="`translate(${light.map.x}, ${light.map.y})`"
        class="cursor-pointer select-none"
        @click="toggleDevice(light)"
    >

        <!-- Outline circle -->
        <circle 
            r="10" 
            :class="[
                'transition-all duration-300 stroke-2',
                light.state.on 
                ? 'fill-yellow-400/20 stroke-yellow-400/50' 
                : 'fill-tp-surface/50 stroke-tp-border/20'
            ]"
        />
                        
        <!-- Inline circle -->
        <circle r="3" :class="light.state.on ? 'fill-yellow-400' : 'fill-muted'" />
                        
    </g>

</template>