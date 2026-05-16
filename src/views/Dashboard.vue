<script setup>

    import Sidebar from '../layout/Sidebar.vue';
    import Topbar from '../layout/Topbar.vue';
    import BottomBar from '../layout/BottomBar.vue';
    import Blueprint from '../components/Blueprint.vue';

</script>

<template>

  <div class="flex h-screen w-screen overflow-clip font-sans bg-tp-bg text-slate-200">
    
    <Sidebar />

    <main class="flex-1 flex flex-col relative overflow-hidden pb-14 md:pb-0">

      <Topbar/>

      <section class="flex-1 relative overflow-hidden bg-grid-dots">
        <Blueprint />
      </section>

    </main>

    <BottomBar />

  </div>

</template>