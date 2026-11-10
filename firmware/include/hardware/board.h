#ifndef BOARD_H
#define BOARD_H

/* Single place that picks the hardware layer for the board being built */
#if defined(DEVICE_HARDWARE_ESP8266)
    #include "hardware/esp8266/hardware.h"
#elif defined(DEVICE_HARDWARE_BK7231N)
    #include "hardware/bk7231n/hardware.h"
#endif

#endif // BOARD_H
