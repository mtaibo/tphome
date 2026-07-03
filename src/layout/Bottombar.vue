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

    <nav class="liquid-bar md:hidden">
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

    .liquid-bar {
        @apply fixed bottom-8 left-4 right-4 z-50 rounded-[24px] px-1.5 py-1.5 flex items-center justify-between;
        background: rgba(44, 44, 46, 0.52);
        backdrop-filter: blur(30px) saturate(180%);
        -webkit-backdrop-filter: blur(30px) saturate(180%);
        border: 0.5px solid var(--color-tp-border);
        box-shadow:
            inset 0 0.5px 0 rgba(255, 255, 255, 0.1),
            0 12px 40px rgba(0, 0, 0, 0.7);
    }

    .tab-item {
        @apply flex items-center justify-center h-[38px] rounded-[18px] cursor-pointer flex-1 transition-[background] duration-150;
    }

    .tab-item.active {
        @apply w-14 flex-none;
        background: rgba(255, 255, 255, 0.14);
    }

    .tab-item svg {
        @apply w-[22px] h-[22px];
        opacity: 0.6;
        color: #fff;
    }

    .tab-item.active svg {
        opacity: 1;
    }
</style>
