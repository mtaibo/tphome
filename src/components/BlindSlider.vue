<script setup>

defineProps({
    fillPos:   { type: Number, default: 0 },   // slats fill position (0-100)
    handlePos: { type: Number, default: 0 },   // bubble position (0-100)
})

const emit = defineEmits(['drag-start', 'drag-move', 'drag-end'])

function posFromY(el, clientY) {
    const rect = el.getBoundingClientRect()
    return Math.max(0, Math.min(100, Math.round((1 - (clientY - rect.top) / rect.height) * 100)))
}

function onPointerDown(e) {
    e.currentTarget.setPointerCapture(e.pointerId)
    emit('drag-start', posFromY(e.currentTarget, e.clientY))
}

function onPointerMove(e) {
    if (!e.currentTarget.hasPointerCapture(e.pointerId)) return
    emit('drag-move', posFromY(e.currentTarget, e.clientY))
}

function onPointerUp(e) {
    emit('drag-end', posFromY(e.currentTarget, e.clientY))
}

</script>

<template>
    <div class="blind-track"
         @pointerdown="onPointerDown"
         @pointermove="onPointerMove"
         @pointerup="onPointerUp"
         @pointercancel="onPointerUp">

        <!-- Slats fill from top -->
        <div class="absolute top-0 left-0 right-0 overflow-hidden"
             :class="fillPos < 100 ? 'border-b border-tp-accent/35' : ''"
             :style="{ height: (100 - fillPos) + '%' }">
            <div class="flex flex-col gap-[3px] px-[4px] pt-[4px]">
                <div v-for="i in 32" :key="i"
                     class="w-full bg-white/14 rounded-[2px] shrink-0"
                     style="height: 4px; min-height: 4px;"></div>
            </div>
        </div>

        <!-- Handle pill — clamped so it stays fully visible inside the track -->
        <div class="blind-track-handle transition-none"
             :style="{ top: `clamp(0px, calc(${100 - handlePos}% - 10px), calc(100% - 20px))` }">
        </div>

    </div>
</template>
