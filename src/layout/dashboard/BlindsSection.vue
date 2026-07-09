<script setup>
    import { ref, watch, nextTick, onMounted, onUnmounted } from 'vue'
    import { ChevronUp, ChevronDown, Pause, Settings, Blinds } from 'lucide-vue-next'
    import { useDevices } from '@/config/devices'
    import { api } from '@/config/api'
    import { useRouter } from 'vue-router'

    const store   = useDevices()
    const router  = useRouter()

    const positions = ref({})
    const loading   = ref({})
    const dragging  = ref({})
    const pressing  = ref({})
    const dragState = ref({})

    // Per-blind animation state (outside Vue reactivity for perf)
    const anim = {}
    let rafId         = null
    let lastFrameTime = Date.now()

    function getAnim(id, initialPos) {
        if (!anim[id]) {
            positions.value[id] = initialPos ?? 0
            anim[id] = { realPos: initialPos ?? 0, realTime: Date.now(), velocity: 0, lastKnownSpeed: 0.007, displayPos: initialPos ?? 0 }
        }
        return anim[id]
    }

    // Derive velocity from WS position updates, don't snap positions directly
    watch(() => store.blinds, (blinds) => {
        for (const [id, device] of Object.entries(blinds)) {
            if (dragging.value[id]) continue
            const newPos = device.state?.position ?? 0
            const a = getAnim(id, newPos)
            const now = Date.now()
            const dt  = now - a.realTime
            if (dt > 50) {
                a.velocity = (newPos - a.realPos) / dt
                if (Math.abs(a.velocity) > 0.001) a.lastKnownSpeed = Math.abs(a.velocity)
            }
            a.realPos  = newPos
            a.realTime = now
        }
    }, { immediate: true, deep: true })

    function animateLoop() {
        const now = Date.now()
        const dt  = Math.min(now - lastFrameTime, 50)
        lastFrameTime = now

        for (const [id, a] of Object.entries(anim)) {
            if (dragging.value[id]) continue
            const corrRate = Math.abs(a.velocity) > 0.002 ? 0.002 : 0.006
            a.displayPos += a.velocity * dt + (a.realPos - a.displayPos) * corrRate * dt
            a.displayPos  = Math.max(0, Math.min(100, a.displayPos))
            positions.value[id] = a.displayPos  // float for smooth visual
        }
        rafId = requestAnimationFrame(animateLoop)
    }

    onMounted(()   => { rafId = requestAnimationFrame(animateLoop) })
    onUnmounted(() => { if (rafId) cancelAnimationFrame(rafId) })

    const sendCommand = async (id, cmd, val = null) => {
        loading.value[id] = true
        try { await api.sendCommand(id, cmd, val) }
        catch (e) { console.error('TPHome - BlindsSection:', e) }
        finally { loading.value[id] = false }
    }

    const pressBtn = (key, action) => {
        pressing.value[key] = false
        nextTick(() => {
            pressing.value[key] = true
            setTimeout(() => { pressing.value[key] = false }, 440)
        })
        action()
    }

    const handleUp = (id) => pressBtn(`${id}-up`, () => {
        const a = getAnim(id, positions.value[id])
        a.displayPos = positions.value[id] ?? 0; a.realPos = a.displayPos; a.realTime = Date.now(); a.velocity = a.lastKnownSpeed
        sendCommand(id, 'up')
    })
    const handleDown = (id) => pressBtn(`${id}-down`, () => {
        const a = getAnim(id, positions.value[id])
        a.displayPos = positions.value[id] ?? 0; a.realPos = a.displayPos; a.realTime = Date.now(); a.velocity = -a.lastKnownSpeed
        sendCommand(id, 'down')
    })
    const handleStop = (id) => pressBtn(`${id}-stop`, () => {
        if (anim[id]) { anim[id].velocity = 0; anim[id].displayPos = anim[id].realPos; positions.value[id] = anim[id].realPos }
        sendCommand(id, 'stop')
    })
    const handleSettings = (id) => pressBtn(`${id}-cfg`,  () => router.push({ path: '/settings', query: { device: id } }))

    // Vertical track drag
    function onTrackPointerDown(e, id) {
        e.currentTarget.setPointerCapture(e.pointerId)
        const rect = e.currentTarget.getBoundingClientRect()
        dragState.value[id] = { active: true, startY: e.clientY, startPos: positions.value[id] ?? 0, height: rect.height }
        dragging.value[id] = true
    }

    function onTrackPointerMove(e, id) {
        const s = dragState.value[id]
        if (!s?.active) return
        const dy    = e.clientY - s.startY
        const delta = -(dy / s.height) * 100
        positions.value[id] = Math.round(Math.max(0, Math.min(100, s.startPos + delta)))
    }

    function onTrackPointerUp(e, id) {
        const s = dragState.value[id]
        if (!s?.active) return
        dragState.value[id] = { active: false }
        dragging.value[id] = false
        const pos = positions.value[id]
        sendCommand(id, 'set', pos)
        const a = getAnim(id, pos)
        a.displayPos = pos; a.realPos = pos; a.realTime = Date.now(); a.velocity = 0
    }

    const TRACK_H  = 180
    const HANDLE_H = 20

    const handleTop = (id) => {
        const pos = positions.value[id] ?? 0
        const raw = (1 - pos / 100) * TRACK_H - HANDLE_H / 2
        return `${Math.max(0, Math.min(TRACK_H - HANDLE_H, raw))}px`
    }
</script>

<template>
    <div class="h-full overflow-y-auto overflow-x-hidden pt-28 pb-32 px-5 md:pt-8 md:pb-8 md:px-8">

        <!-- Empty state -->
        <div v-if="Object.keys(store.blinds).length === 0"
             class="flex flex-col items-center justify-center h-full gap-4 text-muted">
            <Blinds class="w-12 h-12 opacity-20" />
            <p class="text-sm tracking-wide">No hay persianas disponibles</p>
        </div>

        <!-- Cards grid -->
        <div v-else class="flex flex-wrap justify-start md:justify-center gap-4">
            <div
                v-for="(device, id) in store.blinds"
                :key="id"
                class="blind-card transition-opacity duration-300 select-none w-[calc(50%-8px)] md:w-48 shrink-0"
                :class="{ 'opacity-50 pointer-events-none': loading[id] }"
            >
                <!-- Header -->
                <div class="flex items-start justify-between mb-4 gap-2">
                    <div class="flex items-start gap-2 flex-1 min-w-0">
                        <div class="w-2 h-2 rounded-full shrink-0 mt-[3px] transition-all duration-300"
                             :class="device.connection?.online
                                 ? 'bg-tp-ok shadow-[0_0_6px_var(--color-tp-ok)]'
                                 : 'bg-tp-danger'">
                        </div>
                        <h3 class="text-sm font-semibold text-tp-text-primary leading-tight">{{ device.name }}</h3>
                    </div>
                    <div class="flex items-baseline gap-0.5 shrink-0">
                        <span class="text-sm font-mono font-bold text-tp-text-primary tabular-nums leading-none">{{ Math.round(positions[id] ?? 0) }}</span>
                        <span class="text-[9px] font-bold text-tp-accent leading-none mb-0.5">%</span>
                    </div>
                </div>

                <!-- Control area: track left, buttons right -->
                <div class="flex gap-2 items-start">

                    <!-- Vertical track -->
                    <div class="blind-track flex-1"
                         @pointerdown="onTrackPointerDown($event, id)"
                         @pointermove="onTrackPointerMove($event, id)"
                         @pointerup="onTrackPointerUp($event, id)"
                         @pointercancel="onTrackPointerUp($event, id)">

                        <!-- Blind slats fill from top -->
                        <div class="absolute top-0 left-0 right-0 overflow-hidden"
                             :class="(positions[id] ?? 0) < 100 ? 'border-b border-tp-accent/35' : ''"
                             :style="{ height: (100 - (positions[id] ?? 0)) + '%' }">
                            <div class="flex flex-col gap-[3px] px-[4px] pt-[4px]">
                                <div v-for="i in 24" :key="i"
                                     class="w-full bg-white/14 rounded-[2px] shrink-0"
                                     style="height: 4px; min-height: 4px;"></div>
                            </div>
                        </div>

                        <!-- Drag handle -->
                        <div class="blind-track-handle"
                             :class="dragging[id] ? 'transition-none' : ''"
                             :style="{ top: handleTop(id) }">
                        </div>
                    </div>

                    <!-- Buttons column -->
                    <div class="flex flex-col justify-between items-center h-[180px]">
                        <button @click="handleUp(id)"
                                class="blind-btn"
                                :class="{ pressing: pressing[`${id}-up`] }">
                            <ChevronUp class="w-[18px] h-[18px] text-tp-text-primary/80" />
                        </button>
                        <button @click="handleStop(id)"
                                class="blind-btn"
                                :class="{ pressing: pressing[`${id}-stop`] }">
                            <Pause class="w-[15px] h-[15px] fill-current text-tp-text-primary/80" />
                        </button>
                        <button @click="handleDown(id)"
                                class="blind-btn"
                                :class="{ pressing: pressing[`${id}-down`] }">
                            <ChevronDown class="w-[18px] h-[18px] text-tp-text-primary/80" />
                        </button>
                        <button @click="handleSettings(id)"
                                class="blind-btn blind-btn-muted"
                                :class="{ pressing: pressing[`${id}-cfg`] }">
                            <Settings class="w-[15px] h-[15px] text-muted" />
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
