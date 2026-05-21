<script setup>

    import { RefreshCw } from 'lucide-vue-next';

    import { useDevices } from '@/config/devices'
    import { useMap } from '@/config/map'
    import { apiOnline } from '@/config/socket'
    import { socket_manager } from '@/config/socket'
    import { api } from '@/config/api'

    const store = useDevices()
    const map = useMap()

    const handleUpdate = async () => {
        socket_manager.reconnect()
        await store.setup()
        await map.setup()
        await api.triggerUpdate()
    }

</script>

<template>

        <header class="h-20 z-10 hidden md:flex items-center justify-between px-10 bg-tp-surface/60 border-b border-tp-border">

        <div class="flex items-center gap-6"> 
            
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


        <div class="flex items-center gap-6">

            <!-- UNCONFIGURED DEVICES -->
            <div 
                v-if="store.pendingCount > 0"
                class="flex items-center gap-2.5 px-3 py-1.5 bg-tp-danger/5 border border-tp-danger/20 rounded-lg  hover:bg-tp-danger/10 hover:border-tp-danger/40 transition-all duration-300 cursor-pointer"
            >
  
                <div class="w-1.5 h-1.5 bg-tp-danger rounded-full shadow-[0_0_8px_var(--color-tp-danger)]"></div>
                <span class="text-[10px] font-bold text-tp-danger uppercase tracking-tight">{{ store.pendingCount }} Dispositivos sin configurar</span>

            </div>

            <!-- UPDATE -->
            <button 
                @click="handleUpdate"
                class="group flex items-center gap-2.5 px-3 py-1.5 rounded-lg transition-all duration-300 active:scale-95 cursor-pointer"
            >
            
                <RefreshCw class="w-3.5 h-3.5 text-muted group-hover:text-tp-accent group-hover:rotate-180 transition-all duration-500" />
                <span class="text-xs font-mono font-medium text-muted/80 group-hover:text-tp-accent uppercase tracking-wider">UPDATE</span>

            </button>

        </div>

    </header>

</template>
