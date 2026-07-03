<script setup>

    import { computed } from 'vue'
    import { useRouter, useRoute } from 'vue-router'

    import { Smartphone } from 'lucide-vue-next'

    const props = defineProps({ activeSection: String, sections: Array })
    const emit = defineEmits(['update:activeSection'])

    const router = useRouter() // Change route
    const route = useRoute() // Check route

    const isDashboard = computed(() => route.path === '/')

    const tabs = computed(() => [
        ...props.sections,
        isDashboard.value
            ? { id: 'settings', icon: Smartphone, action: () => router.push('/settings') }
            : { id: 'back', icon: Smartphone, action: () => router.push('/') }
    ])

    function setActive(item) {
        if (item.action) item.action()
        else emit('update:activeSection', item.id)
    }

</script>

<template>

    <nav class="liquid-bar">
        <button
            v-for="item in tabs"
            :key="item.id"
            @click="setActive(item)"
            class="tab-item"
            :class="{ active: activeSection === item.id && item.id !== 'settings' }"
        >
            <component :is="item.icon" />
        </button>
    </nav>

</template>

<style scoped>
@reference "tailwindcss";

    .liquid-bar {
        @apply fixed bottom-8 left-4 right-4 z-50 rounded-[24px] px-1.5 py-1.5 flex items-center justify-between;
        background: rgba(255, 255, 255, 0.06);
        backdrop-filter: blur(40px) saturate(200%);
        -webkit-backdrop-filter: blur(40px) saturate(200%);
        border: 0.5px solid rgba(255, 255, 255, 0.18);
        box-shadow:
            inset 0 1px 0 rgba(255, 255, 255, 0.25),
            inset 0 -0.5px 0 rgba(0, 0, 0, 0.08),
            0 20px 60px rgba(0, 0, 0, 0.5),
            0 0 0 0.5px rgba(255, 255, 255, 0.05);

        @media (min-width: 768px) {
            display: none;
        }
    }

    .tab-item {
        @apply flex items-center justify-center h-[38px] rounded-[18px] cursor-pointer flex-1 transition-[background] duration-150;
    }

    .tab-item.active {
        @apply w-14 flex-none;
        background: rgba(255, 255, 255, 0.18);
        box-shadow:
            inset 0 0.5px 0 rgba(255, 255, 255, 0.3),
            0 2px 8px rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
    }

    .tab-item svg {
        @apply w-[22px] h-[22px];
        opacity: 0.55;
        color: #fff;
        filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.3));
    }

    .tab-item.active svg {
        opacity: 1;
        filter: drop-shadow(0 0 8px rgba(255, 255, 255, 0.4));
    }
</style>
