<script setup>

    import { computed } from 'vue'

    const props = defineProps({
        icon: { type: Object, required: true },
        label: { type: String, required: true },
        active: { type: Boolean, default: false },
        collapsed: { type: Boolean, default: false },
        navItem: { type: Boolean, default: false }
    })

    defineEmits(['click'])

    const buttonClass = computed(() => {

        const base = 'w-full flex items-center py-2.5 rounded-lg transition-[background-color,padding] duration-300 cursor-pointer'
        const padding = props.collapsed ? (props.navItem ? 'px-[10px]' : 'px-[6px]') : 'px-4'

        let stateClass
        if (props.navItem && props.active) stateClass = 'bg-tp-surface text-white font-semibold'
        else if (props.navItem) stateClass = 'text-white/60 bg-transparent hover:bg-white/10 hover:text-white'
        else stateClass = 'text-white/60 bg-transparent hover:text-white'

        return `${base} ${padding} ${stateClass}`
    })

</script>

<template>

    <button
        :class="buttonClass"
        :title="collapsed ? label : ''"
        @click="$emit('click')"
    >
        <component :is="icon" class="w-5 h-5 shrink-0" />

        <span
            class="font-medium text-sm whitespace-nowrap overflow-hidden transition-[width,opacity] duration-300"
            :class="collapsed ? 'w-0 opacity-0' : 'opacity-100 ml-4'"
        >
            {{ label }}
        </span>
    </button>

</template>
