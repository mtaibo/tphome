<script setup>

    import { ref, computed } from 'vue'

    import PageLayout from '@/layout/PageLayout.vue'

    import Sidebar from '@/layout/Sidebar.vue'
    import Bottombar from '@/layout/Bottombar.vue'

    import ActiveDevices from '@/layout/settings/ActiveDevices.vue'
    import PendingDevices from '@/layout/settings/PendingDevices.vue'
    import JsonEditor from '@/layout/settings/JsonEditor.vue'
    import FirmwareManager from '@/layout/settings/FirmwareManager.vue'

    const activeSection = ref('active')
    const activeComponent = computed(() => {

        const sections = {
            active: ActiveDevices,
            pending: PendingDevices,
            json: JsonEditor,
            firmware: FirmwareManager
        }

        return sections[activeSection.value]
    })

</script>

<template>

    <PageLayout>

        <Sidebar v-model:activeSection="activeSection" />

        <main class="flex-1"> 
            <component  :is="activeComponent" />
        </main>

        <Bottombar v-model:activeSection="activeSection" />

    </PageLayout>

</template>
