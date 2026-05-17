<script setup>

    import { ref } from 'vue'
    import { useRouter } from 'vue-router'
    import { Smartphone, ArrowLeft, PanelLeftClose, PanelLeftOpen } from 'lucide-vue-next'

    import Header from '@/components/sidebar/Header.vue'
    import NavButton from '@/components/sidebar/NavButton.vue'

    const router = useRouter()

    const collapsed = ref(false)

    const toggle = () => {
        collapsed.value = !collapsed.value
        localStorage.setItem('sidebar-settings-collapsed', collapsed.value)
    }

    const sections = [
        { id: 'dispositivos', name: 'Dispositivos', icon: Smartphone }
    ]
    const activeSection = ref('dispositivos')

    defineExpose({ activeSection })

</script>

<template>

    <aside
        class="flex flex-col border-r border-tp-border bg-tp-surface shrink-0 transition-all duration-300 ease-in-out"
        :class="collapsed ? 'w-16 min-w-16 max-w-16' : 'w-56 min-w-56 max-w-56'"
    >

        <Header :collapsed="collapsed" />

        <nav class="flex-1 p-3 space-y-2">
            <NavButton
                v-for="section in sections"
                :key="section.id"
                :icon="section.icon"
                :label="section.name"
                :active="activeSection === section.id"
                :collapsed="collapsed"
                :nav-item="true"
                @click="activeSection = section.id"
            />
        </nav>

        <footer class="p-4 border-t border-tp-border space-y-2">

            <NavButton
                :icon="collapsed ? PanelLeftOpen : PanelLeftClose"
                label="Colapsar"
                :collapsed="collapsed"
                :nav-item="false"
                @click="toggle"
            />

            <NavButton
                :icon="ArrowLeft"
                label="Volver al plano"
                :collapsed="collapsed"
                :nav-item="false"
                @click="router.push('/')"
            />

            <div
                class="overflow-hidden transition-all duration-300"
                :class="collapsed ? 'h-0 opacity-0' : 'h-auto opacity-100'"
            >
                <span class="block text-[10px] font-mono text-muted/40 pt-2 px-4">TPHome v1.0.0</span>
            </div>

        </footer>

    </aside>

</template>
