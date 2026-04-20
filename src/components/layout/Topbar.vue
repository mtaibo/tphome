<script setup>

    import { RefreshCw, Bell } from 'lucide-vue-next';

    defineProps({
        isOnline: Boolean
    });

</script>

<template>

    <header class="h-20 z-10 flex items-center justify-between px-10 bg-tp-surface/60  border-b border-tp-border ">

        <div class="flex items-center gap-6"> 
            
            <!-- API STATUS -->
            <div class="flex flex-col">

                <span class="text-[10px] font-mono text-muted/60 uppercase tracking-widest">API</span>

                <div class="flex items-center gap-2" :class="isOnline ? 'is-online' : 'is-offline'">
                    <div class="status-dot"></div>
                    <span class="status-text">{{ isOnline ? 'Online' : 'Offline' }}</span>
                </div>

            </div>

            <!-- DIVIDER -->
            <div class="h-8 w-px bg-tp-border/50"></div>

            <!-- ONLINE DEVICES COUNTER -->
            <div class="flex flex-col">

                <span class="text-[10px] font-mono text-muted/60 uppercase tracking-widest">Dispositivos</span>

                <div class="flex items-center gap-1.5">
                    <span class="text-xs font-bold text-tp-accent">12</span>
                    <span class="text-[10px] text-muted uppercase">Activos</span>
                </div>

            </div>

        </div>

        <div class="flex items-center gap-4">

            <button class="p-2.5 bg-tp-border/30 rounded-full hover:bg-tp-accent/20 hover:text-tp-accent transition-all text-muted">
                <Bell class="w-5 h-5" />
            </button>

            <button class="p-2.5 bg-tp-border/30 rounded-full hover:bg-tp-accent/20 hover:text-tp-accent transition-all text-muted">
                <RefreshCw class="w-5 h-5" />
            </button>

        </div>

    </header>

</template>