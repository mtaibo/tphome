<script setup>

    import { ref } from 'vue';
    import { LayoutDashboard, Blinds, Lightbulb, Settings, House, User, PanelLeftClose, PanelLeftOpen } from 'lucide-vue-next';

    const collapsed = ref(localStorage.getItem('sidebar-collapsed') !== 'false')

    const toggle = () => {
        collapsed.value = !collapsed.value
        localStorage.setItem('sidebar-collapsed', collapsed.value)
    }

    const activeItem = ref('blueprint');
    const navItems = [
        { id: 'blueprint', name: 'Plano',     icon: LayoutDashboard },
        { id: 'lights',    name: 'Luces',     icon: Lightbulb       },
        { id: 'blinds',    name: 'Persianas', icon: Blinds          },
    ]

    const getButtonClass = (itemId) => {
        const isActive = activeItem.value === itemId;
        const baseClass = 'w-full flex items-center gap-4 px-4 py-2.5 rounded-lg transition-colors duration-200 cursor-pointer';
        const activeClass = 'bg-tp-accent/10 text-tp-accent font-semibold';
        const inactiveClass = 'text-muted hover:bg-tp-border/20 hover:text-white';
        return `${baseClass} ${isActive ? activeClass : inactiveClass}`;
    };

</script>

<template>

    <aside
        class="z-20 flex flex-col border-r border-tp-border shadow-xl bg-tp-surface transition-all duration-300 ease-in-out"
        :class="collapsed ? 'w-16' : 'w-72'"
    >

        <header class="h-20 px-4 flex items-center gap-4 overflow-hidden">

            <div class="shrink-0">
                <House class="text-tp-accent w-9 h-9" />
            </div>

            <div class="flex flex-col justify-center min-w-0 transition-all duration-300" :class="collapsed ? 'opacity-0 w-0' : 'opacity-100'">
                <h1 class="text-xl font-bold tracking-tight whitespace-nowrap">TPHome</h1>
                <span class="text-[10px] font-mono text-muted/60 tracking-wider whitespace-nowrap">v1.0.0 - stable</span>
            </div>

        </header>


        <nav class="flex-1 p-3 space-y-2">

            <button
                v-for="item in navItems"
                :key="item.id"
                @click="activeItem = item.id"
                :class="getButtonClass(item.id)"
                :title="collapsed ? item.name : ''"
            >
                <component :is="item.icon" class="w-5 h-5 shrink-0" />
                <span
                    class="font-medium text-sm whitespace-nowrap overflow-hidden transition-all duration-300"
                    :class="collapsed ? 'w-0 opacity-0' : 'opacity-100'"
                >
                    {{ item.name }}
                </span>
            </button>

        </nav>


        <footer class="p-4 border-t border-tp-border space-y-2">

            <button
                class="w-full flex items-center gap-4 px-4 py-2.5 rounded-lg transition-colors duration-200 cursor-pointer text-muted hover:text-white"
                :title="collapsed ? 'Configuración' : ''"
            >
                <Settings class="w-5 h-5 shrink-0" />
                <span
                    class="text-sm font-medium whitespace-nowrap overflow-hidden transition-all duration-300"
                    :class="collapsed ? 'w-0 opacity-0' : 'opacity-100'"
                >
                    Configuración
                </span>
            </button>

            <div
                class="flex items-center gap-3 px-4 py-3 bg-tp-bg/50 rounded-xl border border-tp-border overflow-hidden"
                :title="collapsed ? 'Miguel' : ''"
            >
                <div class="w-8 h-8 rounded-lg bg-tp-border flex items-center justify-center shrink-0">
                    <User class="w-4 h-4 text-tp-accent" />
                </div>
                <div
                    class="flex flex-col text-left whitespace-nowrap overflow-hidden transition-all duration-300"
                    :class="collapsed ? 'w-0 opacity-0' : 'opacity-100'"
                >
                    <span class="text-xs font-bold leading-none">Miguel</span>
                    <span class="text-[10px] text-muted italic mt-1">Administrador</span>
                </div>
            </div>

            <!-- Toggle -->

            <button
                @click="toggle"
                class="w-full flex items-center gap-4 px-4 py-2.5 rounded-lg transition-colors duration-200 cursor-pointer text-muted hover:text-white"
            >
                <component :is="collapsed ? PanelLeftOpen : PanelLeftClose" class="w-5 h-5 shrink-0" />
                <span
                    class="text-sm font-medium whitespace-nowrap overflow-hidden transition-all duration-300"
                    :class="collapsed ? 'w-0 opacity-0' : 'opacity-100'"
                >
                    Colapsar
                </span>
            </button>

        </footer>

    </aside>

</template>