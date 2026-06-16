<script setup>

    import { ref, computed } from 'vue'

    import PageLayout from '@/layout/PageLayout.vue'

    import Sidebar from '@/layout/Sidebar.vue'
    import Bottombar from '@/layout/Bottombar.vue'
    import Topbar from '@/layout/Topbar.vue';

    import { getSections, getActiveComponent } from '@/config/sections.js'

    const route = useRoute()
    const sections = getSections(route.path)

    const activeSection = ref(sections[0].id)
    const activeComponent = computed(() => getActiveComponent(sections, activeSection.value))

</script>

<template>

    <PageLayout>

        <Sidebar v-model:activeSection="activeSection" />

        <main class="flex-1"> 
            <component :is="activeComponent" />
        </main>

        <Bottombar v-model:activeSection="activeSection" />

    </PageLayout>

</template>
