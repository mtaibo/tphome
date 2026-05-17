<script setup>

    import DeviceManager from '@/layout/settings/DeviceManager.vue'
    import Sidebar from '@/layout/settings/Sidebar.vue'

    import { ref } from 'vue'

    const sidebarRef = ref(null)

</script>

<template>

    <div class="flex h-screen w-screen overflow-hidden font-sans bg-tp-bg text-slate-200">

        <Sidebar ref="sidebarRef" />

        <main class="flex-1 overflow-hidden">
            <DeviceManager />
        </main>

    </div>

</template>
