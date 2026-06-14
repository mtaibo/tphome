<script setup>

    import { computed } from 'vue'

    import { useDevices } from '@/config/devices'

    const props = defineProps({
        mode: { type: String, default: 'control' }
    })
    const emit = defineEmits(['select', 'pick'])

    const store = useDevices()

    const blinds = computed(() =>
        props.mode === 'config'
            ? (store.storage.blinds ?? {})
            : store.blinds
    )

    const isHorizontal = (blind) => blind.map.width > blind.map.height
    const coverWidth   = (blind) => {
        if (props.mode === 'config' || !blind.state) return blind.map.width
        return isHorizontal(blind) ? blind.map.width  * (100 - blind.state.position) / 100 : blind.map.width
    }
    const coverHeight  = (blind) => {
        if (props.mode === 'config' || !blind.state) return blind.map.height
        return isHorizontal(blind) ? blind.map.height : blind.map.height * (100 - blind.state.position) / 100
    }

    const isActive = (blind) => blind.state && blind.state.position > 0

    const onClick = (id) => {
        if (props.mode === 'config') return emit('pick', id)
        emit('select', id)
    }

</script>

<template>

    <g 
        v-for="(blind, id) in blinds" 
        :key="id" 
        class="select-none cursor-pointer" 
        @click="onClick(id)"
    >
    
        <!-- Hit area (invisible, extends 4px beyond the blind for accessibility) -->
        <rect 
            :x="blind.map.x - 4" :y="blind.map.y - 4"
            :width="blind.map.width + 8" :height="blind.map.height + 8" 
            fill="transparent" rx="3"
        />

        <!-- Blind background -->
        <rect 
            :x="blind.map.x" :y="blind.map.y" rx="1.5"
            :width="blind.map.width" :height="blind.map.height" 
            class="fill-black"
            :class="isActive(blind) ? 'stroke-[#5a5aee]' : 'stroke-tp-border'"
        />

        <!-- Blind plain cover -->
        <rect 
            :x="blind.map.x" :y="blind.map.y" rx="1.5"
            :width="coverWidth(blind)" :height="coverHeight(blind)" 
            :class="props.mode === 'config'
                ? 'fill-tp-accent/20'
                : isActive(blind)
                    ? 'fill-[#5a5aee18] transition-all duration-500 ease-in-out'
                    : 'fill-muted transition-all duration-500 ease-in-out'"
        />

        <!-- Apply pattern -->
        <rect 
            v-if="props.mode !== 'config'"
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
