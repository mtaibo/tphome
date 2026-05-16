<script setup>

    import { Settings, RefreshCw } from 'lucide-vue-next'

    import { apiOnline } from '../config/socket'

</script>

<template>

    <footer class="md:hidden fixed bottom-0 left-0 right-0 z-50 h-14 flex items-center justify-between px-6 bg-tp-surface/80 border-t border-tp-border backdrop-blur-md">

        <div :class="apiOnline ? 'is-online' : 'is-offline'" class="flex items-center">
            <div class="status-dot"></div>
        </div>

        <div class="flex items-center gap-5">

            <RouterLink
                to="/settings"
                class="flex items-center justify-center w-8 h-8 rounded-lg text-muted hover:text-white hover:bg-tp-border/20 active:scale-95 transition-all duration-200"
            >
                <Settings class="w-4 h-4" />
            </RouterLink>

            <button
                class="flex items-center justify-center w-8 h-8 rounded-lg text-muted hover:text-tp-accent hover:bg-tp-border/20 active:scale-95 transition-all duration-200"
            >
                <RefreshCw class="w-3.5 h-3.5" />
            </button>

        </div>

    </footer>

</template>
