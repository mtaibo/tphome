<script setup>

    import Sidebar from '../layout/Sidebar.vue';
    import Topbar from '../layout/Topbar.vue';
    import Blueprint from '../components/Blueprint.vue';

</script>

<template>

  <div class="flex h-screen w-screen overflow-hidden font-sans bg-grid-dots text-slate-200 items-center justify-center">
    
    <RouterLink
        to="/"
        class="flex items-center gap-2 px-3 py-2 rounded-lg text-lg text-muted hover:text-white transition-colors duration-200"
    >
        <ArrowLeft class="w-4 h-4" />
        <span>Volver</span>
    </RouterLink>

  </div>

</template>