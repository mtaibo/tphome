<script setup>

    import { ref } from 'vue'

    import Sidebar from '@/layout/Sidebar.vue';
    import BottomBar from '@/layout/dashboard/BottomBar.vue';
    import Blueprint from '@/layout/dashboard/Blueprint.vue';
    import Topbar from '@/layout/dashboard/Topbar.vue';

    const activeSection = ref('blueprint')

</script>

<template>

    <div class="flex h-screen w-screen overflow-clip font-sans bg-tp-bg text-slate-200">
    
        <Sidebar v-model:activeItem="activeSection" />

        <main class="flex-1 flex flex-col relative overflow-hidden pb-18 md:pb-0 z-10">
            <Topbar />
            <section class="flex-1 relative overflow-hidden">
                <Blueprint v-if="activeSection === 'blueprint'" />
            </section>
        </main>

        <BottomBar />

    </div>

</template>
