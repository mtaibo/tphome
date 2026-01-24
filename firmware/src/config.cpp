#include <config.h>

Config config;

void config_default() {

    // Blind configuration
    config.up_time = 30000;
    config.down_time = 25000;
    config.current_position = 0.0;

    // Execution data
    config.is_moving = false;
    config.is_waiting = false;

    // Preferences
    config.block_buttons = false;
    config.short_pulse = 3000;
    config.long_pulse = 10000;
}