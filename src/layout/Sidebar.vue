<script setup>

    import { ref } from 'vue'
    import { useRouter, useRoute } from 'vue-router'

    import { Settings, PanelLeftClose, PanelLeftOpen, ArrowLeft } from 'lucide-vue-next'

    import { useSections } from '@/config/sections.js'

    import NavButton from '@/components/sidebar/NavButton.vue'
    import UserCard from '@/components/sidebar/UserCard.vue'

    const props = defineProps({ activeSection: { type: String } })
    const emit = defineEmits(['update:activeSection'])

    const router = useRouter()
    const route = useRoute()

    const { sections } = useSections(route.path)

    const navSections = computed(() => sections.map(({ id, name, icon }) => ({ id, name, icon })))

    const collapsed = ref(false)
    const toggle = () => { collapsed.value = !collapsed.value }

    function setActive(id) {
        emit('update:activeSection', id)
    }

</script>

<template>

    <aside
        class="z-20 hidden md:flex md:flex-col shadow-xl bg-[#111113] transition-all duration-300 ease-in-out shrink-0"
        :class="collapsed ? 'w-16 min-w-16 max-w-16' : 'w-1/5 min-w-44 max-w-60'"
    >

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
            <NavButton
                :icon="route.path === '/settings' ? ArrowLeft : Settings"
                :label="route.path === '/settings' ? 'Volver' : 'Configuración'"
                :active="false"
                :collapsed="collapsed"
                :nav-item="true"
                @click="route.path === '/settings' ? router.push('/') : router.push('/settings')"
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

            <UserCard :collapsed="collapsed" />

        </footer>

    </aside>

</template>
