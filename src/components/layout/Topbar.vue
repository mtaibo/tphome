<script setup>
import { Wifi, RefreshCw, Bell } from 'lucide-vue-next';

// Recibimos la variable isOnline desde el padre (App.vue)
defineProps({
  isOnline: Boolean
});
</script>

<template>
  <header class="h-20 bg-tp-surface/60 backdrop-blur-xl border-b border-tp-border flex items-center justify-between px-10 z-10">
    <div class="flex flex-col">
      <h2 class="text-lg font-semibold tracking-tight text-white">Panel de Control</h2>
      <div class="flex items-center gap-2">
        <div :class="['w-2 h-2 rounded-full shadow-[0_0_8px]', 
          isOnline ? 'bg-tp-ok shadow-tp-ok/50 animate-pulse' : 'bg-tp-danger shadow-tp-danger/50']">
        </div>
        <span class="text-[10px] font-mono uppercase tracking-widest text-muted">
          SISTEMA: {{ isOnline ? 'Online' : 'Offline' }}
        </span>
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