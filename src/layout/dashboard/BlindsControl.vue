<script setup>
    import { ref, watch, nextTick, onMounted, onUnmounted } from 'vue'
    import { X, ChevronUp, ChevronDown, Pause, Blinds, Check } from 'lucide-vue-next'
    import { api } from '@/config/api'

    const props = defineProps({
        id:     { type: String, required: true },
        device: { type: Object, required: true }
    })
    const emit = defineEmits(['close'])

    const tempPosition = ref(props.device.state.position)
    const isLoading    = ref(false)
    const pressing     = ref({})

    // Smooth animation state
    let realPos        = props.device.state.position
    let realTime       = Date.now()
    let velocity       = 0      // % per millisecond
    let lastKnownSpeed = 0.007  // updated from real WS data, used as seed on button press
    let displayPos     = props.device.state.position  // internal float driving the UI
    let lastFrameTime  = Date.now()
    let rafId          = null

    // Track real position updates from WS and derive velocity
    watch(() => props.device.state.position, (newPos) => {
        const now = Date.now()
        const dt  = now - realTime
        if (dt > 50) {
            velocity = (newPos - realPos) / dt
            if (Math.abs(velocity) > 0.001) lastKnownSpeed = Math.abs(velocity)
        }
        realPos  = newPos
        realTime = now
    })

    // When motor stops, kill velocity so spring corrects any overshoot
    watch(() => props.device.state.motor_state, () => {
        velocity = 0
        realPos  = props.device.state.position
        realTime = Date.now()
    })

    function animate() {
        const now = Date.now()
        const dt  = Math.min(now - lastFrameTime, 50)
        lastFrameTime = now

        if (!dragging) {
            // Spring: move by velocity + gentle pull toward realPos.
            // Higher corrRate when stopped so overshoot corrects fast.
            const corrRate = Math.abs(velocity) > 0.002 ? 0.002 : 0.006
            displayPos += velocity * dt + (realPos - displayPos) * corrRate * dt
            displayPos  = Math.max(0, Math.min(100, displayPos))
            tempPosition.value = Math.round(displayPos)
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
        displayPos = tempPosition.value; realPos = displayPos; realTime = Date.now(); velocity = lastKnownSpeed
        sendCommand('up')
    })
    const handleDown = () => pressBtn('down', () => {
        displayPos = tempPosition.value; realPos = displayPos; realTime = Date.now(); velocity = -lastKnownSpeed
        sendCommand('down')
    })
    const handleStop = () => pressBtn('stop', () => { velocity = 0; sendCommand('stop') })

    let dragging = false

    function posFromY(el, clientY) {
        const rect = el.getBoundingClientRect()
        const y = clientY - rect.top
        return Math.max(0, Math.min(100, Math.round((1 - y / rect.height) * 100)))
    }

    function onPointerDown(e) {
        dragging = true
        const pos = posFromY(e.currentTarget, e.clientY)
        displayPos = pos
        tempPosition.value = pos
        e.currentTarget.setPointerCapture(e.pointerId)
    }

    function onPointerMove(e) {
        if (!dragging) return
        const pos = posFromY(e.currentTarget, e.clientY)
        displayPos = pos
        tempPosition.value = pos
    }

    function onPointerUp(e) {
        if (!dragging) return
        dragging = false
        const pos = posFromY(e.currentTarget, e.clientY)
        displayPos = pos
        updatePosition(pos)
        realPos  = pos
        realTime = Date.now()
        velocity = 0
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
                <div class="relative w-full aspect-[3/5] rounded-[26px] overflow-hidden touch-none select-none cursor-grab active:cursor-grabbing"
                     style="background: linear-gradient(180deg, rgba(255,255,255,0.07) 0%, rgba(255,255,255,0.04) 100%); border: 0.5px solid rgba(255,255,255,0.13); box-shadow: inset 0 2px 8px rgba(0,0,0,0.22), inset 0 1px 0 rgba(255,255,255,0.09);"
                     @pointerdown="onPointerDown"
                     @pointermove="onPointerMove"
                     @pointerup="onPointerUp"
                     @pointercancel="onPointerUp">
                    <!-- Slats fill from top -->
                    <div class="absolute top-0 left-0 right-0 overflow-hidden"
                         :class="tempPosition < 100 ? 'border-b border-tp-accent/35' : ''"
                         :style="{ height: (100 - tempPosition) + '%' }">
                        <div class="flex flex-col gap-[3px] px-[4px] pt-[4px]">
                            <div v-for="i in 24" :key="i"
                                 class="w-full bg-white/14 rounded-[2px] shrink-0"
                                 style="height: 4px; min-height: 4px;"></div>
                        </div>
                    </div>
                    <!-- Handle -->
                    <div class="absolute left-[7px] right-[7px] h-5 rounded-[10px] pointer-events-none"
                         style="background: linear-gradient(135deg, rgba(255,255,255,0.96), rgba(255,255,255,0.82)); box-shadow: 0 2px 8px rgba(0,0,0,0.30), inset 0 1px 0 white; transition: top 0.08s ease-out;"
                         :style="{ top: `calc(${100 - tempPosition}% - 10px)` }">
                    </div>
                </div>
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
                <div class="relative w-40 h-64 bg-black/40 rounded-2xl border border-tp-border shadow-inner overflow-hidden touch-none select-none"
                     @pointerdown="onPointerDown"
                     @pointermove="onPointerMove"
                     @pointerup="onPointerUp"
                     @pointercancel="onPointerUp">
                    <div class="absolute inset-y-0 left-4 w-px bg-tp-border/10"></div>
                    <div class="absolute inset-y-0 right-4 w-px bg-tp-border/10"></div>
                    <div class="absolute top-0 w-full bg-muted/20 border-b border-tp-accent/40 transition-all duration-700 ease-in-out flex flex-col gap-1.5 p-2 overflow-hidden"
                         :style="{ height: (100 - tempPosition) + '%' }">
                        <div v-for="i in 20" :key="i" class="h-2 min-h-2 w-full bg-muted/30 rounded-sm shrink-0 shadow-sm"></div>
                    </div>
                </div>
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
