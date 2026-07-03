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
        @apply fixed bottom-4 left-4 right-4 z-50 rounded-[28px] px-2 py-2 flex items-center justify-between;
        background: linear-gradient(
            135deg,
            rgba(255, 255, 255, 0.08) 0%,
            rgba(255, 255, 255, 0.04) 50%,
            rgba(255, 255, 255, 0.06) 100%
        );
        backdrop-filter: blur(50px) saturate(220%);
        -webkit-backdrop-filter: blur(50px) saturate(220%);
        border: 0.5px solid rgba(255, 255, 255, 0.22);
        box-shadow:
            inset 0 1.5px 0 rgba(255, 255, 255, 0.35),
            inset 0 -1px 0 rgba(0, 0, 0, 0.12),
            inset 1px 0 0 rgba(255, 255, 255, 0.08),
            inset -1px 0 0 rgba(255, 255, 255, 0.08),
            0 24px 80px rgba(0, 0, 0, 0.6),
            0 8px 32px rgba(0, 0, 0, 0.4),
            0 0 0 0.5px rgba(255, 255, 255, 0.1);

        @media (min-width: 768px) {
            display: none;
        }
    }

    .tab-item {
        @apply flex items-center justify-center h-[48px] rounded-[20px] cursor-pointer flex-1 transition-[background] duration-150;
    }

    .tab-item.active {
        @apply w-14 flex-none;
        background: linear-gradient(
            135deg,
            rgba(255, 255, 255, 0.22) 0%,
            rgba(255, 255, 255, 0.16) 100%
        );
        box-shadow:
            inset 0 1px 0 rgba(255, 255, 255, 0.4),
            inset 0 -0.5px 0 rgba(0, 0, 0, 0.1),
            0 4px 12px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
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
