<script setup>

    import { ref, computed } from 'vue'
    import { Lightbulb, Blinds, Trash2, Radio, Info, Braces, ChevronDown } from 'lucide-vue-next'

    import { useDevices } from '@/config/devices'
    import { api } from '@/config/api'

    const store = useDevices()

    const expandedId = ref(null)

    function toggleExpanded(id) {
        expandedId.value = expandedId.value === id ? null : id
    }

    const allDevices = computed(() => {
        const lights = Object.entries(store.lights).map(([id, d]) => ({ id, ...d, type: 'Luz', category: 'lights' }))
        const blinds = Object.entries(store.blinds).map(([id, d]) => ({ id, ...d, type: 'Persiana', category: 'blinds' }))
        return [...blinds, ...lights]
    })

    async function pingDevice(id) {
        try { await api.sendCommand(id, 'ping') }
        catch (error) { console.error('TPHome - Ping error:', error) }
    }

    async function getDeviceInfo(id) {
        try { await api.getDeviceInfo(id) }
        catch (error) { console.error('TPHome - Info error:', error) }
    }

    async function sendPrefsDevice(id, prefs) {
        try { await api.sendPrefs(id, prefs) }
        catch (error) { console.error('TPHome - Prefs error:', error) }
    }

    async function deleteDevice(id) {
        if (!confirm(`¿Borrar ${id}?`)) return
        try {
            await api.deleteDevice(id)
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
                    class="rounded-xl bg-tp-surface border border-tp-border hover:border-tp-border/60 transition-colors overflow-hidden"
                >
                    <!-- Desktop layout -->
                    <div class="hidden md:block">
                        <!-- Main row (clickable) -->
                        <div
                            class="flex items-center gap-4 px-4 py-3 cursor-pointer select-none"
                            @click="toggleExpanded(device.id)"
                        >
                            <component
                                :is="device.type === 'Luz' ? Lightbulb : Blinds"
                                class="w-4 h-4 shrink-0"
                                :class="device.type === 'Luz' ? 'text-yellow-400/70' : 'text-tp-accent/70'"
                            />
                            <span class="font-mono text-xs text-muted w-16 shrink-0">{{ device.id }}</span>
                            <span class="text-sm text-white flex-1 truncate">{{ device.name }}</span>
                            <span
                                class="text-[10px] font-mono uppercase tracking-wider w-16 shrink-0 text-center px-2 py-0.5 rounded"
                                :class="device.connection?.online ? 'text-tp-ok bg-tp-ok/10' : 'text-tp-danger bg-tp-danger/10'"
                            >
                                {{ device.connection?.online ? 'Online' : 'Offline' }}
                            </span>
                            <ChevronDown
                                class="w-4 h-4 shrink-0 text-muted transition-transform duration-200"
                                :class="{ 'rotate-180': expandedId === device.id }"
                            />
                        </div>

                        <!-- Expanded actions -->
                        <div
                            v-show="expandedId === device.id"
                            class="border-t border-tp-border/50 px-4 py-2 bg-black/10"
                        >
                            <button
                                @click.stop="pingDevice(device.id)"
                                class="flex items-center gap-3 w-full px-3 py-2 rounded-lg text-sm text-muted hover:text-tp-accent hover:bg-tp-accent/10 transition-all cursor-pointer"
                            >
                                <Radio class="w-4 h-4 shrink-0" />
                                <span>Ping</span>
                            </button>
                            <button
                                @click.stop="sendPrefsDevice(device.id, device.prefs)"
                                class="flex items-center gap-3 w-full px-3 py-2 rounded-lg text-sm text-muted hover:text-yellow-400 hover:bg-yellow-400/10 transition-all cursor-pointer"
                            >
                                <Braces class="w-4 h-4 shrink-0" />
                                <span>Mandar preferencias</span>
                            </button>
                            <button
                                @click.stop="getDeviceInfo(device.id)"
                                class="flex items-center gap-3 w-full px-3 py-2 rounded-lg text-sm text-muted hover:text-blue-400 hover:bg-blue-400/10 transition-all cursor-pointer"
                            >
                                <Info class="w-4 h-4 shrink-0" />
                                <span>Actualizar información</span>
                            </button>
                            <button
                                @click.stop="deleteDevice(device.id)"
                                class="flex items-center gap-3 w-full px-3 py-2 rounded-lg text-sm text-muted hover:text-tp-danger hover:bg-tp-danger/10 transition-all cursor-pointer"
                            >
                                <Trash2 class="w-4 h-4 shrink-0" />
                                <span>Eliminar dispositivo</span>
                            </button>
                        </div>
                    </div>

                    <!-- Mobile layout -->
                    <div class="md:hidden">
                        <!-- Main row (clickable) -->
                        <div
                            class="flex items-center gap-3 px-4 py-3 cursor-pointer select-none"
                            @click="toggleExpanded(device.id)"
                        >
                            <component
                                :is="device.type === 'Luz' ? Lightbulb : Blinds"
                                class="w-4 h-4 shrink-0"
                                :class="device.type === 'Luz' ? 'text-yellow-400/70' : 'text-tp-accent/70'"
                            />
                            <span class="text-sm text-white flex-1 truncate">{{ device.name }}</span>
                            <span class="text-xs font-mono text-muted shrink-0">{{ device.id }}</span>
                            <div
                                class="w-2 h-2 rounded-full shrink-0"
                                :class="device.connection?.online ? 'bg-tp-ok shadow-[0_0_6px_var(--color-tp-ok)]' : 'bg-tp-danger'"
                            ></div>
                            <ChevronDown
                                class="w-4 h-4 shrink-0 text-muted transition-transform duration-200"
                                :class="{ 'rotate-180': expandedId === device.id }"
                            />
                        </div>

                        <!-- Expanded actions -->
                        <div
                            v-show="expandedId === device.id"
                            class="border-t border-tp-border/50 px-4 py-2 bg-black/10"
                        >
                            <button
                                @click.stop="pingDevice(device.id)"
                                class="flex items-center gap-3 w-full px-3 py-2 rounded-lg text-sm text-muted hover:text-tp-accent hover:bg-tp-accent/10 transition-all cursor-pointer"
                            >
                                <Radio class="w-4 h-4 shrink-0" />
                                <span>Ping</span>
                            </button>
                            <button
                                @click.stop="sendPrefsDevice(device.id, device.prefs)"
                                class="flex items-center gap-3 w-full px-3 py-2 rounded-lg text-sm text-muted hover:text-yellow-400 hover:bg-yellow-400/10 transition-all cursor-pointer"
                            >
                                <Braces class="w-4 h-4 shrink-0" />
                                <span>Mandar preferencias</span>
                            </button>
                            <button
                                @click.stop="getDeviceInfo(device.id)"
                                class="flex items-center gap-3 w-full px-3 py-2 rounded-lg text-sm text-muted hover:text-blue-400 hover:bg-blue-400/10 transition-all cursor-pointer"
                            >
                                <Info class="w-4 h-4 shrink-0" />
                                <span>Actualizar información</span>
                            </button>
                            <button
                                @click.stop="deleteDevice(device.id)"
                                class="flex items-center gap-3 w-full px-3 py-2 rounded-lg text-sm text-muted hover:text-tp-danger hover:bg-tp-danger/10 transition-all cursor-pointer"
                            >
                                <Trash2 class="w-4 h-4 shrink-0" />
                                <span>Eliminar dispositivo</span>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </section>

    </div>

</template>
