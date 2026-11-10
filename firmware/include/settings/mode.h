#ifndef MODE_H
#define MODE_H

namespace Mode {

    enum Value {
        NORMAL,
        CONNECTION
    };

    bool is(Value mode);
    void set(Value mode);
}

#endif // MODE_H
