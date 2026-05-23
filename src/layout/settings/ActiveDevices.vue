<script setup>

    import { computed } from 'vue'
    import { Lightbulb, Blinds, Trash2, Radio, Info, Upload } from 'lucide-vue-next'

    import { useDevices } from '@/config/devices'
    import { api } from '@/config/api'

    const store = useDevices()

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
                    class="px-4 py-3 rounded-xl bg-tp-surface border border-tp-border hover:border-tp-border/60 transition-colors"
                >
                    <!-- Desktop layout -->
                    <div class="hidden md:flex items-center gap-4">
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
                        <button
                            @click="pingDevice(device.id)"
                            class="flex items-center justify-center w-8 h-8 rounded-lg text-muted hover:text-tp-accent hover:bg-tp-accent/10 transition-all shrink-0 cursor-pointer"
                            title="Ping"
                        >
                            <Radio class="w-4 h-4" />
                        </button>
                        <button
                            @click="getDeviceInfo(device.id)"
                            class="flex items-center justify-center w-8 h-8 rounded-lg text-muted hover:text-blue-400 hover:bg-blue-400/10 transition-all shrink-0 cursor-pointer"
                            title="Get Info"
                        >
                            <Info class="w-4 h-4" />
                        </button>
                        <button
                            @click="sendPrefsDevice(device.id, device.prefs)"
                            class="flex items-center justify-center w-8 h-8 rounded-lg text-muted hover:text-yellow-400 hover:bg-yellow-400/10 transition-all shrink-0 cursor-pointer"
                            title="Send Prefs"
                        >
                            <Upload class="w-4 h-4" />
                        </button>
                        <button
                            @click="deleteDevice(device.id)"
                            class="flex items-center justify-center w-8 h-8 rounded-lg text-muted hover:text-tp-danger hover:bg-tp-danger/10 transition-all shrink-0 cursor-pointer"
                        >
                            <Trash2 class="w-4 h-4" />
                        </button>
                    </div>

                    <!-- Mobile layout -->
                    <div class="flex flex-col gap-2 md:hidden">
                        <div class="flex items-center gap-3">
                            <component
                                :is="device.type === 'Luz' ? Lightbulb : Blinds"
                                class="w-4 h-4 shrink-0"
                                :class="device.type === 'Luz' ? 'text-yellow-400/70' : 'text-tp-accent/70'"
                            />
                            <div class="flex-1 min-w-0">
                                <div class="text-sm text-white truncate">{{ device.name }}</div>
                                <div class="text-xs font-mono text-muted">{{ device.id }}</div>
                            </div>
                            <div
                                class="w-2 h-2 rounded-full shrink-0"
                                :class="device.connection?.online ? 'bg-tp-ok shadow-[0_0_6px_var(--color-tp-ok)]' : 'bg-tp-danger'"
                            ></div>
                        </div>
                        <div class="flex items-center gap-1 ml-7">
                            <button
                                @click="pingDevice(device.id)"
                                class="flex items-center justify-center w-9 h-9 rounded-lg text-muted hover:text-tp-accent hover:bg-tp-accent/10 transition-all cursor-pointer"
                            >
                                <Radio class="w-4 h-4" />
                            </button>
                            <button
                                @click="getDeviceInfo(device.id)"
                                class="flex items-center justify-center w-9 h-9 rounded-lg text-muted hover:text-blue-400 hover:bg-blue-400/10 transition-all cursor-pointer"
                            >
                                <Info class="w-4 h-4" />
                            </button>
                            <button
                                @click="sendPrefsDevice(device.id, device.prefs)"
                                class="flex items-center justify-center w-9 h-9 rounded-lg text-muted hover:text-yellow-400 hover:bg-yellow-400/10 transition-all cursor-pointer"
                            >
                                <Upload class="w-4 h-4" />
                            </button>
                            <button
                                @click="deleteDevice(device.id)"
                                class="flex items-center justify-center w-9 h-9 rounded-lg text-muted hover:text-tp-danger hover:bg-tp-danger/10 transition-all cursor-pointer"
                            >
                                <Trash2 class="w-4 h-4" />
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </section>

    </div>

</template>
