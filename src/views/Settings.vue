<script setup>

    import { useRoute } from 'vue-router'
    import { useSections } from '@/config/sections.js'

    import PageLayout from '@/layout/PageLayout.vue'

    import Sidebar from '@/layout/Sidebar.vue'
    import Bottombar from '@/layout/Bottombar.vue'
    import Topbar from '@/layout/Topbar.vue'

    const route = useRoute()
    const { sections, activeSection, activeComponent } = useSections(route.path)

</script>

<template>

    <PageLayout>

        <Sidebar v-model:activeSection="activeSection" />

        <main class="flex flex-col flex-1 pt-20 md:pt-0">
            <Topbar :activeSection="activeSection" />
            <component :is="activeComponent" />
        </main>

        <Bottombar v-model:activeSection="activeSection" :sections="sections"/>

    </PageLayout>

</template>

<style scoped>
@reference "tailwindcss";
    @media (display-mode: standalone) {
        main {
            padding-top: calc(5rem + env(safe-area-inset-top));
        }
    }
</style>
