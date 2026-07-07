
import { ref, computed } from 'vue'
import { LayoutDashboard, Blinds, Lightbulb, Wand2, Smartphone, Clock, Code, Cpu } from 'lucide-vue-next'

import Blueprint     from '@/layout/dashboard/Blueprint.vue'
import BlindsSection from '@/layout/dashboard/BlindsSection.vue'
import ActiveDevices from '@/layout/settings/ActiveDevices.vue'
import PendingDevices from '@/layout/settings/PendingDevices.vue'
import JsonEditor    from '@/layout/settings/JsonEditor.vue'
import FirmwareManager from '@/layout/settings/FirmwareManager.vue'

const SECTIONS_MAP = {

    "/" : [
        { id: 'blueprint', name: 'Plano',     icon: LayoutDashboard, component: Blueprint },
        { id: 'lights',    name: 'Luces',     icon: Lightbulb,       component: null },
        { id: 'blinds',    name: 'Persianas', icon: Blinds,          component: BlindsSection },
        { id: 'scenes',    name: 'Escenas',   icon: Wand2,           component: null },
    ],

    "/settings" : [
        { id: 'active',   name: 'Dispositivos', icon: Smartphone, component: ActiveDevices },
        { id: 'pending',  name: 'Pendientes',   icon: Clock,      component: PendingDevices },
        { id: 'json',     name: 'JSON',         icon: Code,       component: JsonEditor },
        { id: 'firmware', name: 'Firmware',     icon: Cpu,        component: FirmwareManager },
    ]
}

export function useSections(path) {

    const sections = SECTIONS_MAP[path] || SECTIONS_MAP['/']
    const activeSection = ref(sections[0]?.id || '')
  
    const activeComponent = computed(() => {
        return sections.find(s => s.id === activeSection.value)?.component || null
    })

    return { sections, activeSection, activeComponent }
}
