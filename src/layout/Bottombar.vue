<script setup>

    import { computed } from 'vue'
    import { useRouter, useRoute } from 'vue-router'

    import { LayoutDashboard, Blinds, Lightbulb, Settings, Wand2 } from 'lucide-vue-next'

    const props = defineProps({ activeSection: { type: String } })
    const emit = defineEmits(['update:activeSection'])

    const router = useRouter()
    const route = useRoute()

    const isDashboard = computed(() => route.path === '/')

    const tabs = computed(() => isDashboard.value
        ? [
            { id: 'blueprint', icon: LayoutDashboard },
            { id: 'blinds',    icon: Blinds },
            { id: 'lights',    icon: Lightbulb },
            { id: 'scenes',    icon: Wand2 },
            { id: 'settings',  icon: Settings, action: () => router.push('/settings') },
        ]
        : [
            { id: 'active',    icon: LayoutDashboard },
            { id: 'pending',   icon: Blinds },
            { id: 'json',      icon: Lightbulb },
            { id: 'firmware',  icon: Settings },
            { id: 'back',      icon: Wand2, action: () => router.push('/') },
        ]
    )

    function setActive(item) {
        if (item.action) {
            item.action()
            return
        }
        if (item.id === 'settings') {
            router.push('/settings')
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
