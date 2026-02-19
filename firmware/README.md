# TYWE3S

## PIN Distribution

This table below represents every pin that can be used on chip TYWE3S to interact with buttons, leds and relays. It also includes transmitting and receiving pins which can't be active if you want to see the serial monitor.

| PINs   | 0   | 1  | 2 | 3 | 5 | 12  | 13 | 14  | 15 | 16  |
|:-------|-----|----|---|---|---|-----|----|-----|----|-----|
|LEDs    |Green|    |Low|   |   |     |    |Mid  |    |Top  |
|Buttons |     |    |   |Mid|Low|Top  |    |     |    |     |
|Relays  |     |    |   |   |   |     |L1  |     |L3  |     |
|TX/RX   |     |X   |   |X  |   |     |    |     |    |     |

### LEDs

* **Green LED:** This LED just turns green or off, it doesn't have a secondary color when it's toggled off. To turn this LED green, position is HIGH, to turned it off, position is LOW.

* **Other LED:** The other three LEDs on the chip has two colors. When position is set to HIGH, this LED will bright in RED, otherwise, it will bright in BLUE.

### Buttons

* **Position:** Every button has two positions, pressed and released. The pressed position corresponds to LOW, which is also 0. Otherwise, the released position correpsonds to HIGH, which is 1.

### Relays

* When position is set to HIGH, relay will be giving current to the blind motor, so when position is set to LOW, the relay will not be giving current. By default, the pin 13 will be assigned to L1 relay, and pin 15 to L3 relay.

### Other pins

* **Transmiting and receiving pins:** This pins corresponds to 1 and 3. This pins are reserved to the serial monitor and they have to be on LOW state, which means no current is going through them, to transmit or receive information.

* **Flash memory pins:** This pins, from 6 to 11, are reserved to the interaction with flash memory of the chip. They can't be turned on or off manually via code. 

## ACTIONS

This section is refered to how the buttons interact with the chip depending on the duration of the pulse that the user give at each moment.

Each button will have three phases, the short pulse, the medium pulse and the long pulse. Each kind of pulse will make a different action that will be defined below here:

  TOP_BUTTON:
    - short_pulse: blind_up
    - medium_pulse: 
    - long_pulse: access_point

  MEDIUM_BUTTON:
    - short_pulse: blind_stop
    - medium_pulse: save_config
    - long_pulse: reset_memory
  
  BOTTOM_BUTTON:
    - short_pulse: blind_down
    - medium_pulse: 
    - long_pulse: network_setup()

## MQTT COMMANDS
