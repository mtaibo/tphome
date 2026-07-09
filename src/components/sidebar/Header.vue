<script setup>

    import { House } from 'lucide-vue-next'

    defineProps({
        collapsed: { type: Boolean, default: false }
    })

</script>

<template>

    <header
        class="h-20 flex items-center overflow-hidden transition-all duration-300"
        :class="collapsed ? 'px-[14px]' : 'px-4 gap-4'"
    >
        <div class="shrink-0">
            <House class="text-tp-accent w-9 h-9" />
        </div>

        <div
            class="flex flex-col justify-center min-w-0 transition-[width,opacity] duration-300"
            :class="collapsed ? 'opacity-0 w-0' : 'opacity-100'"
        >
            <h1 class="text-xl font-bold tracking-tight whitespace-nowrap">TPHome</h1>
            <span class="text-[10px] font-mono text-tp-muted/60 tracking-wider whitespace-nowrap">v1.0.0</span>
        </div>
    </header>

</template>
