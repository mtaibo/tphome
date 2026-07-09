
<script setup>

    import { useRoute } from 'vue-router'
    import { useSections } from '@/config/sections.js'

    import Sidebar from '@/layout/Sidebar.vue'
    import Bottombar from '@/layout/Bottombar.vue'
    import Topbar from '@/layout/Topbar.vue'

    const route = useRoute()
    const { sections, activeSection, activeComponent, activeSectionName } = useSections(route.path)

</script>

<template>

    <div class="page-layout">

        <Sidebar v-model:activeSection="activeSection" />

        <main class="flex flex-col flex-1 pt-20 md:pt-0">
            <Topbar :title="activeSectionName" />
            <component :is="activeComponent" />
        </main>

        <Bottombar v-model:activeSection="activeSection" :sections="sections"/>

    </div>

</template>
