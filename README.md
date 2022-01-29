# RPI-Pico-16-BTn-MIDI-Controller-using-CircuitPython
A simple portable USB MIDI controller based on Raspberry-PI Pico, written in Circuit Python

# Parts Required (excluding the PC, MIDI-host-device and the usb-cable):
    1. Raspberry-Pi Pico microcontroller - 1pc
    2. 0.96 inch 128x64 monochrome oled display (here the blue one is used, as it is cheaper). - 1pc
    3. Rotary encoder with switch (5-pins, 2-pins for built-in switch and 3 pins for the encoder) - 1pc
    4. Prototyping PCB (Vero-board) or breadboard, for connecting everything together - 1pc
    5. 1 Mega Ohm resistor as pull-down for the touch-input - 1pc
    6. Some Connecting wires - as per requirement

# Hardware Connection Information:

# 1. Currrent Keypad Setup:
    Keypad Pins:      a   b   c   d   e   f   g   h   i   j   k 
    RPI Pico Pins:    GP0 GP1 GP2 GP3 GP4 GP5 GP6 GP7 GP8 GP9 GP10

    Matrix:             1(c,b)   2(c,d)   3(c,e)   4(h,i)
                        5(a,b)   6(a,d)   7(a,e)   8(g,i)
                        9(f,k)   10(f,d)  11(f,e)  12(f,i)
                        13(j,k)  14(j,d)  15(j,e)  16(j,i)
                        Encoder-Switch (h,k)

# 2. Ecoder Connection:  
                        L to R, knob facing towards viewer:
                        clk (pin-1): GP14 and dt (pin-3): GP15, com (pin-2): Gnd

# 3. I2C 0.96 Blue OLED Connections: 
                        sda-pin: GP20 and scl-pin: GP21; 
                        vdd, vss to 3.3V and gnd respectively 
                        Address: 0x3C

# 4. Touch Input for Sustain:
                        GP11 pin, and a 1meg resistor pull-down from the pin to gnd.

# Notes: 
    1. The keypad I have used here is non-standard. I found and bought the same from my local electronic shop, and it is most likely a replacement part for land-line telephone. But the code in the scanKBD() function, can be easily modified to accomodate the readily available 4x4 matrix keypads.
    2. Based on the above, since I had some extra lines available for the 16-key matrix, I placed the encoder switch between h,k nodes, if standard 16-key, i.e., 4x4 matrix is used, the encoder pin can be shifted to any other GPIO pin. The encoder switch-reading is done inside the main while loop. 
    3. The oled brightness is currently set to 0.4 (i.e., 40%), and the same can be changed in the "Initializing the 0.96inch OLED Display" portion of the code.
    4. The threshold for the touch-input (for sustain) can be set in the "Setting Touch-pin for Sustain Input" portion of the code
    5. If the oled screen has different address (or different I2C speed, here 1,000,000 is used), the same can be modified in the "Initializing the 0.96inch OLED Display" section.
