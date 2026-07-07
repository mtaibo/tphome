<script setup>
    import { ref, watch } from 'vue'
    import { ChevronUp, ChevronDown, Square, Blinds } from 'lucide-vue-next'
    import { useDevices } from '@/config/devices'
    import { api } from '@/config/api'

    const store = useDevices()

    const positions  = ref({})
    const loading    = ref({})
    const draggingId = ref(null)

    watch(() => store.blinds, (blinds) => {
        for (const [id, device] of Object.entries(blinds)) {
            if (draggingId.value !== id) {
                positions.value[id] = device.state?.position ?? 0
            }
        }
    }, { immediate: true, deep: true })

    const sendCommand = async (id, cmd, val = null) => {
        loading.value[id] = true
        try { await api.sendCommand(id, cmd, val) }
        catch (e) { console.error('TPHome - BlindsSection:', e) }
        finally { loading.value[id] = false }
    }

    const onSliderInput  = (id, val) => { draggingId.value = id; positions.value[id] = Number(val) }
    const onSliderChange = (id, val) => { draggingId.value = null; sendCommand(id, 'set', Number(val)) }

    const handleUp   = (id) => { positions.value[id] = 100; sendCommand(id, 'up')   }
    const handleDown = (id) => { positions.value[id] = 0;   sendCommand(id, 'down') }
    const handleStop = (id) => { sendCommand(id, 'stop') }

    const sliderStyle = (id) => ({ '--blind-val': (positions.value[id] ?? 0) + '%' })
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
        <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            <div
                v-for="(device, id) in store.blinds"
                :key="id"
                class="blind-card transition-opacity duration-300 select-none"
                :class="{ 'opacity-50 pointer-events-none': loading[id] }"
            >
                <!-- Header -->
                <div class="flex items-start justify-between mb-5">
                    <div class="flex items-center gap-3">
                        <div class="p-2 rounded-xl transition-colors duration-300"
                             :class="device.connection?.online ? 'bg-tp-accent/15' : 'bg-white/5'">
                            <Blinds class="w-4.5 h-4.5 transition-colors duration-300"
                                    :class="device.connection?.online ? 'text-tp-accent' : 'text-muted'" />
                        </div>
                        <div>
                            <h3 class="text-sm font-semibold text-tp-text-primary leading-tight">{{ device.name }}</h3>
                            <p class="text-[10px] font-medium tracking-widest uppercase mt-0.5 transition-colors duration-300"
                               :class="device.connection?.online ? 'text-tp-ok' : 'text-muted'">
                                {{ device.connection?.online ? 'En línea' : 'Sin conexión' }}
                            </p>
                        </div>
                    </div>
                    <div class="flex items-baseline gap-0.5 mt-0.5">
                        <span class="text-2xl font-mono font-bold text-tp-text-primary tabular-nums leading-none">{{ positions[id] ?? 0 }}</span>
                        <span class="text-xs font-bold text-tp-accent leading-none mb-0.5">%</span>
                    </div>
                </div>

                <!-- Mini blind visualization -->
                <div class="relative w-full h-14 rounded-2xl overflow-hidden mb-5 bg-black/30 border border-white/[0.06]">
                    <div class="absolute inset-y-0 left-5 w-px bg-white/[0.04]"></div>
                    <div class="absolute inset-y-0 right-5 w-px bg-white/[0.04]"></div>
                    <div class="absolute top-0 left-0 right-0 flex flex-col gap-[2.5px] p-[3px] overflow-hidden transition-all duration-500 ease-in-out"
                         :class="(positions[id] ?? 0) < 100 ? 'border-b border-tp-accent/35' : ''"
                         :style="{ height: (100 - (positions[id] ?? 0)) + '%' }">
                        <div v-for="i in 14" :key="i" class="h-[4.5px] min-h-[4.5px] w-full bg-muted/22 rounded-sm shrink-0"></div>
                    </div>
                </div>

                <!-- Position slider -->
                <div class="mb-5 px-0.5">
                    <input
                        type="range"
                        min="0" max="100"
                        :value="positions[id] ?? 0"
                        :style="sliderStyle(id)"
                        class="blind-slider w-full"
                        @input="onSliderInput(id, $event.target.value)"
                        @change="onSliderChange(id, $event.target.value)"
                    />
                </div>

                <!-- Control buttons -->
                <div class="grid grid-cols-3 gap-2">
                    <button @click="handleUp(id)"
                            class="blind-btn group hover:bg-tp-accent/12 hover:border-tp-accent/35 active:scale-95">
                        <ChevronUp class="w-5 h-5 text-muted group-hover:text-tp-accent transition-colors duration-200" />
                    </button>
                    <button @click="handleStop(id)"
                            class="blind-btn group hover:bg-tp-stop/12 hover:border-tp-stop/35 active:scale-95">
                        <Square class="w-3.5 h-3.5 fill-current text-muted group-hover:text-tp-stop transition-colors duration-200" />
                    </button>
                    <button @click="handleDown(id)"
                            class="blind-btn group hover:bg-tp-accent/12 hover:border-tp-accent/35 active:scale-95">
                        <ChevronDown class="w-5 h-5 text-muted group-hover:text-tp-accent transition-colors duration-200" />
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>
