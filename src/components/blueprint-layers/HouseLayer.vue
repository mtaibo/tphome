<script setup>

    import { useMap } from '../../config/map'
    const map = useMap()

</script>

<template>

    <!-- Rooms -->
    <g class="fill-tp-surface/30 stroke-tp-border stroke-2">
        <rect
            v-for="room in map.storage.rooms"
            :key="room.id"
            :x="room.x" :y="room.y"
            :width="room.w" :height="room.h"
        />
    </g>

    <!-- Names -->
    <g class="fill-muted font-mono text-[11px] uppercase tracking-widest pointer-events-none">
        <text
            v-for="(label, i) in map.storage.labels"
            :key="i"
            :x="label.x" :y="label.y"
            text-anchor="middle"
        >{{ label.text }}</text>
    </g>

    <!-- Doors -->
    <g class="stroke-tp-bg/90 stroke-4">
        <line
            v-for="(door, i) in map.storage.doors"
            :key="i"
            :x1="door.x1" :y1="door.y1"
            :x2="door.x2" :y2="door.y2"
        />
    </g>

</template>