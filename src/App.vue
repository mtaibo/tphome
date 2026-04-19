<script setup>
import { ref } from 'vue';
import Sidebar from './components/layout/Sidebar.vue';
import Topbar from './components/layout/Topbar.vue';
import Dashboard from './views/Dashboard.vue';

// Estado global de conexión (que luego actualizarás con WebSockets)
const isOnline = ref(true);
</script>

<template>
  <div class="flex h-screen w-screen bg-tp-bg text-slate-200 overflow-hidden font-sans">
    
    <Sidebar />

    <main class="flex-1 flex flex-col relative overflow-hidden">
      <Topbar :isOnline="isOnline" />

      <section class="flex-1 relative overflow-hidden bg-[radial-gradient(var(--color-tp-border)_1px,transparent_1px)] [background-size:32px_32px]">
        <Dashboard />
      </section>
    </main>

  </div>
</template>