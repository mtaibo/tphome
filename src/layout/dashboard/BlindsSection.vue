<script setup>
    import { ref, watch, nextTick, onMounted, onUnmounted } from 'vue'
    import { ChevronUp, ChevronDown, Pause, Settings, Blinds } from 'lucide-vue-next'
    import { useDevices } from '@/config/devices'
    import { api } from '@/config/api'
    import { useRouter } from 'vue-router'
    import BlindSlider from '@/components/BlindSlider.vue'

    const store   = useDevices()
    const router  = useRouter()

    const positions       = ref({})   // fill position per blind (reactive, for template)
    const handlePositions = ref({})   // bubble position per blind (reactive, for template)
    const loading         = ref({})
    const dragging        = ref({})
    const pressing        = ref({})

    // Per-blind animation state (outside Vue reactivity for perf)
    const anim       = {}
    const setPending = {}
    let rafId = null

    function getAnim(id, initialPos) {
        if (!anim[id]) {
            positions.value[id]       = initialPos ?? 0
            handlePositions.value[id] = initialPos ?? 0
            anim[id] = {
                realPos:      initialPos ?? 0,
                velocity:     0,
                moveStartPos: initialPos ?? 0,
                moveStartTime: Date.now(),
                displayPos:   initialPos ?? 0,
                handlePos:    initialPos ?? 0,
            }
        }
        return anim[id]
    }

    // WS update: recalibrate anchor while button-moving; ignore while set-pending; snap on IDLE
    watch(() => store.blinds, (blinds) => {
        for (const [id, device] of Object.entries(blinds)) {
            if (dragging.value[id]) continue
            const newPos     = device.state?.position ?? 0
            const motorState = device.state?.motor_state ?? 0
            const a = getAnim(id, newPos)
            a.realPos = newPos
            if (motorState === 0) {
                setPending[id] = false
                a.velocity = 0; a.displayPos = newPos; a.handlePos = newPos
                a.moveStartPos = newPos; a.moveStartTime = Date.now()
                positions.value[id] = newPos; handlePositions.value[id] = newPos
            } else if (a.velocity !== 0) {
                a.moveStartPos = newPos; a.moveStartTime = Date.now()
            } else if (!setPending[id]) {
                a.displayPos = newPos; a.handlePos = newPos
                a.moveStartPos = newPos; a.moveStartTime = Date.now()
                positions.value[id] = newPos; handlePositions.value[id] = newPos
            }
        }
    }, { immediate: true, deep: true })

    function animateLoop() {
        const now = Date.now()
        for (const [id, a] of Object.entries(anim)) {
            if (dragging.value[id] || a.velocity === 0) continue
            a.displayPos = Math.max(0, Math.min(100, a.moveStartPos + a.velocity * (now - a.moveStartTime)))
            positions.value[id] = a.displayPos
            if (!setPending[id]) {
                a.handlePos = a.displayPos
                handlePositions.value[id] = a.displayPos
            }
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
        const device = store.blinds[id]
        const a = getAnim(id, positions.value[id])
        setPending[id] = false
        a.velocity = 100 / ((device?.prefs?.up_time ?? 3000) * 10)
        a.moveStartPos = a.displayPos; a.moveStartTime = Date.now()
        sendCommand(id, 'up')
    })
    const handleDown = (id) => pressBtn(`${id}-down`, () => {
        const device = store.blinds[id]
        const a = getAnim(id, positions.value[id])
        setPending[id] = false
        a.velocity = -(100 / ((device?.prefs?.down_time ?? 3000) * 10))
        a.moveStartPos = a.displayPos; a.moveStartTime = Date.now()
        sendCommand(id, 'down')
    })
    const handleStop = (id) => pressBtn(`${id}-stop`, () => {
        if (anim[id]) {
            const a = anim[id]
            a.velocity = 0; a.displayPos = a.realPos; a.handlePos = a.realPos
            a.moveStartPos = a.realPos
            positions.value[id] = a.realPos; handlePositions.value[id] = a.realPos
            setPending[id] = false
        }
        sendCommand(id, 'stop')
    })
    const handleSettings = (id) => pressBtn(`${id}-cfg`, () => router.push({ path: '/settings', query: { device: id } }))

    // Slider drag handlers (receive position values from BlindSlider component)
    function onBlindDragStart(id, pos) {
        dragging.value[id] = true
        const a = getAnim(id, pos)
        a.velocity = 0; setPending[id] = false
        a.displayPos = pos; a.handlePos = pos
        positions.value[id] = pos; handlePositions.value[id] = pos
    }

    function onBlindDragMove(id, pos) {
        const a = anim[id]
        if (!a) return
        a.displayPos = pos; a.handlePos = pos
        positions.value[id] = pos; handlePositions.value[id] = pos
    }

    function onBlindDragEnd(id, pos) {
        dragging.value[id] = false
        const a = anim[id]
        if (!a) return

        a.handlePos = pos
        handlePositions.value[id] = pos

        a.displayPos = a.realPos
        a.moveStartPos = a.realPos
        a.moveStartTime = Date.now()
        positions.value[id] = a.realPos

        const device = store.blinds[id]
        if (pos < a.realPos) {
            a.velocity = -(100 / ((device?.prefs?.down_time ?? 3000) * 10))
            setPending[id] = true
        } else if (pos > a.realPos) {
            a.velocity = 100 / ((device?.prefs?.up_time ?? 3000) * 10)
            setPending[id] = true
        } else {
            a.velocity = 0; setPending[id] = false
        }

        sendCommand(id, 'set', pos)
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
                        <span class="text-sm font-mono font-bold text-tp-text-primary tabular-nums leading-none">{{ Math.round(handlePositions[id] ?? 0) }}</span>
                        <span class="text-[9px] font-bold text-tp-accent leading-none mb-0.5">%</span>
                    </div>
                </div>

                <!-- Control area: slider left, buttons right -->
                <div class="flex gap-2 items-start">

                    <BlindSlider
                        class="flex-1 h-[180px]"
                        :fill-pos="positions[id] ?? 0"
                        :handle-pos="handlePositions[id] ?? 0"
                        @drag-start="onBlindDragStart(id, $event)"
                        @drag-move="onBlindDragMove(id, $event)"
                        @drag-end="onBlindDragEnd(id, $event)"
                    />

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
