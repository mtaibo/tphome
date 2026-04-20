<script setup>
    import { ref } from 'vue'

    const devices = ref([

        { id: 'L0101', name: 'Luz Grande Salón',   x: 110, y: 270, type: 'L' },
        { id: 'L0102', name: 'Luz Pequeña Salón',  x: 75,  y: 340, type: 'L' },

        { id: 'L0201', name: 'Luz Habitación Gemelas',            x: 200, y: 320, type: 'L' },

        { id: 'L0301', name: 'Luz Habitación Ordenador Cama',     x: 280, y: 280, type: 'L' },
        { id: 'L0302', name: 'Luz Habitación Ordenador Armario',  x: 315, y: 330, type: 'L' },

        { id: 'L0401', name: 'Luz Habitación Principal Cama',     x: 420, y: 340, type: 'L' },
        { id: 'L0402', name: 'Luz Habitación Principal Armario',  x: 375, y: 240, type: 'L' },

        { id: 'L0501', name: 'Luz Entrada',   x: 30, y: 125, type: 'L' },
        { id: 'L0502', name: 'Luz Pasillo',   x: 160, y: 211, type: 'L' },
        { id: 'L0503', name: 'Luz Exterior',  x: 30, y: 25, type: 'L' },

        { id: 'L0601', name: 'Luz Baño Invitados',  x: 228, y: 140, type: 'L' },
        { id: 'L0701', name: 'Luz Baño Principal',  x: 445, y: 240, type: 'L' },

        { id: 'L0801', name: 'Luz Cocina',     x: 125, y: 125, type: 'L' },
        { id: 'L0802', name: 'Luz Tendedero',  x: 90, y: 25, type: 'L' },

    ])

    const deviceStates = ref({

        'L0101': { status: 'on' },
        'L0102': { status: 'off' },

        'L0201': { status: 'off' },

        'L0301': { status: 'off' },
        'L0302': { status: 'off' },

        'L0401': { status: 'off' },
        'L0402': { status: 'off' },

        'L0501': { status: 'off' },
        'L0502': { status: 'off' },
        'L0503': { status: 'off' },

        'L0601': { status: 'off' },
        'L0701': { status: 'off' },

        'L0801': { status: 'off' },
        'L0802': { status: 'off' },
    })

    const toggleDevice = (id) => {
        if (deviceStates.value[id]) {
            deviceStates.value[id].status = deviceStates.value[id].status === 'on' ? 'off' : 'on'
        }
    }

</script>

<template>

    <div class="w-full h-full flex items-center justify-center p-8">

        <svg 
            viewBox="0 0 500 450" 
            class="w-full h-auto max-w-2xl"
            xmlns="http://www.w3.org/2000/svg"
        >

            <!-- Rooms -->
            <g class="fill-tp-surface/30 stroke-tp-border stroke-2">

                <rect x="0"  y="50" width="60"  height="190" /> <!-- Entrada                      -->
                <rect x="60"  y="180" width="290" height="60"  /> <!-- Pasillo                      -->
                <rect x="350" y="180" width="50"  height="220" /> <!-- Pasillo Habitación Principal -->

                <rect x="60" y="0"  width="60"  height="50"  />  <!-- Tendedero -->
                <rect x="60" y="50" width="130" height="130" />  <!-- Cocina    -->

                <rect x="0" y="240" width="150" height="160" />  <!-- Salón -->
                <rect x="0" y="400" width="80" height="30" />  <!-- Galería -->

                <rect x="190" y="80" width="75" height="100" />  <!-- Baño Invitados -->
                <rect x="400" y="180" width="90" height="100" />  <!-- Baño Principal -->

                <rect x="150" y="240" width="100" height="160" />  <!-- Habitación Gemelas   -->
                <rect x="250" y="240" width="100" height="160" />  <!-- Habitación Ordenador -->
                <rect x="400" y="280" width="90"  height="120" />  <!-- Habitación Principal -->

            </g>

            <!-- Names -->
            <g class="fill-muted font-mono text-[11px] uppercase tracking-widest pointer-events-none">

                <text x="210" y="214" text-anchor="middle">Pasillo</text>

                <text x="125" y="105" text-anchor="middle">Cocina</text>

                <text x="45" y="290" text-anchor="middle">Salón</text>

                <text x="227" y="120" text-anchor="middle">Baño</text> <!-- Secundario -->
                <text x="445" y="220" text-anchor="middle">Baño</text> <!-- Principal  -->

                <text x="200" y="290" text-anchor="middle">Hab.</text> <!-- Gemelas -->
                <text x="320" y="290" text-anchor="middle">Hab.</text> <!-- Ordenador -->
                <text x="422" y="320" text-anchor="middle">Hab.</text> <!-- Principal  -->

            </g>

            <!-- Doors -->
            <g class="stroke-tp-bg/90 stroke-4">

                <line x1="10" y1="50" x2="45" y2="50" />   <!-- Entrada/Exterior  -->
                <line x1="60" y1="110" x2="60" y2="140" />   <!-- Entrada/Cocina -->
                <line x1="10" y1="240" x2="40" y2="240" />   <!-- Entrada/Salón  -->

                <line x1="65" y1="50" x2="90" y2="50" />  <!-- Cocina/Tendedero  -->
                <line x1="1" y1="400" x2="79" y2="400" />   <!-- Salón/Galería  -->

                <line x1="220" y1="180" x2="250" y2="180" /> <!-- Pasillo/Baño                -->
                <line x1="210" y1="240" x2="240" y2="240" /> <!-- Pasillo/HabitaciónGemelas   -->
                <line x1="265" y1="240" x2="295" y2="240" /> <!-- Pasillo/HabitaciónOrdenador -->
                <line x1="350" y1="185" x2="350" y2="230" /> <!-- Pasillo/HabitaciónPrincipal -->

                <line x1="400" y1="185" x2="400" y2="215" /> <!-- Baño/HabitaciónPrincipal -->

                <line x1="60" y1="181" x2="60" y2="239" />   <!-- Entrada/Pasillo     -->
                <line x1="400" y1="281" x2="400" y2="399" /> <!-- Baño/HabitaciónPrincipal -->

            </g>

            <!-- Devices -->
            <g
                v-for="device in devices" 
                :key="device.id"
                :transform="`translate(${device.x}, ${device.y})`"
                class="cursor-pointer select-none"
                @click="toggleDevice(device.id)"
            >

                <circle 
                    r="7" 
                    :class="[
                        'transition-all duration-300 stroke-2',
                        deviceStates[device.id]?.status === 'on' 
                        ? 'fill-yellow-400/20 stroke-yellow-400' 
                        : 'fill-tp-surface/50 stroke-tp-border'
                    ]"
                />
                    
                <circle r="3" :class="deviceStates[device.id]?.status === 'on' ? 'fill-yellow-400' : 'fill-muted'" />
                    
            </g>

        </svg>
    </div>
</template>