<script setup>

    /* Fixed layout */
    import Sidebar from '@/layout/Sidebar.vue';
    import BottomBar from '@/layout/dashboard/BottomBar.vue';

    /* Custom layout */
    import Topbar from '@/layout/dashboard/Topbar.vue';

    /* Content */
    import Blueprint from '@/layout/dashboard/Blueprint.vue';

    import { ref } from 'vue'
    const activeSection = ref('blueprint')

</script>

<template>

    <div class="flex h-screen w-screen overflow-clip font-sans bg-tp-bg text-slate-200">
    
        <Sidebar v-model:activeItem="activeSection" />
        <Topbar />

        <main class="flex flex-1 relative overflow-hidden pb-18 md:pb-0 pt-20 z-10">

            <section class="flex-1 relative overflow-hidden">
                <Blueprint v-if="activeSection === 'blueprint'" />
            </section>

        </main>

        <BottomBar />

    </div>

</template>
