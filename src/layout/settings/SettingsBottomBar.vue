<script setup>

    import { useRouter } from 'vue-router'
    import { Smartphone, Clock, Code, Cpu, ArrowLeft } from 'lucide-vue-next'

    const props = defineProps({
        activeSection: { type: String, default: 'active' }
    })
    const emit = defineEmits(['update:activeSection'])

    const router = useRouter()

    const navItems = [
        { id: 'active',    name: 'Dispositivos', icon: Smartphone },
        { id: 'pending',   name: 'Pendientes',   icon: Clock },
        { id: 'json',      name: 'JSON',         icon: Code },
        { id: 'firmware',  name: 'Firmware',     icon: Cpu },
    ]

    function setActive(id) {
        emit('update:activeSection', id)
    }

</script>

<template>

    <footer class="md:hidden fixed bottom-0 left-0 right-0 z-50 h-18 flex items-center justify-between px-8 pt-2 pb-8 bg-tp-surface border-t border-tp-border">

        <div class="flex items-center gap-4">
            <button
                v-for="item in navItems"
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

        <button
            @click="router.push('/')"
            class="flex items-center justify-center w-8 h-8 rounded-lg transition-all duration-200 active:scale-95 cursor-pointer text-muted hover:text-white hover:bg-tp-border/20"
        >
            <ArrowLeft class="w-4 h-4" />
        </button>

    </footer>

</template>
