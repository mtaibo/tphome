<script setup>

    import { ref, computed } from 'vue'
    import { useRouter, useRoute } from 'vue-router'

    import { Settings, PanelLeftClose, PanelLeftOpen, ArrowLeft } from 'lucide-vue-next'

    import { useSections } from '@/config/sections.js'

    import NavButton from '@/components/sidebar/NavButton.vue'
    import UserCard from '@/components/sidebar/UserCard.vue'
    import BlindBtn from '@/components/BlindBtn.vue'

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
        class="z-20 hidden md:flex md:flex-col transition-all duration-500 ease-[cubic-bezier(0.4,0,0.2,1)] shrink-0 overflow-hidden"
        :class="collapsed
            ? 'w-16 min-w-16 max-w-16 bg-transparent shadow-none'
            : 'w-1/5 min-w-44 max-w-60 bg-[#111113] shadow-xl'"
    >

        <div class="flex justify-end px-3 pt-4 pb-6">
            <BlindBtn :pressing="false" @click="toggle">
                <component :is="collapsed ? PanelLeftOpen : PanelLeftClose" class="w-[18px] h-[18px] text-tp-text/80" />
            </BlindBtn>
        </div>

        <nav v-show="!collapsed" class="flex-1 p-3 space-y-2">
            <NavButton
                v-for="item in navSections"
                :key="item.id"
                :icon="item.icon"
                :label="item.name"
                :active="props.activeSection === item.id"
                :collapsed="false"
                :nav-item="true"
                @click="setActive(item.id)"
            />
            <NavButton
                :icon="route.path === '/settings' ? ArrowLeft : Settings"
                :label="route.path === '/settings' ? 'Volver' : 'Configuración'"
                :active="false"
                :collapsed="false"
                :nav-item="true"
                @click="route.path === '/settings' ? router.push('/') : router.push('/settings')"
            />
        </nav>

        <footer v-show="!collapsed" class="p-4">
            <UserCard :collapsed="false" />
        </footer>

    </aside>

</template>
