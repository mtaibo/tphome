<script setup>

    import { ref } from 'vue'

    import Sidebar from '@/layout/Sidebar.vue'
    import ActiveDevices from '@/layout/settings/ActiveDevices.vue'
    import PendingDevices from '@/layout/settings/PendingDevices.vue'
    import JsonEditor from '@/layout/settings/JsonEditor.vue'

    const activeItem = ref('active')

</script>

<template>

    <div class="flex h-screen w-screen overflow-hidden font-sans bg-tp-bg text-slate-200">

        <Sidebar v-model:activeItem="activeItem" />

        <main class="flex-1 overflow-hidden">
            <ActiveDevices v-if="activeItem === 'active'" />
            <PendingDevices v-else-if="activeItem === 'pending'" />
            <JsonEditor v-else-if="activeItem === 'json'" />
        </main>

    </div>

</template>
