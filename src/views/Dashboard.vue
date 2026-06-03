<script setup>

    import { ref, computed } from 'vue'

    import PageLayout from '@/layout/PageLayout.vue'

    import Sidebar from '@/layout/Sidebar.vue';
    import Bottombar from '@/layout/Bottombar.vue';
    import Topbar from '@/layout/dashboard/Topbar.vue';

    import Blueprint from '@/layout/dashboard/Blueprint.vue';

    const activeSection = ref('blueprint')
    const activeComponent = computed(() => {

        const sections = {
            blueprint: Blueprint
        }

        return sections[activeSection.value]
    })

</script>

<template>

    <PageLayout>

        <Sidebar v-model:activeSection="activeSection" />

        <main class="flex flex-col flex-1">
            <Topbar />
            <component :is="activeComponent" />
        </main>

        <Bottombar v-model:activeSection="activeSection" />

    </PageLayout>

</template>
