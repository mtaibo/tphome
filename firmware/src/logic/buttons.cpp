#include "buttons.h"
#include "defaults.h"
#include "hardware/board.h"

namespace Buttons {

    /* Struct to store the result of each button check */
    struct ButtonState {
        uint8_t pin;
        Action action;
    };

    /* Array that store every button with its corresponding next action */
    static ButtonState _states[3] = {
        {Pins::BTN_TOP, NONE}, {Pins::BTN_MID, NONE}, {Pins::BTN_BTM, NONE}
    };

    /* Private function to translate duration to Action */
    static Action _translate(uint16_t duration) {
        if (duration >= Defaults::LONG_PULSE) return LONG;
        else if (duration >= Defaults::SHORT_PULSE) return MEDIUM;
        else if (duration >= 5) return SHORT;
        else return NONE;
    }

    /* Function that introduce next action to the button struct array */
    void update() {
        _states[0].action = _translate(Hardware::BtnTop::getDuration());
        _states[1].action = _translate(Hardware::BtnMid::getDuration());
        _states[2].action = _translate(Hardware::BtnBtm::getDuration());
    }

    /* Function that handles each button action based on buttons state array */
    Action getAction(uint8_t pin) {
        for (auto &state : _states) {
            if (state.pin == pin) {
                Action action = state.action;
                state.action = NONE;
                return action;
            }
        } return NONE;
    }
}
