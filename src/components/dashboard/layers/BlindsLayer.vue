<script setup>
    
    import { ref } from 'vue'
    import { devices } from '../../../config/devices'
    const blinds = ref(devices.blinds)

</script>

<template>

    <g 
        v-for="(blind, id) in blinds" 
        :key="id" 
        class="select-none cursor-pointer" 
        @click="$emit('select', blind)"
    >
    
        <rect 
            :x="blind.x" :y="blind.y" 
            :width="blind.width" :height="blind.height" 
            rx="1.5"
            class="fill-black stroke-tp-border stroke-[1px]"
        />

        <rect 
            :x="blind.x" :y="blind.y" 
            :width="blind.width > blind.height ? (blind.state.position / 100) * blind.width : blind.width" 
            :height="blind.height > blind.width ? (blind.state.position / 100) * blind.height : blind.height" 
            rx="1"
            class="fill-muted transition-all duration-500 ease-in-out"
        />

        <rect 
            :x="blind.x" :y="blind.y" 
            :width="blind.width > blind.height ? (blind.state.position / 100) * blind.width : blind.width" 
            :height="blind.height > blind.width ? (blind.state.position / 100) * blind.height : blind.height" 
            :fill="blind.width > blind.height ? 'url(#pattern-v)' : 'url(#pattern-h)'"
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