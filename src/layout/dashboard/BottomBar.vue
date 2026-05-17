<script setup>

    import { ref } from 'vue'
    import { LayoutDashboard, Lightbulb, Blinds, Settings, RefreshCw } from 'lucide-vue-next'

    const activeItem = ref('blueprint')
    const navItems = [
        { id: 'blueprint', name: 'Plano',     icon: LayoutDashboard },
        { id: 'lights',    name: 'Luces',     icon: Lightbulb       },
        { id: 'blinds',    name: 'Persianas', icon: Blinds          },
    ]

</script>

<template>

    <footer class="md:hidden fixed bottom-0 left-0 right-0 z-50 h-18 flex items-center justify-between px-8 pt-2 pb-8 bg-tp-surface border-t border-tp-border">

        <div class="flex items-center gap-4">
            <button
                v-for="item in navItems"
                :key="item.id"
                @click="activeItem = item.id"
                class="flex items-center justify-center w-8 h-8 rounded-lg transition-all duration-200 active:scale-95 cursor-pointer"
                :class="activeItem === item.id
                    ? 'text-tp-accent bg-tp-accent/10'
                    : 'text-muted hover:text-white hover:bg-tp-border/20'"
            >
                <component :is="item.icon" class="w-4 h-4" />
            </button>
        </div>

        <div class="flex items-center gap-4">

            <RouterLink
                to="/settings"
                class="flex items-center justify-center w-8 h-8 rounded-lg transition-all duration-200 active:scale-95"
                :class="activeItem === 'settings'
                    ? 'text-tp-accent bg-tp-accent/10'
                    : 'text-muted hover:text-white hover:bg-tp-border/20'"
            >
                <Settings class="w-4 h-4" />
            </RouterLink>

            <button
                class="flex items-center justify-center w-8 h-8 rounded-lg transition-all duration-200 active:scale-95 cursor-pointer text-muted hover:text-tp-accent hover:bg-tp-border/20"
            >
                <RefreshCw class="w-3.5 h-3.5" />
            </button>

        </div>

    </footer>

</template>
