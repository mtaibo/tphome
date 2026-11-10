#if defined(DEVICE_HARDWARE_ESP8266)

#include <Arduino.h>
#include "hardware/esp8266/hardware.h"

extern "C" {
    #include <user_interface.h>
}

namespace Hardware {

    void setState(uint8_t pin, bool state) {
        switch (pin) {
            case Pins::LED_GREEN: state ? LedGreen::on() : LedGreen::off(); break;
            case Pins::LED_BTM: state ? LedBtm::on() : LedBtm::off(); break;
            case Pins::LED_MID: state ? LedMid::on() : LedMid::off(); break;
            case Pins::LED_TOP: state ? LedTop::on() : LedTop::off(); break;
        }
    }

    uint8_t resetReason() {
        return (uint8_t) ESP.getResetInfoPtr()->reason;
    }

    void setup() {

        LedGreen::setup();
        LedBtm::setup();
        LedMid::setup();
        LedTop::setup();

        BtnBtm::setup();
        BtnMid::setup();
        BtnTop::setup();

        RelayUp::setup();
        RelayDown::setup();

        enableLight();
    }
}

#endif // DEVICE_HARDWARE_ESP8266
