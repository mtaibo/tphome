<script setup>

    import { ref } from 'vue';
    import { RefreshCw, Settings } from 'lucide-vue-next';

    import { apiOnline } from '../config/socket'
    import { useDevices } from '../config/devices'

    const store = useDevices()

    const pendingCount = ref(0);

    const togglePending = () => {
        if (pendingCount.value === 0) {
            pendingCount.value = 2;
        } else {
            pendingCount.value = 0;
        }
    }

</script>

<template>

    <header class="h-12 md:h-20 z-10 flex items-center justify-between px-4 md:px-10 bg-tp-surface/60  border-b border-tp-border ">

        <div class="flex items-center gap-6"> 
            
            <!-- API STATUS -->
            <div :class="apiOnline ? 'is-online' : 'is-offline'" class="flex flex-col">

                <span class="text-[10px] font-mono text-muted/60 uppercase tracking-widest hidden md:block">API</span>

                <div class="flex items-center gap-2">
                    <div class="status-dot"></div>
                    <span class="status-text hidden md:inline">{{ apiOnline ? 'Online' : 'Offline' }}</span>
                </div>

            </div>

            <!-- DIVIDER -->
            <div class="h-8 w-px bg-tp-border/50 hidden md:block"></div>

            <!-- ONLINE DEVICES COUNTER -->
            <div class="flex-col hidden md:flex">

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
                v-if="pendingCount > 0"
                class="hidden md:flex items-center gap-2.5 px-3 py-1.5 bg-tp-danger/5 border border-tp-danger/20 rounded-lg  hover:bg-tp-danger/10 hover:border-tp-danger/40 transition-all duration-300 cursor-pointer"
            >
  
                <div class="w-1.5 h-1.5 bg-tp-danger rounded-full shadow-[0_0_8px_var(--color-tp-danger)]"></div>
                <span class="text-[10px] font-bold text-tp-danger uppercase tracking-tight">2 Dispositivos sin configurar</span>

            </div>

            <!-- SETTINGS (mobile only) -->
            <RouterLink
                to="/settings"
                class="md:hidden flex items-center justify-center w-8 h-8 rounded-lg text-muted hover:text-white hover:bg-tp-border/20 transition-all duration-200"
            >
                <Settings class="w-4 h-4" />
            </RouterLink>

            <!-- UPDATE -->
            <button 
                @click="togglePending"
                class="group flex items-center gap-2.5 px-3 py-1.5 rounded-lg transition-all duration-300 active:scale-95 cursor-pointer"
            >
            
                <RefreshCw class="w-3.5 h-3.5 text-muted group-hover:text-tp-accent group-hover:rotate-180 transition-all duration-500" />
                <span class="text-xs font-mono font-medium text-muted/80 group-hover:text-tp-accent uppercase tracking-wider hidden md:inline">UPDATE</span>

            </button>

        </div>

    </header>

</template>