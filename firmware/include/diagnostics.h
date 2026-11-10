#ifndef DIAGNOSTICS_H
#define DIAGNOSTICS_H

#include <stdint.h>

namespace Diagnostics {
    extern uint16_t flashWrites; // Flash writes since boot, reported over MQTT
}

#endif // DIAGNOSTICS_H
