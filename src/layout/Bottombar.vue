<script setup>

    import { ref, computed } from 'vue'
    //import { useUpdate } from '@/config/update'
    import { useRouter, useRoute } from 'vue-router'

    import { LayoutDashboard, Blinds, Lightbulb, Settings, RefreshCw, Smartphone, ArrowLeft, Clock, Code, Cpu } from 'lucide-vue-next'

    //import { NavButton } from '@/components/bottombar/NavButton.vue'

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

    const update = () => {}

    function setActive(id) {
        emit('update:activeSection', id)
    }

</script>

<template>

    <footer class="md:hidden fixed bottom-0 left-0 right-0 z-50 h-18 flex items-center justify-between px-8 pt-2 pb-8 bg-tp-surface border-t border-tp-border">

        <div class="flex items-center gap-4">
            <button
                v-for="item in navSections"
                :key="item.id"
                @click="setActive(item.id)"
                class="flex items-center justify-center w-8 h-8 rounded-lg transition-all duration-200 active:scale-95 cursor-pointer"
                :class="activeSection === item.id
                    ? 'text-tp-accent bg-tp-accent/10'
                    : 'text-muted hover:text-white hover:bg-tp-border/20'"
            >
                <component :is="item.icon" class="w-4 h-4" />
            </button>
        </div>

        <div class="flex items-center gap-4">

            <button
                @click="update"
                :class="isDashboard ? 'flex' : 'hidden'"
                class="items-center justify-center w-8 h-8 rounded-lg transition-all duration-200 active:scale-95 cursor-pointer text-muted hover:text-tp-accent hover:bg-tp-border/20"
            >
                <RefreshCw class="w-3.5 h-3.5" />
            </button>

            <button
                @click="router.push('/settings')"
                class="items-center justify-center w-8 h-8 rounded-lg transition-all duration-200 active:scale-95 cursor-pointer text-muted hover:text-tp-accent hover:bg-tp-border/20"
                :class="isDashboard ? 'flex' : 'hidden'"
            >
                <Settings class="w-4 h-4" />
            </button>

            <button
                @click="router.push('/')"
                class="items-center justify-center w-8 h-8 rounded-lg transition-all duration-200 active:scale-95 cursor-pointer text-muted hover:text-tp-accent hover:bg-tp-border/20"
                :class="isDashboard ? 'hidden' : 'flex'"
            >
                <ArrowLeft class="w-4 h-4" />
            </button>

        </div>

    </footer>

</template>
