<script setup>
    import { ref, watch } from 'vue'
    import { X, ChevronUp, ChevronDown, Square, Blinds, Check } from 'lucide-vue-next'

    const props = defineProps({
        device: {
            type: Object,
            required: true
        }
    })

    const emit = defineEmits(['close'])

    const tempPosition = ref(props.device.state.position)
    const inputPosition = ref(props.device.state.position)

    const updatePosition = (newVal) => {
        let value = parseInt(newVal)
        if (isNaN(value)) value = 0
        value = Math.max(0, Math.min(100, value))
        
        tempPosition.value = value
        inputPosition.value = value
        props.device.state.position = value 
    }

    watch(tempPosition, (val) => {
        inputPosition.value = val
    })

    watch(() => props.device.state.position, (newVal) => {
        tempPosition.value = newVal
        inputPosition.value = newVal
    })
</script>

<template>

    <div class="flex flex-col h-full bg-tp-surface border-l border-tp-border shadow-xl select-none">
        
        <header class="h-20 px-6 flex items-center justify-between shrink-0">
            
            <!-- Blind Name and Icon -->
            <div class="flex items-center gap-4">

                <div class="shrink-0 p-2 bg-tp-accent/10 rounded-lg">
                    <Blinds class="text-tp-accent w-5 h-5" />
                </div>

                <h2 class="text-lg font-bold tracking-tight text-white">{{ device.name }}</h2>
                
            </div>

            <!-- Cross closing button -->
            <button 
                @click="$emit('close')" 
                class="p-2 hover:bg-tp-border/30 rounded-lg transition-colors cursor-pointer text-muted hover:text-white"
            >

                <X class="w-5 h-5" />

            </button>

        </header>

        <!-- Main Controls -->
        <div class="flex-1 flex flex-col items-center justify-center p-6 space-y-8">
        
            <!-- Blind control -->
            <div class="flex flex-col items-center gap-4">

                <!-- Blind representation -->
                <div class="relative w-40 h-64 bg-black/40 rounded-2xl border border-tp-border shadow-inner overflow-hidden">
                    <div class="absolute inset-y-0 left-4 w-px bg-tp-border/10"></div>
                    <div class="absolute inset-y-0 right-4 w-px bg-tp-border/10"></div>

                    <div 
                        class="absolute top-0 w-full bg-muted/20 border-b border-tp-accent/40 transition-all duration-700 ease-in-out flex flex-col gap-1.5 p-2 overflow-hidden"
                        :style="{ height: (100 - tempPosition) + '%' }"
                    >
                        <div v-for="i in 20" :key="i" class="h-2 min-h-[8px] w-full bg-muted/30 rounded-sm shrink-0 shadow-sm"></div>
                    </div>

                    <input 
                        type="range"
                        min="0"
                        max="100"
                        v-model.number="tempPosition"
                        @input="updatePosition($event.target.value)"
                        class="absolute inset-0 w-full h-full opacity-0 cursor-pointer [appearance:slider-vertical]"
                    />
                </div>
                
                <!-- Show current position -->
                <div class="flex items-baseline gap-1">
                    <span class="text-3xl font-mono font-bold text-white">{{ tempPosition }}</span>
                    <span class="text-sm font-bold text-tp-accent">%</span>
                </div>

            </div>

            <!-- Control buttons -->
            <div class="w-full max-w-[260px] space-y-8">
                
                <!-- Main buttons -->
                <div class="grid grid-cols-3 gap-3">
                    <button @click="updatePosition(100)" class="flex items-center justify-center p-4 bg-tp-border/20 border border-tp-border rounded-xl transition-all cursor-pointer hover:bg-tp-accent/10 hover:border-tp-accent/50 group">
                        <ChevronUp class="w-6 h-6 text-muted group-hover:text-tp-accent" />
                    </button>

                    <button class="flex items-center justify-center p-4 bg-tp-border/20 border border-tp-border rounded-xl transition-all cursor-pointer hover:bg-red-500/10 hover:border-red-500/50 group">
                        <Square class="w-4 h-4 text-muted group-hover:text-red-500 fill-current" />
                    </button>

                    <button @click="updatePosition(0)" class="flex items-center justify-center p-4 bg-tp-border/20 border border-tp-border rounded-xl transition-all cursor-pointer hover:bg-tp-accent/10 hover:border-tp-accent/50 group">
                        <ChevronDown class="w-6 h-6 text-muted group-hover:text-tp-accent" />
                    </button>
                </div>

                <!-- Precise position input -->
               <div class="flex gap-3 h-14">

                    <!-- Field to introduce position -->
                    <div class="flex-1 bg-tp-bg/50 border border-tp-border rounded-xl flex items-center px-4 focus-within:border-tp-accent/50 transition-colors">

                        <input 
                            type="number"
                            v-model="inputPosition"
                            @keyup.enter="updatePosition(inputPosition)"
                            placeholder="0-100"
                            class="w-full bg-transparent border-none text-sm font-mono text-white focus:outline-none [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
                        />

                        <span class="text-muted/30 font-mono text-lg">%</span>

                    </div>

                    <!-- Button to send inputPosition-->
                    <button 
                        @click="updatePosition(inputPosition)"
                        class="flex items-center justify-center px-6 bg-tp-border/20 border border-tp-border rounded-xl transition-all cursor-pointer hover:bg-tp-accent/10 hover:border-tp-accent/50 group"
                    >

                        <Check class="w-5 h-5 text-muted group-hover:text-tp-accent transition-colors" />

                    </button>

                </div> 

            </div>
        </div>

    </div>
</template>

<style scoped>
    input[type="range"] {
        -webkit-appearance: slider-vertical;
        width: 100%;
        height: 100%;
    }
</style>