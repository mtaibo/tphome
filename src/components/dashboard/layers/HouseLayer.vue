<template>

    <!-- Rooms -->
    <g class="fill-tp-surface/30 stroke-tp-border stroke-2">

        <rect x="0"   y="50"  width="60"  height="190" /> <!-- Entrada                      -->
        <rect x="60"  y="180" width="290" height="60"  /> <!-- Pasillo                      -->
        <rect x="350" y="180" width="50"  height="220" /> <!-- Pasillo Habitación Principal -->

        <rect x="60" y="0"  width="60"  height="50"  />  <!-- Tendedero -->
        <rect x="60" y="50" width="130" height="130" />  <!-- Cocina    -->

        <rect x="0" y="240" width="150" height="160" />  <!-- Salón -->
        <rect x="0" y="400" width="80"  height="30"  />  <!-- Galería -->

        <rect x="190" y="80"  width="75" height="100" />  <!-- Baño Invitados -->
        <rect x="400" y="180" width="90" height="100" />  <!-- Baño Principal -->

        <rect x="150" y="240" width="100" height="160" />  <!-- Habitación Gemelas   -->
        <rect x="250" y="240" width="100" height="160" />  <!-- Habitación Ordenador -->
        <rect x="400" y="280" width="90"  height="120" />  <!-- Habitación Principal -->

    </g>

    <!-- Names -->
    <g class="fill-muted font-mono text-[11px] uppercase tracking-widest pointer-events-none">

        <text x="210" y="214" text-anchor="middle">Pasillo</text>

        <text x="125" y="105" text-anchor="middle">Cocina</text>

        <text x="45"  y="290" text-anchor="middle">Salón</text>

        <text x="227" y="105" text-anchor="middle">Baño</text> <!-- Invitados -->
        <text x="440" y="214" text-anchor="middle">Baño</text> <!-- Principal  -->

        <text x="200" y="290" text-anchor="middle">Hab.</text> <!-- Gemelas -->
        <text x="320" y="290" text-anchor="middle">Hab.</text> <!-- Ordenador -->
        <text x="422" y="320" text-anchor="middle">Hab.</text> <!-- Principal  -->

    </g>

    <!-- Doors -->
    <g class="stroke-tp-bg/90 stroke-4">

        <line x1="10" y1="50"  x2="45" y2="50"  />  <!-- Entrada/Exterior  -->
        <line x1="60" y1="110" x2="60" y2="140" />  <!-- Entrada/Cocina -->
        <line x1="10" y1="240" x2="40" y2="240" />  <!-- Entrada/Salón  -->

        <line x1="65" y1="50"  x2="90" y2="50"  />  <!-- Cocina/Tendedero  -->
        <line x1="1"  y1="400" x2="79" y2="400" />  <!-- Salón/Galería  -->

        <line x1="220" y1="180" x2="250" y2="180" /> <!-- Pasillo/Baño                -->
        <line x1="210" y1="240" x2="240" y2="240" /> <!-- Pasillo/HabitaciónGemelas   -->
        <line x1="265" y1="240" x2="295" y2="240" /> <!-- Pasillo/HabitaciónOrdenador -->
        <line x1="350" y1="185" x2="350" y2="230" /> <!-- Pasillo/HabitaciónPrincipal -->

        <line x1="400" y1="185" x2="400" y2="215" /> <!-- Baño/HabitaciónPrincipal -->

        <line x1="60"  y1="181" x2="60"  y2="239" /> <!-- Entrada/Pasillo     -->
        <line x1="400" y1="281" x2="400" y2="399" /> <!-- Baño/HabitaciónPrincipal -->

    </g>

</template>