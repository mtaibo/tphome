<script setup>

    import { ref } from 'vue'
    import { ArrowLeft, Smartphone } from 'lucide-vue-next'

    const sections = [
        { id: 'dispositivos', name: 'Dispositivos', icon: Smartphone }
    ]
    const activeSection = ref('dispositivos')

    defineExpose({ activeSection })

</script>

<template>

    <aside class="w-56 min-w-56 flex flex-col border-r border-tp-border bg-tp-surface shrink-0">

        <header class="h-20 px-6 flex items-center border-b border-tp-border">
            <RouterLink
                to="/"
                class="flex items-center gap-2 text-sm text-muted hover:text-white transition-colors"
            >
                <ArrowLeft class="w-4 h-4" />
                <span class="font-medium">Ajustes</span>
            </RouterLink>
        </header>

        <nav class="flex-1 p-3 space-y-1">
            <button
                v-for="section in sections"
                :key="section.id"
                @click="activeSection = section.id"
                class="w-full flex items-center gap-3 px-4 py-2.5 rounded-lg text-sm transition-all duration-200 cursor-pointer"
                :class="activeSection === section.id
                    ? 'bg-tp-accent/10 text-tp-accent font-semibold'
                    : 'text-muted hover:text-white hover:bg-tp-border/20'"
            >
                <component :is="section.icon" class="w-4 h-4 shrink-0" />
                {{ section.name }}
            </button>
        </nav>

        <footer class="p-4 border-t border-tp-border">
            <span class="text-[10px] font-mono text-muted/40">TPHome v1.0.0</span>
        </footer>

    </aside>

</template>
