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

    const getButtonClass = (itemId, isCollapsed) => {
        const isActive = activeItem.value === itemId;
        const layoutClass = isCollapsed
            ? 'w-full flex items-center px-[10px] py-2.5 rounded-lg transition-[background-color,padding] duration-200 cursor-pointer'
            : 'w-full flex items-center px-4 py-2.5 rounded-lg transition-[background-color,padding] duration-200 cursor-pointer';
        const activeClass = 'bg-tp-accent/10 text-tp-accent font-semibold';
        const inactiveClass = 'text-muted bg-transparent hover:bg-tp-border/20 hover:text-white';
        return `${layoutClass} ${isActive ? activeClass : inactiveClass}`;
    };

</script>

<template>

    <aside
        class="z-20 hidden md:flex md:flex-col border-r border-tp-border shadow-xl bg-tp-surface transition-all duration-300 ease-in-out"
        :class="collapsed ? 'w-16' : 'w-72'"
    >

        <header class="h-20 px-4 flex items-center gap-4 overflow-hidden">

            <div class="shrink-0">
                <House class="text-tp-accent w-9 h-9" />
            </div>

            <div class="flex flex-col justify-center min-w-0 transition-[width,opacity] duration-200" :class="collapsed ? 'opacity-0 w-0' : 'opacity-100'">
                <h1 class="text-xl font-bold tracking-tight whitespace-nowrap">TPHome</h1>
                <span class="text-[10px] font-mono text-muted/60 tracking-wider whitespace-nowrap">v1.0.0 - stable</span>
            </div>

        </header>


        <nav class="flex-1 p-3 space-y-2">

            <button
                v-for="item in navItems"
                :key="item.id"
                @click="activeItem = item.id"
                :class="getButtonClass(item.id, collapsed)"
                :title="collapsed ? item.name : ''"
            >
                <component :is="item.icon" class="w-5 h-5 shrink-0" />
                <span
                    class="font-medium text-sm whitespace-nowrap overflow-hidden transition-[width,opacity] duration-200"
                    :class="collapsed ? 'w-0 opacity-0' : 'opacity-100 ml-4'"
                >
                    {{ item.name }}
                </span>
            </button>

        </nav>


        <footer class="p-4 border-t border-tp-border space-y-2">

            <button
                @click="toggle"
                class="w-full flex items-center py-2.5 rounded-lg transition-[background-color,padding] duration-200 cursor-pointer text-muted bg-transparent hover:text-white"
                :class="collapsed ? 'px-[6px]' : 'px-4'"
            >
                <component :is="collapsed ? PanelLeftOpen : PanelLeftClose" class="w-5 h-5 shrink-0" />
                <span
                    class="text-sm font-medium whitespace-nowrap overflow-hidden transition-[width,opacity] duration-200"
                    :class="collapsed ? 'w-0 opacity-0' : 'opacity-100 ml-4'"
                >
                    Colapsar
                </span>
            </button>

            <RouterLink
                to="/settings"
                class="w-full flex items-center py-2.5 rounded-lg transition-[background-color,padding] duration-200 cursor-pointer text-muted bg-transparent hover:text-white"
                :class="collapsed ? 'px-[6px]' : 'px-4'"
                :title="collapsed ? 'Configuración' : ''"
            >
                <Settings class="w-5 h-5 shrink-0" />
                <span
                    class="text-sm font-medium whitespace-nowrap overflow-hidden transition-[width,opacity] duration-200"
                    :class="collapsed ? 'w-0 opacity-0' : 'opacity-100 ml-4'"
                >
                    Configuración
                </span>
            </RouterLink>

            <div
                class="flex items-center overflow-hidden transition-all duration-200 rounded-xl"
                :class="collapsed ? 'p-0 border-0 bg-transparent' : 'px-4 py-3 bg-tp-bg/50 border border-tp-border'"
                :title="collapsed ? 'Miguel' : ''"
            >
                <div class="w-8 h-8 rounded-lg bg-tp-border flex items-center justify-center shrink-0">
                    <User class="w-4 h-4 text-tp-accent" />
                </div>
                <div
                    class="flex flex-col text-left whitespace-nowrap overflow-hidden transition-[width,opacity] duration-200"
                    :class="collapsed ? 'w-0 opacity-0' : 'opacity-100 ml-3'"
                >
                    <span class="text-xs font-bold leading-none">Miguel</span>
                    <span class="text-[10px] text-muted italic mt-1">Administrador</span>
                </div>
            </div>

        </footer>

    </aside>

</template>