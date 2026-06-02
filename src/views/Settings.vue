<script setup>

    import { ref } from 'vue'

    import Sidebar from '@/layout/Sidebar.vue'
    import SettingsBottomBar from '@/layout/settings/SettingsBottomBar.vue'
    import ActiveDevices from '@/layout/settings/ActiveDevices.vue'
    import PendingDevices from '@/layout/settings/PendingDevices.vue'
    import JsonEditor from '@/layout/settings/JsonEditor.vue'
    import FirmwareManager from '@/layout/settings/FirmwareManager.vue'

    const activeSection = ref('active')

</script>

<template>

    <div class="flex h-screen w-screen overflow-hidden font-sans bg-tp-bg text-slate-200">

        <Sidebar v-model:activeSection="activeSection" />

        <main class="flex-1 overflow-hidden pb-18 md:pb-0">
            <ActiveDevices   v-if      = " activeSection === 'active'   " />
            <PendingDevices  v-else-if = " activeSection === 'pending'  " />
            <JsonEditor      v-else-if = " activeSection === 'json'     " />
            <FirmwareManager v-else-if = " activeSection === 'firmware' " />
        </main>

        <SettingsBottomBar v-model:activeSection="activeSection" />

    </div>

</template>
