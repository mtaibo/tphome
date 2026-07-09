
<script setup>

    import { computed } from 'vue';

    const props = defineProps({
        activeSection: { type: String, default: 'blueprint' }
    })

    const sectionNames = {
        blueprint: 'Plano',
        lights: 'Luces',
        blinds: 'Persianas',
        scenes: 'Escenas',
        active: 'Dispositivos',
        pending: 'Pendientes',
        json: 'JSON',
        firmware: 'Firmware',
    }

    const sectionTitle = computed(() => sectionNames[props.activeSection] ?? 'Plano')

</script>

<template>

    <header class="topbar">
        <h1 class="text-[34px] font-bold text-white tracking-tight leading-none">{{ sectionTitle }}</h1>
    </header>

</template>
