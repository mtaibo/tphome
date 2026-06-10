<script setup>

    import { computed } from 'vue'

    import { useDevices } from '@/config/devices'
    import { api } from '@/config/api'

    const props = defineProps({
        mode: { type: String, default: 'control' }
    })
    const emit = defineEmits(['pick'])

    const store = useDevices()

    const lights = computed(() =>
        props.mode === 'config'
            ? (store.storage.lights ?? {})
            : store.lights
    )

    const toggleLight = async (id) => {
        if (props.mode === 'config') return emit('pick', id)
        await api.sendCommand(id, 'toggle')
    }

    const circleClass = (light) => {
        if (props.mode === 'config') return 'fill-tp-surface/50 stroke-tp-accent/50'
        return light.state.on
            ? 'fill-tp-light-on/20 stroke-tp-light-on/50'
            : 'fill-tp-surface/50 stroke-tp-border/20'
    }

    const dotClass = (light) => {
        if (props.mode === 'config') return 'fill-tp-accent'
        return light.state.on ? 'fill-tp-light-on' : 'fill-muted'
    }

</script>

<template>

    <g
        v-for="(light, id) in lights" 
        :key="id"
        :transform="`translate(${light.map.x}, ${light.map.y})`"
        class="cursor-pointer select-none"
        @click="toggleLight(id)"
    >

        <!-- Hit area (invisible, larger for accessibility) -->
        <circle r="14" fill="transparent" />

        <!-- Outline circle -->
        <circle 
            r="10" 
            :class="['transition-all duration-300 stroke-2', circleClass(light)]"
        />

        <!-- Inline circle -->
        <circle r="3" :class="dotClass(light)" />

    </g>

</template>