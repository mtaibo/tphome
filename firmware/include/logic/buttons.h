#ifndef BUTTONS_H
#define BUTTONS_H

#include <stdint.h>

namespace Buttons {

    /* Enums to simplify code */
    enum Action { NONE, SHORT, MEDIUM, LONG };

    void update();

    /* Returns the pending action of the button and clears it */
    Action getAction(uint8_t pin);
}

#endif // BUTTONS_H
