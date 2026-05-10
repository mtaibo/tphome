<script setup>

    import { computed } from 'vue'

    import { useDevices } from '../../config/devices'
    import { api } from '../../config/api'

    const store = useDevices()
    const lights = computed(() => store.lights)

    const toggleLight = async (id) => { await api.sendCommand(id, 'toggle') }

</script>

<template>

    <g
        v-for="(light, id) in lights" 
        :key="id"
        :transform="`translate(${light.map.x}, ${light.map.y})`"
        class="cursor-pointer select-none"
        @click="toggleLight(id)"
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