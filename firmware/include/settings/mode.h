#ifndef MODE_H
#define MODE_H

namespace Mode {

    enum Value {
        NORMAL,
        CONNECTION,
        LOCKED      // Admin lock, see Settings::locked
    };

    bool is(Value mode);
    void set(Value mode);
}

#endif // MODE_H
