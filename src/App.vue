<script setup>

    import { ref } from 'vue';

    import Sidebar from './components/Sidebar.vue';
    import Topbar from './components/Topbar.vue';
    import Blueprint from './components/Blueprint.vue';

    const isOnline = ref(true); // API connection status

</script>

<template>

  <div class="flex h-screen w-screen overflow-hidden font-sans bg-tp-bg text-slate-200">
    
    <Sidebar />

    <main class="flex-1 flex flex-col relative overflow-hidden">

      <Topbar :isOnline="isOnline" />

      <section class="flex-1 relative overflow-hidden bg-grid-dots">
        <Blueprint />
      </section>

    </main>

  </div>

</template>