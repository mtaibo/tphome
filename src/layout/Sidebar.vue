<script setup>

    import { ref, computed } from 'vue'
    import { useRouter, useRoute } from 'vue-router'
    import { LayoutDashboard, Blinds, Lightbulb, Settings as SettingsIcon, User, PanelLeftClose, PanelLeftOpen, Smartphone, ArrowLeft } from 'lucide-vue-next'

    import Header from '@/components/sidebar/Header.vue'
    import NavButton from '@/components/sidebar/NavButton.vue'

    const router = useRouter()
    const route = useRoute()

    const isDashboard = computed(() => route.path === '/')

    const collapsed = ref(localStorage.getItem('sidebar-collapsed') === 'true')

    const toggle = () => {
        collapsed.value = !collapsed.value
        localStorage.setItem('sidebar-collapsed', collapsed.value)
    }

    const dashboardItems = [
        { id: 'blueprint', name: 'Plano',     icon: LayoutDashboard },
        { id: 'lights',    name: 'Luces',     icon: Lightbulb       },
        { id: 'blinds',    name: 'Persianas', icon: Blinds          },
    ]
    const settingsItems = [
        { id: 'dispositivos', name: 'Dispositivos', icon: Smartphone }
    ]

    const navItems = computed(() => isDashboard.value ? dashboardItems : settingsItems)

    const activeItem = ref('blueprint')

</script>

<template>

    <aside
        class="z-20 hidden md:flex md:flex-col border-r border-tp-border shadow-xl bg-tp-surface transition-all duration-300 ease-in-out shrink-0"
        :class="collapsed ? 'w-16 min-w-16 max-w-16' : 'w-1/5 min-w-44 max-w-60'"
    >

        <Header :collapsed="collapsed" />

        <nav class="flex-1 p-3 space-y-2">
            <NavButton
                v-for="item in navItems"
                :key="item.id"
                :icon="item.icon"
                :label="item.name"
                :active="activeItem === item.id"
                :collapsed="collapsed"
                :nav-item="true"
                @click="activeItem = item.id"
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
                v-if="isDashboard"
                :icon="SettingsIcon"
                label="Configuración"
                :collapsed="collapsed"
                :nav-item="false"
                @click="router.push('/settings')"
            />

            <NavButton
                v-else
                :icon="ArrowLeft"
                label="Volver al plano"
                :collapsed="collapsed"
                :nav-item="false"
                @click="router.push('/')"
            />

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

        </footer>

    </aside>

</template>
