<script setup>
    import { ref, watch, nextTick, onMounted, onUnmounted } from 'vue'
    import { X, ChevronUp, ChevronDown, Pause, Blinds, Check } from 'lucide-vue-next'
    import { api } from '@/config/api'
    import BlindSlider from '@/components/BlindSlider.vue'

    const props = defineProps({
        id:     { type: String, required: true },
        device: { type: Object, required: true }
    })
    const emit = defineEmits(['close'])

    const tempPosition = ref(Math.round(props.device.state.position))  // integer, for text/input
    const smoothPos    = ref(props.device.state.position)              // float, fill position
    const handlePos    = ref(props.device.state.position)              // float, bubble position
    const isLoading    = ref(false)
    const pressing     = ref({})

    // Animation: constant speed from prefs, anchored to (moveStartPos, moveStartTime)
    // Each WS update recalibrates the anchor so prediction stays in sync without jerks
    let velocity      = 0
    let moveStartPos  = props.device.state.position
    let moveStartTime = Date.now()
    let realPos       = props.device.state.position
    let displayPos    = props.device.state.position
    let setPending    = false  // true while motor moves toward a slider-set target
    let rafId         = null

    const snapToReal = () => {
        velocity           = 0
        setPending         = false
        displayPos         = realPos
        moveStartPos       = realPos
        moveStartTime      = Date.now()
        smoothPos.value    = realPos
        handlePos.value    = realPos
        tempPosition.value = Math.round(realPos)
    }

    // WS position update: recalibrate anchor while button-moving; ignore while set-pending
    watch(() => props.device.state.position, (newPos) => {
        realPos = newPos
        if (velocity !== 0) {
            moveStartPos = newPos; moveStartTime = Date.now()
        } else if (!setPending) {
            displayPos = newPos; smoothPos.value = newPos; handlePos.value = newPos; tempPosition.value = Math.round(newPos)
        }
    })

    // Snap only when motor reaches IDLE (0) — clears setPending and confirms final position
    watch(() => props.device.state.motor_state, (newState) => {
        if (newState === 0) { realPos = props.device.state.position; snapToReal() }
    })

    function animate() {
        if (!dragging && velocity !== 0) {
            const now = Date.now()
            displayPos      = Math.max(0, Math.min(100, moveStartPos + velocity * (now - moveStartTime)))
            smoothPos.value = displayPos
            if (!setPending) {
                handlePos.value    = displayPos
                tempPosition.value = Math.round(displayPos)
            }
        }
        rafId = requestAnimationFrame(animate)
    }

    onMounted(()   => { rafId = requestAnimationFrame(animate) })
    onUnmounted(() => { if (rafId) cancelAnimationFrame(rafId) })

    const pressBtn = (key, action) => {
        pressing.value[key] = false
        nextTick(() => {
            pressing.value[key] = true
            setTimeout(() => { pressing.value[key] = false }, 440)
        })
        action()
    }

    const sendCommand = async (command, value = null) => {
        isLoading.value = true
        try {
            await api.sendCommand(props.id, command, value)
        } catch (error) {
            console.error('TPHome - BlindsControl error:', error)
        } finally {
            isLoading.value = false
        }
    }

    const updatePosition = (val) => {
        let value = Math.max(0, Math.min(100, parseInt(val) || 0))
        tempPosition.value = value
        sendCommand('set', value)
    }

    const handleUp = () => pressBtn('up', () => {
        setPending = false
        velocity = 100 / ((props.device.prefs?.up_time ?? 3000) * 10)
        moveStartPos = displayPos; moveStartTime = Date.now()
        sendCommand('up')
    })
    const handleDown = () => pressBtn('down', () => {
        setPending = false
        velocity = -(100 / ((props.device.prefs?.down_time ?? 3000) * 10))
        moveStartPos = displayPos; moveStartTime = Date.now()
        sendCommand('down')
    })
    const handleStop = () => pressBtn('stop', () => { snapToReal(); sendCommand('stop') })

    let dragging = false

    function onSliderDragStart(pos) {
        dragging = true
        velocity = 0; setPending = false
        displayPos = pos; smoothPos.value = pos; handlePos.value = pos; tempPosition.value = pos
    }

    function onSliderDragMove(pos) {
        if (!dragging) return
        displayPos = pos; smoothPos.value = pos; handlePos.value = pos; tempPosition.value = pos
    }

    function onSliderDragEnd(pos) {
        if (!dragging) return
        dragging = false

        handlePos.value    = pos
        tempPosition.value = pos

        displayPos      = realPos
        smoothPos.value = realPos
        moveStartPos    = realPos
        moveStartTime   = Date.now()

        if (pos < realPos) {
            velocity = -(100 / ((props.device.prefs?.down_time ?? 3000) * 10))
            setPending = true
        } else if (pos > realPos) {
            velocity = 100 / ((props.device.prefs?.up_time ?? 3000) * 10)
            setPending = true
        } else {
            velocity = 0; setPending = false
        }

        updatePosition(pos)
    }

</script>

<template>
    <div class="flex flex-col h-full select-none" :class="{ 'opacity-80 pointer-events-none': isLoading }">
        
        <header class="px-5 pt-5 pb-4 flex items-center justify-between shrink-0">
            <div class="flex items-center gap-3">
                <div class="shrink-0 p-2 bg-tp-accent/10 rounded-[14px]">
                    <Blinds class="text-tp-accent w-5 h-5" />
                </div>
                <h2 class="text-base font-bold tracking-tight text-tp-text-primary">{{ device.name }}</h2>
            </div>
            <button @click="pressBtn('close', () => emit('close'))"
                    class="blind-btn blind-btn-muted"
                    :class="{ pressing: pressing['close'] }">
                <X class="w-[15px] h-[15px] text-muted" />
            </button>
        </header>

        <!-- MOBILE LAYOUT -->
        <div class="md:hidden flex-1 flex items-center justify-center px-5 pb-6 gap-4">
            <div class="flex flex-col items-center gap-3 flex-1 max-w-[110px]">
                <BlindSlider
                    class="w-full aspect-[3/5]"
                    :fill-pos="smoothPos"
                    :handle-pos="handlePos"
                    @drag-start="onSliderDragStart"
                    @drag-move="onSliderDragMove"
                    @drag-end="onSliderDragEnd"
                />
                <div class="flex items-baseline gap-1">
                    <span class="text-2xl font-mono font-bold text-tp-text-primary">{{ tempPosition }}</span>
                    <span class="text-sm font-bold text-tp-accent">%</span>
                </div>
            </div>

            <div class="flex flex-col gap-3">
                <button @click="handleUp" class="blind-btn" :class="{ pressing: pressing['up'] }">
                    <ChevronUp class="w-[18px] h-[18px] text-tp-text-primary/80" />
                </button>
                <button @click="handleStop" class="blind-btn" :class="{ pressing: pressing['stop'] }">
                    <Pause class="w-[15px] h-[15px] fill-current text-tp-text-primary/80" />
                </button>
                <button @click="handleDown" class="blind-btn" :class="{ pressing: pressing['down'] }">
                    <ChevronDown class="w-[18px] h-[18px] text-tp-text-primary/80" />
                </button>
            </div>
        </div>

        <!-- DESKTOP LAYOUT -->
        <div class="hidden md:flex flex-1 flex-col items-center justify-center p-6 space-y-8">
            <div class="flex flex-col items-center gap-4">
                <BlindSlider
                    class="w-40 h-64"
                    :fill-pos="smoothPos"
                    :handle-pos="handlePos"
                    @drag-start="onSliderDragStart"
                    @drag-move="onSliderDragMove"
                    @drag-end="onSliderDragEnd"
                />
                <div class="flex items-baseline gap-1">
                    <span class="text-3xl font-mono font-bold text-tp-text-primary">{{ tempPosition }}</span>
                    <span class="text-sm font-bold text-tp-accent">%</span>
                </div>
            </div>

            <div class="w-full max-w-65 space-y-8">
                <div class="grid grid-cols-3 gap-3">
                    <button @click="handleUp" class="flex items-center justify-center p-4 bg-tp-border/20 border border-tp-border rounded-xl transition-all cursor-pointer hover:bg-tp-accent/10 hover:border-tp-accent/50 group">
                        <ChevronUp class="w-6 h-6 text-muted group-hover:text-tp-accent" />
                    </button>
                    <button @click="handleStop" class="flex items-center justify-center p-4 bg-tp-border/20 border border-tp-border rounded-xl transition-all cursor-pointer hover:bg-tp-stop/10 hover:border-tp-stop/50 group">
                        <Square class="w-4 h-4 text-muted group-hover:text-tp-stop fill-current" />
                    </button>
                    <button @click="handleDown" class="flex items-center justify-center p-4 bg-tp-border/20 border border-tp-border rounded-xl transition-all cursor-pointer hover:bg-tp-accent/10 hover:border-tp-accent/50 group">
                        <ChevronDown class="w-6 h-6 text-muted group-hover:text-tp-accent" />
                    </button>
                </div>

                <div class="flex gap-3 h-14">
                    <div class="flex-1 bg-tp-bg/50 border border-tp-border rounded-xl flex items-center px-4 focus-within:border-tp-accent/50 transition-colors">
                        <input type="number" v-model.number="tempPosition" @keyup.enter="updatePosition(tempPosition)"
                               placeholder="0-100"
                               class="w-full bg-transparent border-none text-sm font-mono text-tp-text-primary focus:outline-none [appearance:textfield]"
                        />
                        <span class="text-muted/30 font-mono text-lg">%</span>
                    </div>
                    <button @click="updatePosition(tempPosition)" class="flex items-center justify-center px-6 bg-tp-border/20 border border-tp-border rounded-xl transition-all cursor-pointer hover:bg-tp-accent/10 hover:border-tp-accent/50 group">
                        <Check class="w-5 h-5 text-muted group-hover:text-tp-accent transition-colors" />
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>
