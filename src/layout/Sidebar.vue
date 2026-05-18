<script setup>

    import { ref, computed } from 'vue'
    import { useRouter, useRoute } from 'vue-router'
    import { LayoutDashboard, Blinds, Lightbulb, Settings as SettingsIcon, PanelLeftClose, PanelLeftOpen, Smartphone, ArrowLeft } from 'lucide-vue-next'

    import Header from '@/components/sidebar/Header.vue'
    import NavButton from '@/components/sidebar/NavButton.vue'
    import UserCard from '@/components/sidebar/UserCard.vue'

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
        { id: 'active',  name: 'Dispositivos', icon: Smartphone },
        { id: 'pending', name: 'Pendientes',   icon: Smartphone },
        { id: 'json',    name: 'JSON',         icon: Smartphone }
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
                label="Volver"
                :collapsed="collapsed"
                :nav-item="false"
                @click="router.push('/')"
            />

            <UserCard :collapsed="collapsed" />

        </footer>

    </aside>

</template>
