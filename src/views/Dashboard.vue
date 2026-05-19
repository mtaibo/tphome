<script setup>

    /* Control */
    import Sidebar from '@/layout/Sidebar.vue';
    import BottomBar from '@/layout/dashboard/BottomBar.vue';

    /* Content */
    import Blueprint from '@/layout/dashboard/Blueprint.vue';

    /* Info */
    import Topbar from '@/layout/dashboard/Topbar.vue';
    import { apiOnline } from '@/config/socket'

</script>

<template>

  <div class="flex h-screen w-screen overflow-clip font-sans bg-tp-bg text-slate-200">
    
    <Sidebar />

    <!-- Dot background - top-20 to not be shown below topbar due to its oppacity -->
    <div class="fixed inset-0 top-20 bg-grid-dots pointer-events-none z-0"></div>

    <main class="flex-1 flex flex-col relative overflow-hidden pb-18 md:pb-0 z-10">
      <Topbar/>
      <section class="flex-1 relative overflow-hidden"><Blueprint /></section>
    </main>

    <BottomBar />

    <!-- Mobile-only API status dot -->
    <div
        class="md:hidden fixed top-4 left-4 z-50 w-2.5 h-2.5 rounded-full shadow-[0_0_8px] animate-pulse transition-all duration-500"
        :class="apiOnline ? 'bg-tp-ok shadow-tp-ok/50' : 'bg-tp-danger shadow-tp-danger/50'"
    ></div>

  </div>

</template>
