<script setup>
    import { User } from 'lucide-vue-next'

    defineProps({
        collapsed: {
            type: Boolean,
            default: false,
        },
    })
</script>

<template>
    <div
        class="flex items-center overflow-hidden transition-all duration-300 rounded-xl"
        :class="collapsed ? 'p-0 border-0 bg-transparent' : 'px-4 py-3 bg-tp-bg/50 border border-tp-border'"
        :title="collapsed ? 'Miguel' : ''"
    >
        <div class="w-8 h-8 rounded-lg bg-tp-border flex items-center justify-center shrink-0">
            <User class="w-4 h-4 text-tp-accent" />
        </div>
        <div
            class="flex flex-col text-left whitespace-nowrap overflow-hidden transition-[width,opacity] duration-300"
            :class="collapsed ? 'w-0 opacity-0' : 'opacity-100 ml-3'"
        >
            <span class="text-xs font-bold leading-none">Miguel</span>
            <span class="text-[10px] text-muted italic mt-1">Administrador</span>
        </div>
    </div>
</template>
