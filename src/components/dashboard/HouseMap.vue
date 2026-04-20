<template>

    <div class="w-full h-full flex items-center justify-center p-8">

        <svg 
            viewBox="0 0 800 600" 
            class="w-full h-auto max-w-5xl"
            xmlns="http://www.w3.org/2000/svg"
        >

            <!-- Rooms -->
            <g class="fill-tp-surface/30 stroke-tp-border stroke-2">
                <rect x="20" y="100" width="80" height="220" /> <!-- Recibidor -->
                <rect x="100" y="100" width="150" height="130" /> <!-- Cocina -->
                <rect x="100" y="50" width="60" height="50" /> <!-- Tendedero -->
                <rect x="100" y="260" width="400" height="60" /> <!-- Pasillo -->
            </g>

            <!-- Names -->
            <g class="fill-muted font-mono text-[11px] uppercase tracking-widest pointer-events-none">
                <text x="65" y="210" text-anchor="middle" transform="rotate(270, 65, 210)">Recibidor</text>
                <text x="175" y="170" text-anchor="middle">Cocina</text>
            </g>

            <!-- Door -->
            <g class="stroke-tp-bg/90 stroke-4">
                <line x1="100" y1="160" x2="100" y2="190" /> <!-- Recibidor/Cocina -->
            </g>

        </svg>
    </div>
</template>