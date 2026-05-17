<script setup>

    import DeviceManager from '@/layout/settings/DeviceManager.vue'
    import Sidebar from '@/layout/Sidebar.vue'

</script>

<template>

    <div class="flex h-screen w-screen overflow-hidden font-sans bg-tp-bg text-slate-200">

        <Sidebar />

        <main class="flex-1 overflow-hidden">
            <DeviceManager />
        </main>

    </div>

</template>
