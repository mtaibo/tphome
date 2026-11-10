#ifndef NETWORK_H
#define NETWORK_H

namespace Network {
    void setup();
    bool isConnected();

    /* busy: the device is doing something that must not be interrupted (blind moving) */
    void update(bool busy);
}

#endif // NETWORK_H
