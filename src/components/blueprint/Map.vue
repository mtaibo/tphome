<script setup>

    import { computed } from 'vue'
    import { useMap } from '@/config/map'

    const map = useMap()

    const wallSegments = computed(() => {
        const rooms = map.storage.rooms
        const doors = map.storage.doors

        // Collect all wall segments from all rooms
        const allWalls = []
        for (const room of rooms) {
            allWalls.push({ x1: room.x, y1: room.y, x2: room.x + room.w, y2: room.y })
            allWalls.push({ x1: room.x + room.w, y1: room.y, x2: room.x + room.w, y2: room.y + room.h })
            allWalls.push({ x1: room.x, y1: room.y + room.h, x2: room.x + room.w, y2: room.y + room.h })
            allWalls.push({ x1: room.x, y1: room.y, x2: room.x, y2: room.y + room.h })
        }

        // Normalize segments (ensure x1<=x2, y1<=y2)
        const normalized = allWalls.map(w => ({
            x1: Math.min(w.x1, w.x2),
            y1: Math.min(w.y1, w.y2),
            x2: Math.max(w.x1, w.x2),
            y2: Math.max(w.y1, w.y2)
        }))

        // Group by line (same x for vertical, same y for horizontal)
        const groups = {}
        for (const wall of normalized) {
            const key = wall.x1 === wall.x2 ? `v${wall.x1}` : `h${wall.y1}`
            if (!groups[key]) groups[key] = []
            groups[key].push(wall)
        }

        // Merge overlapping/adjacent segments within each group
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

        // Normalize doors for comparison
        const normDoors = doors.map(d => ({
            x1: Math.min(d.x1, d.x2),
            y1: Math.min(d.y1, d.y2),
            x2: Math.max(d.x1, d.x2),
            y2: Math.max(d.y1, d.y2)
        }))

        // Subtract door segments from walls
        const result = []
        for (const wall of merged) {
            const isVertical = wall.x1 === wall.x2
            const overlappingDoors = normDoors.filter(door => {
                const doorIsVertical = door.x1 === door.x2
                if (isVertical !== doorIsVertical) return false
                if (isVertical) {
                    return door.x1 === wall.x1 && door.y1 < wall.y2 && door.y2 > wall.y1
                } else {
                    return door.y1 === wall.y1 && door.x1 < wall.x2 && door.x2 > wall.x1
                }
            })

            if (overlappingDoors.length === 0) {
                result.push(wall)
                continue
            }

            // Split wall at door boundaries
            let segments = [{ ...wall }]
            for (const door of overlappingDoors) {
                const newSegments = []
                for (const seg of segments) {
                    if (isVertical) {
                        if (door.y1 > seg.y1 + 0.5) {
                            newSegments.push({ x1: seg.x1, y1: seg.y1, x2: seg.x2, y2: door.y1 })
                        }
                        if (door.y2 < seg.y2 - 0.5) {
                            newSegments.push({ x1: seg.x1, y1: door.y2, x2: seg.x2, y2: seg.y2 })
                        }
                    } else {
                        if (door.x1 > seg.x1 + 0.5) {
                            newSegments.push({ x1: seg.x1, y1: seg.y1, x2: door.x1, y2: seg.y2 })
                        }
                        if (door.x2 < seg.x2 - 0.5) {
                            newSegments.push({ x1: door.x2, y1: seg.y1, x2: seg.x2, y2: seg.y2 })
                        }
                    }
                }
                segments = newSegments
            }
            result.push(...segments)
        }

        return result
    })

</script>

<template>

    <!-- Rooms (fill only, no stroke) -->
    <g class="fill-tp-surface/50">
        <rect
            v-for="room in map.storage.rooms"
            :key="room.id"
            :x="room.x" :y="room.y"
            :width="room.w" :height="room.h"
        />
    </g>

    <!-- Walls (lines with gaps for doors, merged for shared walls) -->
    <g class="stroke-tp-border stroke-2">
        <line
            v-for="(seg, i) in wallSegments"
            :key="i"
            :x1="seg.x1" :y1="seg.y1"
            :x2="seg.x2" :y2="seg.y2"
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

</template>
