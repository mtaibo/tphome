<script setup>
    import { ref, watch } from 'vue'
    import { X, ChevronUp, ChevronDown, Square, Blinds, Check } from 'lucide-vue-next'
    import { api } from '@/config/api'

    const props = defineProps({
        id:     { type: String, required: true },
        device: { type: Object, required: true }
    })
    const emit = defineEmits(['close'])

    const tempPosition = ref(props.device.state.position)
    const isLoading    = ref(false)

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

    const handleUp   = () => { tempPosition.value = 100; sendCommand('up')   }
    const handleDown = () => { tempPosition.value = tempPosition.value === 20 ? 0 : 20; sendCommand('down') }
    const handleStop = () => { sendCommand('stop') }

    let dragging = false

    function posFromY(el, clientY) {
        const rect = el.getBoundingClientRect()
        const y = clientY - rect.top
        return Math.max(0, Math.min(100, Math.round((1 - y / rect.height) * 100)))
    }

    function onPointerDown(e) {
        dragging = true
        tempPosition.value = posFromY(e.currentTarget, e.clientY)
        e.currentTarget.setPointerCapture(e.pointerId)
    }

    function onPointerMove(e) {
        if (!dragging) return
        tempPosition.value = posFromY(e.currentTarget, e.clientY)
    }

    function onPointerUp(e) {
        if (!dragging) return
        dragging = false
        updatePosition(posFromY(e.currentTarget, e.clientY))
    }

    watch(() => props.device.state.position, (val) => {
        tempPosition.value = val
    }, { immediate: true })

</script>

<template>
    <div class="flex flex-col h-full md:bg-tp-surface bg-transparent md:border-l md:border-tp-border select-none" :class="{ 'opacity-80 pointer-events-none': isLoading }">
        
        <header class="h-20 px-6 flex items-center justify-between shrink-0">
            <div class="flex items-center gap-4">
                <div class="shrink-0 p-2 bg-tp-accent/10 rounded-lg">
                    <Blinds class="text-tp-accent w-5 h-5" />
                </div>
                <h2 class="text-lg font-bold tracking-tight text-tp-text-primary">{{ device.name }}</h2>
            </div>
            <button @click="emit('close')" class="p-2 hover:bg-tp-border/30 rounded-lg transition-colors cursor-pointer text-muted hover:text-tp-text-primary">
                <X class="w-5 h-5" />
            </button>
        </header>

        <!-- MOBILE LAYOUT -->
        <div class="md:hidden flex-1 flex items-center justify-center px-4 pb-6 gap-3">
            <div class="flex flex-col items-center gap-3 flex-1 max-w-[140px]">
                <div class="relative w-full aspect-[3/5] bg-black/40 rounded-2xl border border-tp-border shadow-inner overflow-hidden touch-none select-none"
                     @pointerdown="onPointerDown"
                     @pointermove="onPointerMove"
                     @pointerup="onPointerUp"
                     @pointercancel="onPointerUp">
                    <div class="absolute inset-y-0 left-3 w-px bg-tp-border/10"></div>
                    <div class="absolute inset-y-0 right-3 w-px bg-tp-border/10"></div>
                    <div class="absolute top-0 w-full bg-muted/20 border-b border-tp-accent/40 transition-all duration-700 ease-in-out flex flex-col gap-1 p-1.5 overflow-hidden"
                         :style="{ height: (100 - tempPosition) + '%' }">
                        <div v-for="i in 16" :key="i" class="h-1.5 min-h-1.5 w-full bg-muted/30 rounded-sm shrink-0 shadow-sm"></div>
                    </div>
                </div>
                <div class="flex items-baseline gap-1">
                    <span class="text-2xl font-mono font-bold text-tp-text-primary">{{ tempPosition }}</span>
                    <span class="text-sm font-bold text-tp-accent">%</span>
                </div>
            </div>

            <div class="flex flex-col gap-3">
                <button @click="handleUp" class="flex items-center justify-center p-4 bg-tp-border/20 border border-tp-border rounded-xl hover:bg-tp-accent/10 hover:border-tp-accent/50 group cursor-pointer transition-all">
                    <ChevronUp class="w-6 h-6 text-muted group-hover:text-tp-accent" />
                </button>
                <button @click="handleStop" class="flex items-center justify-center p-4 bg-tp-border/20 border border-tp-border rounded-xl cursor-pointer hover:bg-tp-stop/10 hover:border-tp-stop/50 group transition-all">
                    <Square class="w-4 h-4 text-muted group-hover:text-tp-stop fill-current" />
                </button>
                <button @click="handleDown" class="flex items-center justify-center p-4 bg-tp-border/20 border border-tp-border rounded-xl hover:bg-tp-accent/10 hover:border-tp-accent/50 group cursor-pointer transition-all">
                    <ChevronDown class="w-6 h-6 text-muted group-hover:text-tp-accent" />
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