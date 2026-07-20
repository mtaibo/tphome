<script setup>

    import { ref, onMounted } from 'vue'
    import { Upload, Cpu, Trash2, Check, ChevronDown } from 'lucide-vue-next'
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
        selectedFile.value = (file && file.name.endsWith('.bin')) ? file : null
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

    <div class="h-full flex flex-col overflow-y-auto px-8 pt-6 pb-24 gap-8">

        <!-- Upload section -->
        <section>
            <p class="text-base font-semibold text-white px-1 pb-3">Subir firmware</p>

            <div class="rounded-2xl overflow-hidden bg-[#111113] form-list mb-3">

                <div class="px-4 py-3">
                    <label class="flex items-center gap-4 cursor-pointer">
                        <span class="text-sm text-tp-text flex-1">Archivo .bin</span>
                        <span class="text-xs font-mono text-tp-muted truncate max-w-[140px]">
                            {{ selectedFile ? selectedFile.name : 'Ninguno' }}
                        </span>
                        <span class="text-xs text-tp-accent bg-tp-accent/10 px-2.5 py-1 rounded-lg shrink-0">Elegir</span>
                        <input type="file" accept=".bin" @change="onFileChange" class="hidden" />
                    </label>
                </div>

                <div class="flex items-center gap-4 px-4 py-3">
                    <span class="text-sm text-tp-text flex-1">Nombre</span>
                    <input v-model="form.name" type="text" placeholder="Persiana v2.1" class="form-input w-40" />
                </div>

                <div class="flex items-center gap-4 px-4 py-3">
                    <span class="text-sm text-tp-text flex-1">Versión</span>
                    <input v-model="form.version" type="text" placeholder="2.1.0" class="form-input w-20" />
                </div>

                <div class="flex items-center gap-4 px-4 py-3">
                    <span class="text-sm text-tp-text flex-1">Chip</span>
                    <input v-model="form.chip" type="text" placeholder="BK7231N" class="form-input w-24" />
                </div>

                <div class="flex items-center gap-4 px-4 py-3">
                    <span class="text-sm text-tp-text flex-1">Target</span>
                    <select v-model="form.target" class="form-input form-select w-32">
                        <option value="blinds">Persianas</option>
                        <option value="lights">Luces</option>
                        <option value="switches">Interruptores</option>
                    </select>
                </div>

                <div class="px-4 py-3">
                    <p class="text-sm text-tp-muted mb-2">Notas</p>
                    <textarea
                        v-model="form.notes"
                        placeholder="Changelog o notas..."
                        rows="2"
                        class="w-full bg-transparent text-sm text-tp-text placeholder:text-tp-muted/40 resize-none outline-none"
                    />
                </div>

            </div>

            <div class="flex items-center gap-3">
                <button
                    @click="handleUpload"
                    :disabled="uploading || !selectedFile || !form.name || !form.chip || !form.version"
                    class="action-primary disabled:opacity-30 disabled:cursor-not-allowed"
                >
                    <Upload class="w-4 h-4 shrink-0" />
                    <span>{{ uploading ? 'Subiendo...' : 'Subir firmware' }}</span>
                </button>
                <span v-if="uploadStatus === 'ok'" class="text-xs text-tp-on">Subido correctamente</span>
                <span v-if="uploadStatus === 'error'" class="text-xs text-tp-off">Error al subir</span>
            </div>
        </section>

        <!-- Firmware list -->
        <section>
            <p class="text-base font-semibold text-white px-1 pb-3">
                Firmwares
                <span class="text-tp-accent font-mono ml-1.5">{{ firmwares.length }}</span>
            </p>

            <div v-if="firmwares.length === 0" class="text-sm text-tp-muted/50 italic px-1">
                No hay firmwares subidos.
            </div>

            <div v-else class="rounded-2xl overflow-hidden bg-[#111113] firmware-list">
                <div
                    v-for="fw in firmwares"
                    :key="fw.id"
                    class="firmware-item"
                    :class="{ 'bg-tp-accent/5': fw.active }"
                >
                    <div
                        class="flex items-center gap-4 px-4 py-3 cursor-pointer select-none"
                        @click="toggleExpanded(fw.id)"
                    >
                        <Cpu class="w-4 h-4 shrink-0 text-tp-accent/70" />
                        <div class="flex-1 min-w-0">
                            <p class="text-sm text-tp-text truncate">{{ fw.name }}</p>
                            <p class="text-xs font-mono text-tp-muted">v{{ fw.version }} · {{ fw.chip }}</p>
                        </div>
                        <span v-if="fw.active" class="text-xs text-tp-on font-mono uppercase tracking-wider shrink-0">Activo</span>
                        <ChevronDown
                            class="w-4 h-4 shrink-0 text-tp-muted transition-transform duration-200"
                            :class="{ 'rotate-180': expandedId === fw.id }"
                        />
                    </div>

                    <div class="expand-content" :class="{ 'expand-open': expandedId === fw.id }">
                        <div class="px-4 pb-2 space-y-1">
                            <p class="text-xs text-tp-muted/60"><span class="text-tp-muted">Target:</span> {{ fw.target }}</p>
                            <p class="text-xs text-tp-muted/60"><span class="text-tp-muted">Subido:</span> {{ new Date(fw.uploaded_at).toLocaleString() }}</p>
                            <p v-if="fw.notes" class="text-xs text-tp-muted/60"><span class="text-tp-muted">Notas:</span> {{ fw.notes }}</p>
                        </div>
                        <div class="flex items-center gap-2 px-4 pb-3">
                            <button
                                v-if="!fw.active"
                                @click.stop="activate(fw.id)"
                                class="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium bg-tp-on/10 text-tp-on hover:bg-tp-on/20 transition-all cursor-pointer"
                            >
                                <Check class="w-3.5 h-3.5" />Activar
                            </button>
                            <button
                                @click.stop="remove(fw.id)"
                                class="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium bg-tp-off/10 text-tp-off hover:bg-tp-off/20 transition-all cursor-pointer"
                            >
                                <Trash2 class="w-3.5 h-3.5" />Eliminar
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </section>

    </div>

</template>

<style scoped>
    .form-list > div,
    .firmware-list .firmware-item {
        position: relative;
    }
    .form-list > div + div::before,
    .firmware-list .firmware-item + .firmware-item::before {
        content: '';
        position: absolute;
        top: 0;
        left: 16px;
        right: 16px;
        height: 0.5px;
        background: rgba(255, 255, 255, 0.06);
        pointer-events: none;
    }

    .form-input {
        background: rgba(255, 255, 255, 0.06);
        border: 0.5px solid rgba(255, 255, 255, 0.12);
        border-radius: 8px;
        padding: 5px 10px;
        font-size: 0.8125rem;
        font-family: inherit;
        color: var(--color-tp-text);
        text-align: right;
        outline: none;
        transition: border-color 0.15s ease;
    }
    .form-input::placeholder {
        color: color-mix(in srgb, var(--color-tp-muted) 40%, transparent);
    }
    .form-input:focus {
        border-color: color-mix(in srgb, var(--color-tp-accent) 50%, transparent);
    }

    .form-select {
        appearance: none;
        -webkit-appearance: none;
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%236b7280' stroke-width='2'%3E%3Cpath d='M6 9l6 6 6-6'/%3E%3C/svg%3E");
        background-repeat: no-repeat;
        background-position: right 8px center;
        padding-right: 24px;
        cursor: default;
    }
    .form-select option {
        background: #111113;
    }

    .action-primary {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 10px 18px;
        border-radius: 14px;
        background: linear-gradient(
            145deg,
            rgba(255, 255, 255, 0.14) 0%,
            rgba(255, 255, 255, 0.07) 50%,
            rgba(255, 255, 255, 0.10) 100%
        );
        backdrop-filter: blur(24px) saturate(200%);
        -webkit-backdrop-filter: blur(24px) saturate(200%);
        border: 0.5px solid rgba(255, 255, 255, 0.22);
        box-shadow:
            inset 0 1px 0 rgba(255, 255, 255, 0.36),
            inset 0 -0.5px 0 rgba(0, 0, 0, 0.18),
            0 4px 12px rgba(0, 0, 0, 0.24),
            0 1px 3px rgba(0, 0, 0, 0.14);
        color: var(--color-tp-text);
        font-size: 0.875rem;
        font-weight: 500;
        cursor: default;
        transition: background 0.18s ease, box-shadow 0.18s ease;
    }
    .action-primary:hover:not(:disabled) {
        background: linear-gradient(
            145deg,
            rgba(255, 255, 255, 0.20) 0%,
            rgba(255, 255, 255, 0.11) 50%,
            rgba(255, 255, 255, 0.16) 100%
        );
        box-shadow:
            inset 0 1px 0 rgba(255, 255, 255, 0.42),
            inset 0 -0.5px 0 rgba(0, 0, 0, 0.18),
            0 6px 18px rgba(0, 0, 0, 0.30),
            0 1px 3px rgba(0, 0, 0, 0.14);
    }

    .expand-content {
        max-height: 0;
        overflow: hidden;
        transition: max-height 0.4s ease-out;
    }
    .expand-open {
        max-height: 200px;
    }
</style>
