<script setup>

    import { computed } from 'vue'

    import { useDevices } from '../../db/devices'

    const store = useDevices()
    const blinds = computed(() => store.blinds)

    const isHorizontal = (blind) => blind.map.width > blind.map.height
    const coverWidth = (blind) => {
    console.log(blind.map, blind.state)
    if (!blind.state) return 0
    return isHorizontal(blind) ? blind.map.width * (100 - blind.state.position) / 100 : blind.map.width
}
    const coverHeight = (blind) => !blind.state ? 0 : isHorizontal(blind) ? blind.map.height : blind.map.height * (100 - blind.state.position) / 100

</script>

<template>

    <g 
        v-for="(blind, id) in blinds" 
        :key="id" 
        class="select-none cursor-pointer" 
        @click="$emit('select', id)"
    >
    
        <!-- Blind background -->
        <rect 
            :x="blind.map.x" :y="blind.map.y" rx="1.5"
            :width="blind.map.width" :height="blind.map.height" 
            class="fill-black stroke-tp-border"
        />

        <!-- Blind plain cover -->
        <rect 
            :x="blind.map.x" :y="blind.map.y" rx="1.5"
            :width="coverWidth(blind)" :height="coverHeight(blind)" 
            class="fill-muted transition-all duration-500 ease-in-out"
        />

        <!-- Apply pattern -->
        <rect 
            :x="blind.map.x" :y="blind.map.y" 
            :width="coverWidth(blind)" :height="coverHeight(blind)" 
            :fill="isHorizontal(blind) ? 'url(#pattern-v)' : 'url(#pattern-h)'"
            class="pointer-events-none transition-all duration-500 ease-in-out"
        />

    </g>

    <!-- Patterns -->
    <defs>
        <pattern id="pattern-h" x="0" y="0" width="100%" height="4" patternUnits="userSpaceOnUse">
            <line x1="0" y1="0" x2="100%" y2="0" class="stroke-black/30" stroke-width="1"/>
        </pattern>

        <pattern id="pattern-v" x="0" y="0" width="4" height="100%" patternUnits="userSpaceOnUse">
            <line x1="0" y1="0" x2="0" y2="100%" class="stroke-black/30" stroke-width="1"/>
        </pattern>
    </defs>

</template>