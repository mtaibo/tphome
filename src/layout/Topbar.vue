<script setup>

    import { computed } from 'vue';
    import { RefreshCw } from 'lucide-vue-next';

    import { useDevices } from '@/config/devices'
    import { useMap } from '@/config/map'
    import { apiOnline } from '@/config/socket'
    import { socket_manager } from '@/config/socket'
    import { api } from '@/config/api'

    const props = defineProps({
        activeSection: { type: String, default: 'blueprint' }
    })

    const store = useDevices()
    const map = useMap()

    const sectionNames = {
        blueprint: 'Plano',
        lights: 'Luces',
        blinds: 'Persianas',
        scenes: 'Escenas',
        active: 'Dispositivos',
        pending: 'Pendientes',
        json: 'JSON',
        firmware: 'Firmware',
    }

    const sectionTitle = computed(() => sectionNames[props.activeSection] ?? 'Plano')

    const isSettingsSection = computed(() =>
        ['active', 'pending', 'json', 'firmware'].includes(props.activeSection)
    )

    const handleUpdate = async () => {
        await api.triggerUpdate()
        await store.setup()
        await map.setup()
        socket_manager.reconnect()
    }

</script>

<template>

    <header class="fixed top-0 left-0 right-0 z-20 flex items-center justify-between px-6 md:px-10 bg-transparent border-0 md:relative md:bg-tp-surface/60 md:border-b md:border-tp-border md:backdrop-blur-md topbar-header">

        <!-- Mobile: section title -->
        <div class="md:hidden">
            <h1 class="text-[34px] font-bold text-white tracking-tight leading-none">{{ sectionTitle }}</h1>
        </div>

        <!-- Desktop: section title (settings only) -->
        <div v-if="isSettingsSection" class="hidden md:block">
            <h1 class="text-[34px] font-bold text-white tracking-tight leading-none">{{ sectionTitle }}</h1>
        </div>

        <!-- Desktop: status + devices -->
        <div v-if="!isSettingsSection" class="hidden md:flex items-center gap-6"> 
            
            <!-- API STATUS -->
            <div class="flex flex-col">

                <span class="text-[10px] font-mono text-muted/60 uppercase tracking-widest">API</span>

                <div class="flex items-center gap-2" :class="apiOnline ? 'is-online' : 'is-offline'">
                    <div class="status-dot"></div>
                    <span class="status-text">{{ apiOnline ? 'Online' : 'Offline' }}</span>
                </div>

            </div>

            <!-- DIVIDER -->
            <div class="h-8 w-px bg-tp-border/50"></div>

            <!-- ONLINE DEVICES COUNTER -->
            <div class="flex flex-col">

                <span class="text-[10px] font-mono text-muted/60 uppercase tracking-widest">Dispositivos</span>

                <div class="flex items-center gap-1.5">
                    <span class="text-xs font-bold text-tp-accent">{{ store.active }}</span>
                    <span class="text-[10px] text-tp-accent/80 uppercase">Activos</span>
                </div>

            </div>

        </div>


        <div v-if="!isSettingsSection" class="flex items-center gap-6">

            <!-- UNCONFIGURED DEVICES -->
            <div 
                v-if="store.pendingCount > 0"
                class="hidden md:flex items-center gap-2.5 px-3 py-1.5 bg-tp-danger/5 border border-tp-danger/20 rounded-lg  hover:bg-tp-danger/10 hover:border-tp-danger/40 transition-all duration-300 cursor-pointer"
            >
  
                <div class="w-1.5 h-1.5 bg-tp-danger rounded-full shadow-[0_0_8px_var(--color-tp-danger)]"></div>
                <span class="text-[10px] font-bold text-tp-danger uppercase tracking-tight">{{ store.pendingCount }} Dispositivos sin configurar</span>

            </div>

            <!-- UPDATE -->
            <button 
                @click="handleUpdate"
                class="hidden md:group md:flex items-center gap-2.5 px-3 py-1.5 rounded-lg transition-all duration-300 active:scale-95 cursor-pointer"
            >
            
                <RefreshCw class="w-3.5 h-3.5 text-muted group-hover:text-tp-accent group-hover:rotate-180 transition-all duration-500" />
                <span class="text-xs font-mono font-medium text-muted/80 group-hover:text-tp-accent uppercase tracking-wider">UPDATE</span>

            </button>

        </div>


    </header>

</template>

<style scoped>
@reference "tailwindcss";

    .topbar-header {
        padding-top: var(--safe-top);
        height: calc(5rem + var(--safe-top));
    }

</style>
