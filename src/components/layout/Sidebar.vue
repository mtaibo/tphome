<script setup>
import { ref } from 'vue';
import { LayoutDashboard, Blinds, Lightbulb, Settings, House, User } from 'lucide-vue-next';

const activeTab = ref('plano');
</script>

<template>
  <aside class="w-72 bg-tp-surface border-r border-tp-border flex flex-col z-20 shadow-xl">
    <div class="p-8 flex flex-col items-center gap-3">
      <div class="w-14 h-14 bg-linear-to-br from-tp-accent to-tp-accent2 rounded-2xl flex items-center justify-center shadow-[0_0_25px_rgba(79,156,249,0.4)]">
        <House class="text-white w-8 h-8" />
      </div>
      <div class="text-center">
        <h1 class="text-2xl font-bold tracking-tighter bg-gradient-to-r from-tp-accent to-tp-accent2 bg-clip-text text-transparent">
          TPHOME
        </h1>
        <p class="text-[10px] text-muted tracking-[0.3em] uppercase font-mono mt-1 opacity-70">Control Central</p>
      </div>
    </div>

    <nav class="flex-1 px-4 space-y-2">
      <button v-for="item in [
        { id: 'plano', name: 'Plano de Casa', icon: LayoutDashboard },
        { id: 'luces', name: 'Luces', icon: Lightbulb },
        { id: 'persianas', name: 'Persianas', icon: Blinds }
      ]" :key="item.id"
        @click="activeTab = item.id"
        :class="['w-full flex items-center gap-4 px-4 py-3 rounded-xl transition-all duration-300 border', 
        activeTab === item.id ? 'bg-tp-accent/10 border-tp-accent/30 text-tp-accent shadow-inner' : 'border-transparent text-muted hover:bg-tp-border/40 hover:text-white']"
      >
        <component :is="item.icon" class="w-5 h-5" />
        <span class="font-medium text-sm">{{ item.name }}</span>
      </button>
    </nav>

    <div class="p-4 border-t border-tp-border space-y-2">
      <button class="w-full flex items-center gap-4 px-4 py-3 rounded-xl text-muted hover:text-white transition-colors">
        <Settings class="w-5 h-5" />
        <span class="text-sm font-medium">Configuración</span>
      </button>
      <div class="flex items-center gap-3 px-4 py-3 bg-tp-bg/50 rounded-2xl border border-tp-border">
        <div class="w-8 h-8 rounded-full bg-tp-border flex items-center justify-center">
          <User class="w-4 h-4 text-tp-accent" />
        </div>
        <div class="flex flex-col text-left">
          <span class="text-xs font-bold leading-none">Miguel</span>
          <span class="text-[10px] text-muted italic mt-1">Administrador</span>
        </div>
      </div>
    </div>
  </aside>
</template>