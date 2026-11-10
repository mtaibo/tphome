#ifndef BLINDS_H
#define BLINDS_H

#include <stdint.h>

namespace Blinds {

    enum State { IDLE, WAITING, MOVING, STOPPING };

    void stop(); // Stop any movement and save the position
    bool isIdle();
    State state();
    void update();

    namespace Position {
        void set(uint16_t targetPosition); // 0 (closed) - 10000 (open)
    }
}

#endif // BLINDS_H
