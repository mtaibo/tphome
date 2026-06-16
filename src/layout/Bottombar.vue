<script setup>

    import { computed } from 'vue'
    import { useRouter, useRoute } from 'vue-router'

    import { getSections } from '@/config/sections.js'

    const props = defineProps({ activeSection: { type: String } })
    const emit = defineEmits(['update:activeSection'])

    const router = useRouter()
    const route = useRoute()

    const isDashboard = computed(() => route.path === '/')

    const tabs = computed(() => {
        const sections = getSections(route.path)
        const items = sections.map(({ id, icon }) => ({ id, icon }))

        if (isDashboard.value) {
            items.push({ id: 'settings', icon: null, action: () => router.push('/settings') })
        } else {
            items.push({ id: 'back', icon: null, action: () => router.push('/') })
        }

        return items
    })

    function setActive(item) {
        if (item.action) {
            item.action()
            return
        }
        emit('update:activeSection', item.id)
    }

</script>

<template>

    <nav v-if="isDashboard" class="liquid-bar md:hidden">
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
