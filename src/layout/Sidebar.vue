<script setup>

    import { ref, computed } from 'vue'
    import { useRouter, useRoute } from 'vue-router'

    import { LayoutDashboard, Blinds, Lightbulb, Settings, PanelLeftClose, PanelLeftOpen, Smartphone, ArrowLeft, Clock, Code, Cpu } from 'lucide-vue-next'

    import Header from '@/components/sidebar/Header.vue'
    import NavButton from '@/components/sidebar/NavButton.vue'
    import UserCard from '@/components/sidebar/UserCard.vue'

    const props = defineProps({ activeSection: { type: String } })
    const emit = defineEmits(['update:activeSection'])

    const dashboardSections = [
        { id: 'blueprint', name: 'Plano',     icon: LayoutDashboard },
        { id: 'lights',    name: 'Luces',     icon: Lightbulb       },
        { id: 'blinds',    name: 'Persianas', icon: Blinds          },
    ]

    const settingsSections = [
        { id: 'active',    name: 'Dispositivos', icon: Smartphone },
        { id: 'pending',   name: 'Pendientes',   icon: Clock },
        { id: 'json',      name: 'JSON',         icon: Code },
        { id: 'firmware',  name: 'Firmware',     icon: Cpu }
    ]

    const router = useRouter()
    const route = useRoute()

    const isDashboard = computed(() => route.path === '/')
    const navSections = computed(() => isDashboard.value ? dashboardSections : settingsSections)

    const collapsed = ref(false)
    const toggle = () => { collapsed.value = !collapsed.value }

    function setActive(id) {
        emit('update:activeSection', id)
    }

</script>

<template>

    <aside
        class="z-20 hidden md:flex md:flex-col border-r border-tp-border shadow-xl bg-tp-surface transition-all duration-300 ease-in-out shrink-0"
        :class="collapsed ? 'w-16 min-w-16 max-w-16' : 'w-1/5 min-w-44 max-w-60'"
    >

        <Header :collapsed="collapsed" />

        <nav class="flex-1 p-3 space-y-2">
            <NavButton
                v-for="item in navSections"
                :key="item.id"
                :icon="item.icon"
                :label="item.name"
                :active="props.activeSection === item.id"
                :collapsed="collapsed"
                :nav-item="true"
                @click="setActive(item.id)"
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
                :icon="Settings"
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
