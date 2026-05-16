<script setup>

    import Sidebar from '../layout/Sidebar.vue';
    import Topbar from '../layout/Topbar.vue';
    import BottomBar from '../layout/BottomBar.vue';
    import Blueprint from '../components/Blueprint.vue';
    import { apiOnline } from '../config/socket'

</script>

<template>

  <div class="flex h-screen w-screen overflow-clip font-sans bg-tp-bg text-slate-200">
    
    <Sidebar />

    <main class="flex-1 flex flex-col relative overflow-hidden pb-18 md:pb-0">

      <Topbar/>

      <section class="flex-1 relative overflow-hidden bg-grid-dots">
        <Blueprint />
      </section>

    </main>

    <BottomBar />

    <div
        class="md:hidden fixed top-4 left-4 z-50 flex items-center gap-2 px-2 py-1.5 rounded-lg bg-tp-surface/80 backdrop-blur-sm border border-tp-border"
        :class="apiOnline ? 'is-online' : 'is-offline'"
    >
        <div class="status-dot"></div>
    </div>

  </div>

</template>