<script setup>

    import { ref } from 'vue';
    import { LayoutDashboard, Blinds, Lightbulb, Settings, House, User } from 'lucide-vue-next';

    const activeItem = ref('blueprint');
    const navItems = [
        { id: 'blueprint', name: 'Plano',         icon: LayoutDashboard },
        { id: 'lights',    name: 'Luces',         icon: Lightbulb       },
        { id: 'blinds',    name: 'Persianas',     icon: Blinds          },
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

    <aside class="z-20 w-72 flex flex-col border-r border-tp-border shadow-xl bg-tp-surface">

        <header class="h-20 px-6 pt-1.5 flex items-center gap-4">

            <div class="shrink-0">
                <House class="text-tp-accent w-9 h-9" />
            </div>

            <div class="flex flex-col justify-center">
                <h1 class="text-xl font-bold tracking-tight"> TPHome </h1>
                <span class="text-[10px] font-mono text-muted/60 tracking-wider"> v1.0.0 - stable </span>
            </div>

        </header>


        <nav class="flex-1 p-3 space-y-2">

            <button 
                v-for="item in navItems" 
                :key="item.id"
                @click="activeItem = item.id"
                :class="getButtonClass(item.id)"
            >
                <component :is="item.icon" class="w-5 h-5" />
                <span class="font-medium text-sm">{{ item.name }}</span>
            </button>

        </nav>


        <footer class="p-4 border-t border-tp-border space-y-2">

            <button class="w-full flex items-center gap-4 px-4 py-2.5 rounded-lg transition-colors duration-200 cursor-pointer text-muted hover:text-white">

                <Settings class="w-5 h-5" />
                <span class="text-sm font-medium">Configuración</span>

            </button>

            <div class="flex items-center gap-3 px-4 py-3 bg-tp-bg/50 rounded-xl border border-tp-border">
            
                <div class="w-8 h-8 rounded-lg bg-tp-border flex items-center justify-center">
                    <User class="w-4 h-4 text-tp-accent" />
                </div>

                <div class="flex flex-col text-left">
                    <span class="text-xs font-bold leading-none">Miguel</span>
                    <span class="text-[10px] text-muted italic mt-1">Administrador</span>
                </div>

            </div>

        </footer>

    </aside>

</template>