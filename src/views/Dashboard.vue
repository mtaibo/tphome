<script setup>

    import Sidebar from '@/layout/Sidebar.vue';
    import Topbar from '@/layout/dashboard/Topbar.vue';
    import Blueprint from '@/layout/dashboard/Blueprint.vue';
    import BottomBar from '@/layout/dashboard/BottomBar.vue';

    import { apiOnline } from '@/config/socket'

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

    <!-- Mobile-only API status indicator dot -->
    <div
        class="md:hidden fixed top-4 left-4 z-50 w-2.5 h-2.5 rounded-full shadow-[0_0_8px] animate-pulse transition-all duration-500"
        :class="apiOnline ? 'bg-tp-ok shadow-tp-ok/50' : 'bg-tp-danger shadow-tp-danger/50'"
    ></div>

  </div>

</template>
