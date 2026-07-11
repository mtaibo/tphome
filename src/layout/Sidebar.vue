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
        class="relative z-20 hidden md:flex md:flex-col shrink-0 transition-[width] duration-500 ease-[cubic-bezier(0.4,0,0.2,1)]"
        :class="collapsed ? 'w-18' : 'w-60'"
    >

        <!-- Botón anclado, no se desplaza -->
        <div class="absolute top-4 right-3 z-20">
            <BlindBtn :pressing="false" @click="toggle">
                <component :is="collapsed ? PanelLeftOpen : PanelLeftClose" class="w-[18px] h-[18px] text-tp-text/80" />
            </BlindBtn>
        </div>

        <!-- Máscara de recorte: se encoge con el aside -->
        <div class="absolute inset-0 overflow-hidden z-10">

            <!-- Panel deslizante: ancho fijo, se mueve hacia la izquierda al colapsar -->
            <!-- w-60 = 240px, w-16 = 64px, diferencia = 176px = translate-x-44 -->
            <div
                class="w-60 h-full flex flex-col bg-[#111113] shadow-xl transition-transform duration-500 ease-[cubic-bezier(0.4,0,0.2,1)]"
                :class="collapsed ? '-translate-x-60' : 'translate-x-0'"
            >
                <div class="h-[72px] shrink-0" />

                <nav class="flex-1 p-3 space-y-2">
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

                <footer class="p-4">
                    <UserCard :collapsed="false" />
                </footer>
            </div>

        </div>

    </aside>

</template>
