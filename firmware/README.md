
## TYWE3S

This table below represents every pin that can be used on chip TYWE3S to interact with buttons, leds and relays. It also includes transmitting and receiving pins which can't be active if you want to see the serial monitor.

| PINs   | 0   | 1  | 2 | 3 | 5 | 12  | 13 | 14  | 15 | 16  |
|:-------|-----|----|---|---|---|-----|----|-----|----|-----|
|LEDs    |Green|    |Low|   |   |     |    |Mid  |    |Top  |
|Buttons |     |    |   |Mid|Low|Top  |    |     |    |     |
|Relays  |     |    |   |   |   |     |L1  |     |L3  |     |
|TX/RX   |     |X   |   |X  |   |     |    |     |    |     |

### LED

* **Green LED:** This LED just turns green or off, it doesn't have a secondary color when it's toggled off. To turn this LED green, position is HIGH, to turned it off, position is LOW.

* **Other LED:** The other three LEDs on the chip has two colors. When position is set to HIGH, this LED will bright in RED, otherwise, it will bright in BLUE.

### BUTTON

* **Position:** Every button has two positions, pressed and released. The pressed position corresponds to LOW, which is also 0. Otherwise, the released position correpsonds to HIGH, which is 1.

### RELAY

* When position is set to HIGH, relay will be giving current to the blind motor, so when position is set to LOW, the relay will not be giving current.

### OTHER

