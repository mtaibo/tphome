<script setup>

    import { computed } from 'vue'
    import { useMap } from '@/config/map'

    const map = useMap()

    const wallPath = computed(() => {
        const rooms = map.storage.rooms

        const allWalls = []
        for (const room of rooms) {
            allWalls.push({ x1: room.x, y1: room.y, x2: room.x + room.w, y2: room.y })
            allWalls.push({ x1: room.x + room.w, y1: room.y, x2: room.x + room.w, y2: room.y + room.h })
            allWalls.push({ x1: room.x, y1: room.y + room.h, x2: room.x + room.w, y2: room.y + room.h })
            allWalls.push({ x1: room.x, y1: room.y, x2: room.x, y2: room.y + room.h })
        }

        const normalized = allWalls.map(w => ({
            x1: Math.min(w.x1, w.x2),
            y1: Math.min(w.y1, w.y2),
            x2: Math.max(w.x1, w.x2),
            y2: Math.max(w.y1, w.y2)
        }))

        const groups = {}
        for (const wall of normalized) {
            const key = wall.x1 === wall.x2 ? `v${wall.x1}` : `h${wall.y1}`
            if (!groups[key]) groups[key] = []
            groups[key].push(wall)
        }

        const merged = []
        for (const key in groups) {
            const walls = groups[key].sort((a, b) => a.x1 - b.x1 || a.y1 - b.y1)
            let current = { ...walls[0] }
            for (let i = 1; i < walls.length; i++) {
                const next = walls[i]
                const overlaps = key.startsWith('v')
                    ? next.y1 <= current.y2 + 1 && next.y2 >= current.y1 - 1
                    : next.x1 <= current.x2 + 1 && next.x2 >= current.x1 - 1

                if (overlaps) {
                    if (key.startsWith('v')) {
                        current.y1 = Math.min(current.y1, next.y1)
                        current.y2 = Math.max(current.y2, next.y2)
                    } else {
                        current.x1 = Math.min(current.x1, next.x1)
                        current.x2 = Math.max(current.x2, next.x2)
                    }
                } else {
                    merged.push(current)
                    current = { ...next }
                }
            }
            merged.push(current)
        }

        return merged.map(seg => `M${seg.x1},${seg.y1}L${seg.x2},${seg.y2}`).join('')
    })

</script>

<template>

    <defs>
        <mask id="door-mask">
            <rect :width="map.storage.viewBox.split(' ')[2]" :height="map.storage.viewBox.split(' ')[3]" fill="white"/>
            <line
                v-for="(door, i) in map.storage.doors"
                :key="i"
                :x1="door.x1" :y1="door.y1"
                :x2="door.x2" :y2="door.y2"
                stroke="black"
                stroke-width="8"
            />
        </mask>
    </defs>

    <!-- Rooms (fill only) -->
    <g class="fill-tp-surface/50">
        <rect
            v-for="room in map.storage.rooms"
            :key="room.id"
            :x="room.x" :y="room.y"
            :width="room.w" :height="room.h"
        />
    </g>

    <!-- Walls: single path with door mask, consistent stroke -->
    <path
        :d="wallPath"
        fill="none"
        class="stroke-2"
        style="stroke: #ffffff;"
        stroke-linejoin="round"
        stroke-linecap="butt"
        mask="url(#door-mask)"
    />

    <!-- Names -->
    <g class="fill-white font-mono text-[11px] uppercase tracking-widest pointer-events-none">
        <text
            v-for="(label, i) in map.storage.labels"
            :key="i"
            :x="label.x" :y="label.y"
            text-anchor="middle"
        >{{ label.text }}</text>
    </g>

</template>
