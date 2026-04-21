
export const devices = {

    lights: {

        'L0101' : { name: 'Luz Grande Salón',  x: 110, y:270, on: false },
        'L0102' : { name: 'Luz Pequeña Salón', x:  75, y:340, on: false },

        'L0201' : { name: 'Luz Habitación Gemelas', x: 200, y: 320, on: false },

        'L0301' : { name: 'Luz Habitación Ordenador Cama',    x: 280, y: 280, on: false },
        'L0302' : { name: 'Luz Habitación Ordenador Armario', x: 315, y: 330, on: false },

        'L0401' : { name: 'Luz Habitación Principal Cama',    x: 420, y: 340, on: false },
        'L0402' : { name: 'Luz Habitación Principal Armario', x: 375, y: 240, on: false },

        'L0501' : { name: 'Luz Entrada',  x:  30, y: 125, on: false },
        'L0502' : { name: 'Luz Pasillo',  x: 160, y: 211, on: false },
        'L0503' : { name: 'Luz Exterior', x:  30, y:  25, on: false },

        'L0601' : { name: 'Luz Baño Invitados',        x: 228, y: 130, on: false },
        'L0602' : { name: 'Luz Baño Invitados Espejo', x: 205, y: 160, on: false },

        'L0701' : { name: 'Luz Baño Principal',        x: 445, y: 240, on: false },
        'L0702' : { name: 'Luz Baño Principal Espejo', x: 475, y: 200, on: false },

        'L0801' : { name: 'Luz Cocina',    x: 125, y: 125, on: false },
        'L0802' : { name: 'Luz Tendedero', x:  90, y:  25, on: false },

    },

    switches: {

    },

    blinds: {

        'B0101': { name: 'Persiana Salón Grande',         x:  10, y: 427, width: 60, height:  7, state: { position: 75, motor: 0 } },
        'B0102': { name: 'Persiana Salón Pequeña',        x:  77, y: 405, width:  7, height: 20, state: { position: 50, motor: 0 } },

        'B0201': { name: 'Persiana Habitación Gemelas',   x: 180, y: 397, width: 50, height:  7, state: { position:  60, motor: 0 } },

        'B0301': { name: 'Persiana Habitación Ordenador', x: 270, y: 397, width: 50, height:  7, state: { position: 100, motor: 0 } },

        'B0401': { name: 'Persiana Habitación Principal', x: 400, y: 397, width: 50, height:  7, state: { position:   0, motor: 0 } },

    }
}