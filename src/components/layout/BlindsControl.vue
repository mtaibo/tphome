<script setup>

    import { ref, computed } from 'vue'
    import { X, ChevronUp, ChevronDown, Square } from 'lucide-vue-next'

    const props = defineProps({
        device: {
            type: Object,
            required: true
        }
    })

    const emit = defineEmits(['close'])

    const tempPosition = ref(props.device.state.position)

    const updatePosition = (newVal) => {
        tempPosition.value = newVal
        props.device.state.position = newVal 
    }

</script>

<template>

    <div class="flex flex-col h-full text-muted p-6 select-none">
        
        <header class="flex items-center justify-between mb-8">

            <h2 class="text-lg font-bold tracking-tight">{{ device.name }}</h2>

            <button 
                @click="$emit('close')" 
                class="p-2 hover:bg-white/10 rounded-full transition-colors cursor-pointer"
            >
                <X class="w-5 h-5 text-muted" />
            </button>

        </header>


        <div class="flex-1 flex flex-col items-center justify-center gap-8">
        
            <div class="relative w-24 h-64 bg-black/40 rounded-xl border border-tp-border overflow-hidden">

                <div class="absolute inset-y-0 left-2 w-px bg-tp-border/30"></div>
                <div class="absolute inset-y-0 right-2 w-px bg-tp-border/30"></div>

                <div 
                    class="absolute top-0 w-full bg-muted/30 transition-all duration-500 ease-out flex flex-col gap-1 p-1"
                    :style="{ height: tempPosition + '%' }"
                >
                    <div v-for="i in 15" :key="i" class="h-1 w-full bg-black/20 rounded-full"></div>
                </div>

                <input 
                    type="range"
                    min="0"
                    max="100"
                    step="1"
                    v-model.number="tempPosition"
                    @input="updatePosition($event.target.value)"
                    class="absolute inset-0 w-full h-full opacity-0 cursor-pointer [appearance:slider-vertical] rotate-180"
                />

            </div>

            <div class="text-center">
                <span class="text-4xl font-mono font-light">{{ tempPosition }}%</span>
                <p class="text-[10px] text-muted uppercase tracking-tighter mt-1">Apertura actual</p>
            </div>

        </div>


        <div class="grid grid-cols-3 gap-3 mt-auto">

            <button 
                class="flex flex-col items-center gap-2 p-4 bg-white/5 border border-tp-border rounded-xl hover:bg-tp-accent/20 hover:border-tp-accent/50 transition-all cursor-pointer"
                @click="updatePosition(100)"
            >
                <ChevronUp class="w-5 h-5 text-tp-accent" />
            </button>

            <button 
                class="flex flex-col items-center gap-2 p-4 bg-white/5 border border-tp-border rounded-xl hover:bg-tp-danger/20 hover:border-tp-danger/50 transition-all cursor-pointer"
            >
                <Square class="w-5 h-5 text-tp-danger" />
            </button>

            <button 
                class="flex flex-col items-center gap-2 p-4 bg-white/5 border border-tp-border rounded-xl hover:bg-tp-accent/20 hover:border-tp-accent/50 transition-all cursor-pointer"
                @click="updatePosition(0)"
            >
                <ChevronDown class="w-5 h-5 text-tp-accent" />
            </button>

        </div>

    </div>

</template>

<style scoped>

    input[type="range"]::-webkit-slider-runnable-track {
        cursor: pointer;
    }

</style>