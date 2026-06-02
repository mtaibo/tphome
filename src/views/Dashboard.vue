<script setup>

    import Sidebar from '@/layout/Sidebar.vue';
    import Bottombar from '@/layout/BottomBar.vue';
    import Topbar from '@/layout/dashboard/Topbar.vue';

    /* Content */
    import Blueprint from '@/layout/dashboard/Blueprint.vue';

    import { ref, computed } from 'vue'
    const activeSection = ref('blueprint')

    const currentComponent = computed(() => {
        const sections = {
            blueprint: Blueprint
        }
        return sections[activeSection.value]
    })

</script>

<template>

    <div class="flex h-screen w-screen overflow-clip font-sans bg-tp-bg text-slate-200">
    
        <!-- LAYOUT -->
        <Topbar />
        <Bottombar />
        <Sidebar v-model:activeSection="activeSection" />

        <!-- CONTENT -->
        <main class="flex-1 relative overflow-hidden pb-18 md:pb-0 pt-20 z-10">
            <component :is="currentComponent" class="w-full h-full"/>
        </main>

    </div>

</template>
