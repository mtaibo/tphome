<script setup>

    import { ref, onMounted } from 'vue';

    import Sidebar from './layout/Sidebar.vue';
    import Topbar from './layout/Topbar.vue';
    import Blueprint from './components/Blueprint.vue';

    import { useDevices } from './db/devices'

    const isOnline = ref(true); // API connection status

    const store = useDevices()
    onMounted(async () => { await store.setup() })

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