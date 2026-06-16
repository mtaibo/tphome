import { LayoutDashboard, Blinds, Lightbulb, Wand2, Smartphone, Clock, Code, Cpu } from 'lucide-vue-next'

import Blueprint     from '@/layout/dashboard/Blueprint.vue'
import ActiveDevices from '@/layout/settings/ActiveDevices.vue'
import PendingDevices from '@/layout/settings/PendingDevices.vue'
import JsonEditor    from '@/layout/settings/JsonEditor.vue'
import FirmwareManager from '@/layout/settings/FirmwareManager.vue'

export const dashboardSections = [
  { id: 'blueprint', name: 'Plano',     icon: LayoutDashboard, component: Blueprint },
  { id: 'lights',    name: 'Luces',     icon: Lightbulb,       component: null },
  { id: 'blinds',    name: 'Persianas', icon: Blinds,          component: null },
  { id: 'scenes',    name: 'Escenas',   icon: Wand2,           component: null },
]

export const settingsSections = [
  { id: 'active',   name: 'Dispositivos', icon: Smartphone, component: ActiveDevices },
  { id: 'pending',  name: 'Pendientes',   icon: Clock,      component: PendingDevices },
  { id: 'json',     name: 'JSON',         icon: Code,       component: JsonEditor },
  { id: 'firmware', name: 'Firmware',     icon: Cpu,        component: FirmwareManager },
]

export function getSections(path) {
  return path === '/' ? dashboardSections : settingsSections
}

export function getActiveComponent(sections, activeId) {
  return sections.find(s => s.id === activeId)?.component ?? null
}