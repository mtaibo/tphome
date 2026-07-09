<script setup>

    import { computed } from 'vue'
    import { useMap } from '@/config/map'

    const map = useMap()

    const roomRx = computed(() => {
        const parts = (map.storage.viewBox ?? '0 0 100 100').split(' ').map(Number)
        return Math.round(Math.min(parts[2] || 100, parts[3] || 100) * 0.08)
    })

    // Interior walls: segments where both sides are inside rooms (shared between rooms)
    const interiorWallPath = computed(() => {
        const rooms = map.storage.rooms
        const xs = [...new Set(rooms.flatMap(r => [r.x, r.x + r.w]))].sort((a, b) => a - b)
        const ys = [...new Set(rooms.flatMap(r => [r.y, r.y + r.h]))].sort((a, b) => a - b)
        const inRoom = (x, y) => rooms.some(r => x >= r.x && x <= r.x + r.w && y >= r.y && y <= r.y + r.h)

        const segs = []
        for (const y of ys) {
            for (let i = 0; i < xs.length - 1; i++) {
                const xm = (xs[i] + xs[i + 1]) / 2
                if (inRoom(xm, y - 0.5) && inRoom(xm, y + 0.5))
                    segs.push(`M${xs[i]},${y}L${xs[i + 1]},${y}`)
            }
        }
        for (const x of xs) {
            for (let j = 0; j < ys.length - 1; j++) {
                const ym = (ys[j] + ys[j + 1]) / 2
                if (inRoom(x - 0.5, ym) && inRoom(x + 0.5, ym))
                    segs.push(`M${x},${ys[j]}L${x},${ys[j + 1]}`)
            }
        }
        return segs.join('')
    })

    // Exterior outline: connected polygon traced from boundary segments, with rounded corners
    const exteriorOutlinePath = computed(() => {
        const rooms = map.storage.rooms
        const xs = [...new Set(rooms.flatMap(r => [r.x, r.x + r.w]))].sort((a, b) => a - b)
        const ys = [...new Set(rooms.flatMap(r => [r.y, r.y + r.h]))].sort((a, b) => a - b)
        const inRoom = (x, y) => rooms.some(r => x >= r.x && x <= r.x + r.w && y >= r.y && y <= r.y + r.h)

        // Boundary segments: exactly one side is inside a room
        const segs = []
        for (const y of ys) {
            for (let i = 0; i < xs.length - 1; i++) {
                const xm = (xs[i] + xs[i + 1]) / 2
                if (inRoom(xm, y - 0.5) !== inRoom(xm, y + 0.5))
                    segs.push({ x1: xs[i], y1: y, x2: xs[i + 1], y2: y })
            }
        }
        for (const x of xs) {
            for (let j = 0; j < ys.length - 1; j++) {
                const ym = (ys[j] + ys[j + 1]) / 2
                if (inRoom(x - 0.5, ym) !== inRoom(x + 0.5, ym))
                    segs.push({ x1: x, y1: ys[j], x2: x, y2: ys[j + 1] })
            }
        }

        if (!segs.length) return ''

        // Build adjacency graph from segment endpoints
        const adj = new Map()
        const k = (x, y) => `${x},${y}`
        for (const seg of segs) {
            const k1 = k(seg.x1, seg.y1), k2 = k(seg.x2, seg.y2)
            if (!adj.has(k1)) adj.set(k1, { x: seg.x1, y: seg.y1, nb: [] })
            if (!adj.has(k2)) adj.set(k2, { x: seg.x2, y: seg.y2, nb: [] })
            adj.get(k1).nb.push(k2)
            adj.get(k2).nb.push(k1)
        }

        // Start from topmost-leftmost vertex (guaranteed to be on exterior)
        const startKey = [...adj.keys()].reduce((a, b) => {
            const na = adj.get(a), nb = adj.get(b)
            return nb.y < na.y || (nb.y === na.y && nb.x < na.x) ? b : a
        })

        // Trace closed polygon by following neighbors (avoid backtracking)
        const raw = []
        let cur = startKey, prev = null
        do {
            const node = adj.get(cur)
            raw.push({ x: node.x, y: node.y })
            const next = node.nb.find(n => n !== prev) ?? node.nb[0]
            prev = cur
            cur = next
        } while (cur !== startKey && raw.length <= segs.length)

        // Drop collinear vertices (cross product = 0)
        const n = raw.length
        const poly = raw.filter((c, i) => {
            const p = raw[(i - 1 + n) % n], nx = raw[(i + 1) % n]
            return (c.x - p.x) * (nx.y - p.y) - (c.y - p.y) * (nx.x - p.x) !== 0
        })

        if (poly.length < 3) return ''

        // Build rounded-corner path using quadratic bezier arcs at each corner
        const r = 12
        const m = poly.length
        let d = ''

        for (let i = 0; i < m; i++) {
            const pv = poly[(i - 1 + m) % m]
            const cv = poly[i]
            const nx = poly[(i + 1) % m]

            const dx1 = cv.x - pv.x, dy1 = cv.y - pv.y
            const len1 = Math.hypot(dx1, dy1)
            const dx2 = nx.x - cv.x, dy2 = nx.y - cv.y
            const len2 = Math.hypot(dx2, dy2)

            const cr = Math.min(r, len1 / 2, len2 / 2)
            const p1x = cv.x - (dx1 / len1) * cr, p1y = cv.y - (dy1 / len1) * cr
            const p2x = cv.x + (dx2 / len2) * cr, p2y = cv.y + (dy2 / len2) * cr

            d += i === 0 ? `M${p1x},${p1y}` : `L${p1x},${p1y}`
            d += `Q${cv.x},${cv.y} ${p2x},${p2y}`
        }

        return d + 'Z'
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
    <g>
        <rect
            v-for="room in map.storage.rooms"
            :key="room.id"
            :x="room.x" :y="room.y"
            :width="room.w" :height="room.h"
            :rx="roomRx" :ry="roomRx"
            fill="none"
        />
    </g>

    <!-- Interior walls (straight, between rooms) -->
    <path
        :d="interiorWallPath"
        fill="none"
        class="stroke-2"
        style="stroke: rgba(255,255,255,0.80);"
        stroke-linecap="round"
        mask="url(#door-mask)"
    />

    <!-- Exterior outline with rounded corners -->
    <path
        :d="exteriorOutlinePath"
        fill="none"
        class="stroke-2"
        style="stroke: rgba(255,255,255,0.80);"
        stroke-linecap="round"
        mask="url(#door-mask)"
    />

    <!-- Room labels -->
    <g font-family="-apple-system, BlinkMacSystemFont, 'SF Pro Text', 'SF Pro Display', sans-serif"
       font-size="11"
       font-weight="500"
       fill="rgba(255,255,255,0.68)"
       letter-spacing="1.4"
       class="uppercase pointer-events-none">
        <text
            v-for="(label, i) in map.storage.labels"
            :key="i"
            :x="label.x" :y="label.y"
            text-anchor="middle"
        >{{ label.text }}</text>
    </g>

</template>
