<script setup>

    import { ref, computed, onMounted, onUnmounted } from 'vue'
    import { useRouter, useRoute } from 'vue-router'

    import { Smartphone } from 'lucide-vue-next'

    const props = defineProps({ activeSection: String, sections: Array })
    const emit = defineEmits(['update:activeSection'])

    const router = useRouter()
    const route = useRoute()

    const navRef = ref(null)
    const hoverIndex = ref(-1)
    const isDragging = ref(false)
    const isPointerDown = ref(false)

    const isDashboard = computed(() => route.path === '/')

    const tabs = computed(() => [
        ...props.sections,
        isDashboard.value
            ? { id: 'settings', icon: Smartphone, action: () => router.push('/settings') }
            : { id: 'back', icon: Smartphone, action: () => router.push('/') }
    ])

    const activeIndex = computed(() => {
        return tabs.value.findIndex(t => t.id === props.activeSection)
    })

    const visualActiveIndex = computed(() => {
        if (isDragging.value && hoverIndex.value >= 0) return hoverIndex.value
        return activeIndex.value
    })

    const bubbleStyle = computed(() => {
        if (visualActiveIndex.value < 0 || !navRef.value) return { opacity: 0 }
        
        const buttons = navRef.value.querySelectorAll('.tab-item')
        const button = buttons[visualActiveIndex.value]
        if (!button) return { opacity: 0 }

        const navRect = navRef.value.getBoundingClientRect()
        const buttonRect = button.getBoundingClientRect()

        const scale = isDragging.value ? 'scale(1.5)' : 'scale(1)'
        const opacity = isDragging.value ? 0.2 : 1

        return {
            opacity,
            transform: `translateX(${buttonRect.left - navRect.left}px) ${scale}`,
            width: `${buttonRect.width}px`,
            height: `${buttonRect.height}px`
        }
    })

    function setActive(item) {
        if (item.action) item.action()
        else emit('update:activeSection', item.id)
    }

    function handlePointerDown() {
        isPointerDown.value = true
    }

    function handlePointerMove(e) {
        if (!navRef.value || !isPointerDown.value) return
        
        const touch = e.touches?.[0] || e
        const navRect = navRef.value.getBoundingClientRect()
        const x = touch.clientX - navRect.left

        const buttons = navRef.value.querySelectorAll('.tab-item')
        let index = -1
        
        for (let i = 0; i < buttons.length; i++) {
            const rect = buttons[i].getBoundingClientRect()
            const buttonX = rect.left - navRect.left
            if (x >= buttonX && x < buttonX + rect.width) {
                index = i
                break
            }
        }

        if (index >= 0) {
            hoverIndex.value = index
            isDragging.value = true
        }
    }

    function handlePointerEnd() {
        if (isDragging.value && hoverIndex.value >= 0) {
            const item = tabs.value[hoverIndex.value]
            if (item && !item.action) {
                emit('update:activeSection', item.id)
            }
        }
        isDragging.value = false
        hoverIndex.value = -1
        isPointerDown.value = false
    }

    onMounted(() => {
        if (navRef.value) {
            navRef.value.addEventListener('mousedown', handlePointerDown)
            navRef.value.addEventListener('touchstart', handlePointerDown, { passive: true })
            navRef.value.addEventListener('mousemove', handlePointerMove)
            navRef.value.addEventListener('touchmove', handlePointerMove, { passive: true })
            navRef.value.addEventListener('mouseup', handlePointerEnd)
            navRef.value.addEventListener('touchend', handlePointerEnd)
            navRef.value.addEventListener('touchcancel', handlePointerEnd)
            navRef.value.addEventListener('mouseleave', handlePointerEnd)
        }
    })

    onUnmounted(() => {
        if (navRef.value) {
            navRef.value.removeEventListener('mousedown', handlePointerDown)
            navRef.value.removeEventListener('touchstart', handlePointerDown)
            navRef.value.removeEventListener('mousemove', handlePointerMove)
            navRef.value.removeEventListener('touchmove', handlePointerMove)
            navRef.value.removeEventListener('mouseup', handlePointerEnd)
            navRef.value.removeEventListener('touchend', handlePointerEnd)
            navRef.value.removeEventListener('touchcancel', handlePointerEnd)
            navRef.value.removeEventListener('mouseleave', handlePointerEnd)
        }
    })

</script>

<template>

    <nav ref="navRef" class="liquid-bar" :class="{ dragging: isDragging }">
        <div class="bubble-indicator" :style="bubbleStyle"></div>
        <button
            v-for="(item, index) in tabs"
            :key="item.id"
            @click="setActive(item)"
            class="tab-item"
            :class="{ active: visualActiveIndex === index && item.id !== 'settings' }"
        >
            <component :is="item.icon" />
        </button>
    </nav>

</template>

<style scoped>
@reference "tailwindcss";

    .liquid-bar {
        @apply fixed bottom-6 left-4 right-4 z-50 rounded-[32px] px-1.5 py-1.5 flex items-center justify-between;
        position: fixed;
        background: linear-gradient(
            135deg,
            rgba(255, 255, 255, 0.1) 0%,
            rgba(255, 255, 255, 0.05) 50%,
            rgba(255, 255, 255, 0.08) 100%
        );
        backdrop-filter: blur(60px) saturate(240%);
        -webkit-backdrop-filter: blur(60px) saturate(240%);
        border: 0.5px solid rgba(255, 255, 255, 0.25);
        box-shadow:
            inset 0 2px 0 rgba(255, 255, 255, 0.4),
            inset 0 -1px 0 rgba(0, 0, 0, 0.15),
            inset 1px 0 0 rgba(255, 255, 255, 0.12),
            inset -1px 0 0 rgba(255, 255, 255, 0.12),
            0 30px 90px rgba(0, 0, 0, 0.65),
            0 12px 40px rgba(0, 0, 0, 0.45),
            0 0 0 0.5px rgba(255, 255, 255, 0.15);
        transition: padding 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);

        @media (min-width: 768px) {
            display: none;
        }
    }

    .liquid-bar.dragging {
        padding-top: 7px;
        padding-bottom: 7px;
    }

    .bubble-indicator {
        position: absolute;
        top: 6px;
        left: 0;
        border-radius: 26px;
        background: linear-gradient(
            135deg,
            rgba(255, 255, 255, 0.28) 0%,
            rgba(255, 255, 255, 0.2) 100%
        );
        box-shadow:
            inset 0 1.5px 0 rgba(255, 255, 255, 0.5),
            inset 0 -0.5px 0 rgba(0, 0, 0, 0.12),
            0 6px 16px rgba(0, 0, 0, 0.35),
            0 0 0 0.5px rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
        pointer-events: none;
        z-index: 1;
    }

    .tab-item {
        @apply flex items-center justify-center h-[52px] rounded-[26px] cursor-pointer flex-1 transition-all duration-200;
        position: relative;
        z-index: 2;
    }

    .tab-item svg {
        @apply w-[24px] h-[24px];
        opacity: 0.5;
        color: #fff;
        filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.3));
        transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
    }

    .tab-item.active svg {
        opacity: 1;
        filter: drop-shadow(0 0 10px rgba(255, 255, 255, 0.5));
        transform: scale(1.05);
    }
</style>
