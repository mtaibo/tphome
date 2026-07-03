<script setup>

    import { ref, computed, onMounted, onUnmounted } from 'vue'
    import { useRouter, useRoute } from 'vue-router'

    import { Settings, ArrowLeft } from 'lucide-vue-next'

    const props = defineProps({ activeSection: String, sections: Array })
    const emit = defineEmits(['update:activeSection'])

    const router = useRouter()
    const route = useRoute()

    const navRef = ref(null)
    const hoverIndex = ref(-1)
    const isDragging = ref(false)
    const isPointerDown = ref(false)
    const startX = ref(0)
    const startY = ref(0)

    const tabs = computed(() => [
        ...props.sections,
        route.path === '/'
            ? { id: 'settings', icon: Settings, action: () => router.push('/settings') }
            : { id: 'back', icon: ArrowLeft, action: () => router.push('/') }
    ])

    const visualIndex = computed(() =>
        isDragging.value && hoverIndex.value >= 0
            ? hoverIndex.value
            : tabs.value.findIndex(t => t.id === props.activeSection)
    )

    const bubbleStyle = computed(() => {
        const idx = visualIndex.value
        const nav = navRef.value
        if (idx < 0 || !nav) return { opacity: 0 }

        const button = nav.querySelectorAll('.tab-item')[idx]
        if (!button) return { opacity: 0 }

        const navRect = nav.getBoundingClientRect()
        const btnRect = button.getBoundingClientRect()

        return {
            opacity: isDragging.value ? 0.2 : 1,
            transform: `translateX(${btnRect.left - navRect.left}px) scale(${isDragging.value ? 1.5 : 1})`,
            width: `${btnRect.width}px`,
            height: `${btnRect.height}px`
        }
    })

    function activate(item) {
        if (item.action) item.action()
        else emit('update:activeSection', item.id)
    }

    function getButtonIndex(nav, clientX) {
        const navRect = nav.getBoundingClientRect()
        const x = clientX - navRect.left
        const buttons = nav.querySelectorAll('.tab-item')
        return Array.from(buttons).findIndex(btn => {
            const r = btn.getBoundingClientRect()
            const bx = r.left - navRect.left
            return x >= bx && x < bx + r.width
        })
    }

    function onPointerDown(e) {
        isPointerDown.value = true
        const touch = e.touches?.[0] || e
        startX.value = touch.clientX
        startY.value = touch.clientY
    }

    function onPointerMove(e) {
        if (!navRef.value || !isPointerDown.value) return
        
        const touch = e.touches?.[0] || e
        const clientX = touch.clientX
        const clientY = touch.clientY
        
        const deltaX = Math.abs(clientX - startX.value)
        const deltaY = Math.abs(clientY - startY.value)
        
        if (deltaY > deltaX) return
        
        const index = getButtonIndex(navRef.value, clientX)
        if (index >= 0) {
            hoverIndex.value = index
            isDragging.value = true
        }
    }

    function onPointerEnd() {
        if (isDragging.value && hoverIndex.value >= 0) {
            const item = tabs.value[hoverIndex.value]
            if (item) activate(item)
        }
        isDragging.value = false
        hoverIndex.value = -1
        isPointerDown.value = false
    }

    const listeners = [
        ['mousedown', onPointerDown],
        ['touchstart', onPointerDown, { passive: true }],
        ['mousemove', onPointerMove],
        ['touchmove', onPointerMove, { passive: true }],
        ['mouseup', onPointerEnd],
        ['touchend', onPointerEnd],
        ['touchcancel', onPointerEnd],
        ['mouseleave', onPointerEnd],
    ]

    onMounted(() => {
        if (!navRef.value) return
        listeners.forEach(([event, handler, opts]) =>
            navRef.value.addEventListener(event, handler, opts)
        )
    })

    onUnmounted(() => {
        if (!navRef.value) return
        listeners.forEach(([event, handler, opts]) =>
            navRef.value.removeEventListener(event, handler, opts)
        )
    })

</script>

<template>

    <nav ref="navRef" class="liquid-bar" :class="{ dragging: isDragging }">
        <div class="bubble-indicator" :style="bubbleStyle"></div>
        <button
            v-for="(item, index) in tabs"
            :key="item.id"
            @click="activate(item)"
            class="tab-item"
            :class="{ active: visualIndex === index }"
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
