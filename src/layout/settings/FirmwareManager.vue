<script setup>

    import { ref, onMounted } from 'vue'
    import { Upload, Cpu, Trash2, Check, FileBox, ChevronDown } from 'lucide-vue-next'
    import { api } from '@/config/api'

    const firmwares = ref([])
    const uploading = ref(false)
    const uploadStatus = ref('')
    const expandedId = ref(null)

    const form = ref({
        name: '',
        chip: '',
        target: 'blinds',
        version: '',
        notes: ''
    })

    const selectedFile = ref(null)

    onMounted(loadFirmwares)

    async function loadFirmwares() {
        try {
            firmwares.value = await api.getFirmwares()
        } catch (error) {
            console.error('TPHome - Error loading firmwares:', error)
        }
    }

    function onFileChange(event) {
        const file = event.target.files[0]
        if (file && file.name.endsWith('.bin')) {
            selectedFile.value = file
        } else {
            selectedFile.value = null
        }
    }

    async function handleUpload() {
        if (!selectedFile.value) return
        if (!form.value.name || !form.value.chip || !form.value.version) return

        uploading.value = true
        uploadStatus.value = ''

        try {
            await api.uploadFirmware(selectedFile.value, { ...form.value })
            form.value = { name: '', chip: '', target: 'blinds', version: '', notes: '' }
            selectedFile.value = null
            uploadStatus.value = 'ok'
            await loadFirmwares()
        } catch (error) {
            console.error('TPHome - Upload error:', error)
            uploadStatus.value = 'error'
        } finally {
            uploading.value = false
        }
    }

    async function activate(id) {
        try {
            await api.activateFirmware(id)
            await loadFirmwares()
        } catch (error) {
            console.error('TPHome - Activate error:', error)
        }
    }

    async function remove(id) {
        if (!confirm('¿Eliminar este firmware?')) return
        try {
            await api.deleteFirmware(id)
            if (expandedId.value === id) expandedId.value = null
            await loadFirmwares()
        } catch (error) {
            console.error('TPHome - Delete error:', error)
        }
    }

    function toggleExpanded(id) {
        expandedId.value = expandedId.value === id ? null : id
    }

</script>

<template>

    <div class="h-full flex flex-col p-8 gap-8 overflow-y-auto">

        <!-- Upload section -->
        <section>
            <div class="flex items-center gap-3 mb-5">
                <div class="w-2 h-2 rounded-full bg-tp-accent shadow-[0_0_6px_var(--color-tp-accent)]"></div>
                <h2 class="text-sm font-bold uppercase tracking-widest text-muted">
                    Subir firmware
                </h2>
            </div>

            <div class="rounded-xl bg-tp-surface border border-tp-border p-5 space-y-4">

                <div class="flex items-center gap-3">
                    <label class="flex-1">
                        <span class="block text-xs text-muted mb-1.5">Archivo .bin</span>
                        <input
                            type="file"
                            accept=".bin"
                            @change="onFileChange"
                            class="w-full text-sm text-muted file:mr-3 file:py-1.5 file:px-3 file:rounded-lg file:border-0 file:text-xs file:font-medium file:bg-tp-accent/10 file:text-tp-accent file:cursor-pointer hover:file:bg-tp-accent/20 cursor-pointer"
                        />
                    </label>
                    <div v-if="selectedFile" class="shrink-0 mt-5 text-xs text-tp-ok font-mono">
                        {{ selectedFile.name }}
                    </div>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
                    <div>
                        <label class="block text-xs text-muted mb-1.5">Nombre</label>
                        <input
                            v-model="form.name"
                            type="text"
                            placeholder="Persiana v2.1"
                            class="w-full px-3 py-2 rounded-lg bg-black/20 border border-tp-border text-sm text-tp-text-primary placeholder:text-muted/40 focus:outline-none focus:border-tp-accent/50 transition-colors"
                        />
                    </div>
                    <div>
                        <label class="block text-xs text-muted mb-1.5">Versión</label>
                        <input
                            v-model="form.version"
                            type="text"
                            placeholder="2.1.0"
                            class="w-full px-3 py-2 rounded-lg bg-black/20 border border-tp-border text-sm text-tp-text-primary placeholder:text-muted/40 focus:outline-none focus:border-tp-accent/50 transition-colors"
                        />
                    </div>
                    <div>
                        <label class="block text-xs text-muted mb-1.5">Chip</label>
                        <input
                            v-model="form.chip"
                            type="text"
                            placeholder="BK7231N"
                            class="w-full px-3 py-2 rounded-lg bg-black/20 border border-tp-border text-sm text-tp-text-primary placeholder:text-muted/40 focus:outline-none focus:border-tp-accent/50 transition-colors"
                        />
                    </div>
                    <div>
                        <label class="block text-xs text-muted mb-1.5">Target</label>
                        <select
                            v-model="form.target"
                            class="w-full px-3 py-2 rounded-lg bg-black/20 border border-tp-border text-sm text-tp-text-primary focus:outline-none focus:border-tp-accent/50 transition-colors"
                        >
                            <option value="blinds">Persianas</option>
                            <option value="lights">Luces</option>
                            <option value="switches">Interruptores</option>
                        </select>
                    </div>
                </div>

                <div>
                    <label class="block text-xs text-muted mb-1.5">Notas</label>
                    <textarea
                        v-model="form.notes"
                        placeholder="Changelog o notas..."
                        rows="2"
                        class="w-full px-3 py-2 rounded-lg bg-black/20 border border-tp-border text-sm text-tp-text-primary placeholder:text-muted/40 focus:outline-none focus:border-tp-accent/50 transition-colors resize-none"
                    />
                </div>

                <div class="flex items-center gap-3">
                    <button
                        @click="handleUpload"
                        :disabled="uploading || !selectedFile || !form.name || !form.chip || !form.version"
                        class="flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium bg-tp-accent/10 text-tp-accent hover:bg-tp-accent/20 disabled:opacity-30 disabled:cursor-not-allowed transition-all cursor-pointer"
                    >
                        <Upload class="w-4 h-4" />
                        <span>{{ uploading ? 'Subiendo...' : 'Subir firmware' }}</span>
                    </button>

                    <span v-if="uploadStatus === 'ok'" class="text-xs text-tp-ok">Subido correctamente</span>
                    <span v-if="uploadStatus === 'error'" class="text-xs text-tp-danger">Error al subir</span>
                </div>

            </div>
        </section>

        <!-- Firmware list -->
        <section>
            <div class="flex items-center gap-3 mb-5">
                <div class="w-2 h-2 rounded-full bg-tp-accent shadow-[0_0_6px_var(--color-tp-accent)]"></div>
                <h2 class="text-sm font-bold uppercase tracking-widest text-muted">
                    Firmwares
                    <span class="text-tp-accent font-mono ml-1.5">{{ firmwares.length }}</span>
                </h2>
            </div>

            <div v-if="firmwares.length === 0" class="text-sm text-muted/50 italic px-1">
                No hay firmwares subidos.
            </div>

            <div v-else class="space-y-2">
                <div
                    v-for="fw in firmwares"
                    :key="fw.id"
                    class="rounded-xl bg-tp-surface border border-tp-border hover:border-tp-border/60 transition-colors overflow-hidden"
                    :class="{ 'border-tp-accent/30': fw.active }"
                >
                    <!-- Desktop layout -->
                    <div class="hidden md:block">
                        <div
                            class="flex items-center gap-4 px-4 py-3 cursor-pointer select-none"
                            @click="toggleExpanded(fw.id)"
                        >
                            <Cpu class="w-4 h-4 shrink-0 text-tp-accent/70" />
                            <span class="text-sm text-tp-text-primary flex-1 truncate">{{ fw.name }}</span>
                            <span class="text-xs font-mono text-muted">{{ fw.version }}</span>
                            <span class="text-xs font-mono text-muted hidden lg:block">{{ fw.chip }}</span>

                            <div v-if="fw.active" class="flex items-center gap-1.5 shrink-0">
                                <Check class="w-3.5 h-3.5 text-tp-ok" />
                                <span class="text-xs text-tp-ok font-medium">Activo</span>
                            </div>

                            <ChevronDown
                                class="w-4 h-4 shrink-0 text-muted transition-transform duration-200"
                                :class="{ 'rotate-180': expandedId === fw.id }"
                            />
                        </div>

                        <div
                            class="expand-content"
                            :class="{ 'expand-open': expandedId === fw.id }"
                        >
                            <div class="border-t border-tp-border/50 px-4 py-2 bg-black/10">
                                <div class="px-3 py-2 text-xs text-muted/60 space-y-1">
                                    <div><span class="text-muted">Target:</span> {{ fw.target }}</div>
                                    <div><span class="text-muted">Chip:</span> {{ fw.chip }}</div>
                                    <div><span class="text-muted">Subido:</span> {{ new Date(fw.uploaded_at).toLocaleString() }}</div>
                                    <div v-if="fw.notes"><span class="text-muted">Notas:</span> {{ fw.notes }}</div>
                                </div>

                                <div class="flex items-center gap-2 px-3 pb-2">
                                    <button
                                        v-if="!fw.active"
                                        @click.stop="activate(fw.id)"
                                        class="flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-medium bg-tp-ok/10 text-tp-ok hover:bg-tp-ok/20 transition-all cursor-pointer"
                                    >
                                        <Check class="w-3.5 h-3.5" />
                                        Activar
                                    </button>
                                    <button
                                        @click.stop="remove(fw.id)"
                                        class="flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-medium bg-tp-danger/10 text-tp-danger hover:bg-tp-danger/20 transition-all cursor-pointer"
                                    >
                                        <Trash2 class="w-3.5 h-3.5" />
                                        Eliminar
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Mobile layout -->
                    <div class="md:hidden">
                        <div
                            class="flex items-center gap-3 px-4 py-3 cursor-pointer select-none"
                            @click="toggleExpanded(fw.id)"
                        >
                            <Cpu class="w-4 h-4 shrink-0 text-tp-accent/70" />
                            <span class="text-sm text-tp-text-primary flex-1 truncate min-w-0">{{ fw.name }}</span>
                            <span class="text-xs font-mono text-muted shrink-0 whitespace-nowrap">{{ fw.version }}</span>
                            <div v-if="fw.active" class="shrink-0">
                                <Check class="w-3.5 h-3.5 text-tp-ok" />
                            </div>
                            <ChevronDown
                                class="w-4 h-4 shrink-0 text-muted transition-transform duration-200"
                                :class="{ 'rotate-180': expandedId === fw.id }"
                            />
                        </div>

                        <div
                            class="expand-content"
                            :class="{ 'expand-open': expandedId === fw.id }"
                        >
                            <div class="border-t border-tp-border/50 px-4 py-2 bg-black/10">
                                <div class="px-3 py-2 text-xs text-muted/60 space-y-1">
                                    <div><span class="text-muted">Target:</span> {{ fw.target }}</div>
                                    <div><span class="text-muted">Chip:</span> {{ fw.chip }}</div>
                                    <div><span class="text-muted">Subido:</span> {{ new Date(fw.uploaded_at).toLocaleString() }}</div>
                                    <div v-if="fw.notes"><span class="text-muted">Notas:</span> {{ fw.notes }}</div>
                                </div>

                                <div class="flex items-center gap-2 px-3 pb-2">
                                    <button
                                        v-if="!fw.active"
                                        @click.stop="activate(fw.id)"
                                        class="flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-medium bg-tp-ok/10 text-tp-ok hover:bg-tp-ok/20 transition-all cursor-pointer"
                                    >
                                        <Check class="w-3.5 h-3.5" />
                                        Activar
                                    </button>
                                    <button
                                        @click.stop="remove(fw.id)"
                                        class="flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-medium bg-tp-danger/10 text-tp-danger hover:bg-tp-danger/20 transition-all cursor-pointer"
                                    >
                                        <Trash2 class="w-3.5 h-3.5" />
                                        Eliminar
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>

    </div>

</template>

<style scoped>
    .expand-content {
        max-height: 0;
        overflow: hidden;
        transition: max-height 0.4s ease-out;
    }

    .expand-open {
        max-height: 400px;
    }
</style>
