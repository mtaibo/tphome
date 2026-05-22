<script setup>

    import { computed } from 'vue'
    import { Lightbulb, Blinds, Trash2 } from 'lucide-vue-next'

    import { useDevices } from '@/config/devices'
    import { api } from '@/config/api'

    const store = useDevices()

    const allDevices = computed(() => {
        const lights = Object.entries(store.lights).map(([id, d]) => ({ id, ...d, type: 'Luz', category: 'lights' }))
        const blinds = Object.entries(store.blinds).map(([id, d]) => ({ id, ...d, type: 'Persiana', category: 'blinds' }))
        return [...blinds, ...lights]
    })

    async function deleteDevice(category, id) {
        if (!confirm(`¿Borrar ${id}?`)) return
        try {
            const config = await api.getConfig('devices')
            delete config[category][id]
            await api.postConfig('devices', config)
            await store.setup()
        } catch (error) {
            console.error('TPHome - Error deleting device:', error)
        }
    }

</script>

<template>

    <div class="h-full flex flex-col p-8 gap-8 overflow-y-auto">

        <section>
            <div class="flex items-center gap-3 mb-5">
                <div class="w-2 h-2 rounded-full bg-tp-ok shadow-[0_0_6px_var(--color-tp-ok)]"></div>
                <h2 class="text-sm font-bold uppercase tracking-widest text-muted">
                    Dispositivos
                    <span class="text-tp-accent font-mono ml-1.5">{{ allDevices.length }}</span>
                </h2>
            </div>

            <div v-if="allDevices.length === 0" class="text-sm text-muted/50 italic px-1">
                No hay dispositivos configurados en el mapa.
            </div>

            <div v-else class="space-y-2">
                <div
                    v-for="device in allDevices"
                    :key="device.id"
                    class="flex items-center gap-4 px-4 py-3 rounded-xl bg-tp-surface border border-tp-border hover:border-tp-border/60 transition-colors"
                >
                    <component
                        :is="device.type === 'Luz' ? Lightbulb : Blinds"
                        class="w-4 h-4 shrink-0"
                        :class="device.type === 'Luz' ? 'text-yellow-400/70' : 'text-tp-accent/70'"
                    />
                    <span class="font-mono text-xs text-muted w-16 shrink-0">{{ device.id }}</span>
                    <span class="text-sm text-white flex-1 truncate">{{ device.name }}</span>
                    <span class="text-[10px] font-mono uppercase tracking-wider text-muted/50 w-20 shrink-0">{{ device.type }}</span>
                    <span
                        class="text-[10px] font-mono uppercase tracking-wider w-16 shrink-0 text-center px-2 py-0.5 rounded"
                        :class="device.connection?.online ? 'text-tp-ok bg-tp-ok/10' : 'text-tp-danger bg-tp-danger/10'"
                    >
                        {{ device.connection?.online ? 'Online' : 'Offline' }}
                    </span>
                    <button
                        @click="deleteDevice(device.category, device.id)"
                        class="flex items-center justify-center w-8 h-8 rounded-lg text-muted hover:text-tp-danger hover:bg-tp-danger/10 transition-all shrink-0 cursor-pointer"
                    >
                        <Trash2 class="w-4 h-4" />
                    </button>
                </div>
            </div>
        </section>

    </div>

</template>
