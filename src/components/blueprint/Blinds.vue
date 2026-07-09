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
            fill="black"
            stroke="rgba(255,255,255,0.55)"
            stroke-width="0.5"
        />

        <!-- Config mode: flat accent fill -->
        <rect
            v-if="props.mode === 'config'"
            :x="blind.map.x" :y="blind.map.y" rx="1.5"
            :width="blind.map.width" :height="blind.map.height"
            class="fill-tp-accent/20"
        />

        <!-- Control mode: white slat fill sized by position -->
        <rect
            v-else
            :x="blind.map.x" :y="blind.map.y" rx="1.5"
            :width="coverWidth(blind)" :height="coverHeight(blind)"
            :fill="isHorizontal(blind) ? 'url(#blind-slat-h)' : 'url(#blind-slat-v)'"
            class="transition-all duration-500 ease-in-out"
        />

    </g>

    <defs>

        <!--
            Horizontal blind (wide × thin, fills left→right):
            Vertical slat stripes — each stripe = one slat seen from above.
            Body: white. Left edge: highlight. Right edge: shadow.
        -->
        <pattern id="blind-slat-h" x="0" y="0" width="5" height="7" patternUnits="userSpaceOnUse">
            <rect width="5" height="7" fill="rgba(255,255,255,0.84)"/>
            <rect x="0"   width="0.6" height="7" fill="rgba(255,255,255,1)"/>
            <rect x="4.2" width="0.8" height="7" fill="rgba(0,0,0,0.18)"/>
        </pattern>

        <!--
            Vertical blind (narrow × tall, fills top→bottom):
            Horizontal slat stripes — each stripe = one slat seen from the side.
            Body: white. Top edge: highlight. Bottom edge: shadow.
        -->
        <pattern id="blind-slat-v" x="0" y="0" width="7" height="4" patternUnits="userSpaceOnUse">
            <rect width="7" height="4"   fill="rgba(255,255,255,0.84)"/>
            <rect width="7" height="0.6" fill="rgba(255,255,255,1)"/>
            <rect y="3.4"  width="7" height="0.6" fill="rgba(0,0,0,0.18)"/>
        </pattern>

    </defs>

</template>
