
<script setup>

    import { onMounted } from 'vue'

    import { useDevices } from './config/devices'
    import { useMap } from './config/map'
    import { useSections } from './config/sections'

    import Sidebar   from '@/layout/Sidebar.vue'
    import Topbar    from '@/layout/Topbar.vue'
    import Bottombar from '@/layout/Bottombar.vue'

    const devices = useDevices()
    const map = useMap()

    onMounted(async () => {
        await devices.setup()
        await map.setup()
    })

    const { allSections, activeSection, activeComponent, activeSectionName } = useSections()

</script>

<template>

    <div class="page-layout">

        <Sidebar />

        <main class="flex flex-col flex-1 h-full md:pt-0">
            <Topbar :title="activeSectionName" />
            <component :is="activeComponent" />
        </main>

        <Bottombar v-model:activeSection="activeSection" :sections="allSections" />

    </div>

</template>
