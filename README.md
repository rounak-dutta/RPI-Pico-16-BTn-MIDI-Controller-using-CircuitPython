# RPI-Pico-16-BTn-MIDI-Controller-using-CircuitPython
    A simple portable USB MIDI controller based on Raspberry-PI Pico, written in Circuit Python.

# YouTube Link for the Device Usage Demo: 
    https://youtu.be/kVHYq4UNdmo
    
# Other Links/ References:
    
    CircuitPython UF2 file Download: https://circuitpython.org/board/raspberry_pi_pico/
    CircuitPython Library Download: https://circuitpython.org/libraries
    CircuitPython Docs on the modules used: https://circuitpython.readthedocs.io/en/latest/shared-bindings/displayio/index.html
    Mu Editor Download Link: https://codewith.mu/

    *** Please make sure to match the library and the UF2 file versions ***
    *** Even Notepad can be used to modify the "code.py" file on the RPI-Pico, but Mu editor has the Serial-terminal integrated and also checks for syntax and other issues in the code, hence I used the above. ***
    *** Only issue with (the version of Mu) editor I have is that it crashes if large amoumnt of serial data needs to be displayed and/or the data is updated too fast in the serial terminal. ***

# Detailed Description of the project/ device:
    The aim is to create a simple and portable USB MIDI controller to be used with DAWs availble on mobile devices, e.g., FL Studio Mobile, Garage Band, etc. 
    This is because I personally find playing something on a touch-screen to be very difficult, hence if I have any spontaneous musical ideas, I almost always have to sit down with my laptop, plug the usb-audio-interface, plug my keyboard as MIDI device, etc etc, which sometimes may or may not be possible depending on the situation, as well as mood.
    *** I am fully aware that portable MIDI controllers and Keyboards are readily available, but where's the fun in just simply buying them, when you can make one yourself ;-) ***
    *** If one is interested solely in the music-production aspect, I will suggest to get the commercially available devices and ignore this project, as it will save precious time, but if you like to DIY, then please keep reading ***
    
    The device (after construction) shows up and acts as general MIDI device in PC or Android. I have tested in Windows 10 with Waveform-11 and in Android Smartphone with FL-Studio mobile, and it works with both and device is recognized without any drivers. Thanks to the amazing libraries from Adafruit Industries.

    The controller is USB bus powered and has 16-buttons in the keypad, which can be used to send MIDI notes. Multiple notes can be sent at ones, but the polyphony is limited by the ghost-note effect of the 4x4 button matrix. This can be fixed by using diodes with switches, one can google for "diode keypad matrix" regarding the same for more information.
    
    The controller's GUI consists of the 128x64 oled screen and the rotary encoder. The notes for each key in the keypad is displayed and with the rotary encoder the velocity value can be selected, as well as transpose and octave. 
    
    The controller also has a scale mode, where currently 10 scales can be selected, with chromatic-scale as the default.
    It also has a chord mode, where Power, Major, Minor and Diminshed chords can be sent by presseing only one button.
    
    For more information and a demo of the features, please visit the YouTube link.

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

# 2. Encoder Connection:  
                        L to R, knob facing towards viewer:
                        clk (pin-1): GP14 and dt (pin-3): GP15, com (pin-2): Gnd

# 3. I2C 0.96 Blue OLED Connections: 
                        sda-pin: GP20 and scl-pin: GP21; 
                        vdd, vss to 3.3V and gnd respectively 
                        Address: 0x3C

# 4. Touch Input for Sustain:
                        GP11 pin, and a 1meg resistor pull-down from the pin to gnd.

# Notes: 
    1. The keypad I have used here is non-standard. I found and bought the same from my local electronic shop, and it is most likely a replacement part for land-line telephone. But the code in the "scanKBD()" function, can be easily modified to accomodate the readily available 4x4 matrix keypads.
    
    2. Based on the above, since I had some extra lines available for the 16-key matrix, I placed the encoder switch between h,k nodes, if standard 16-key, i.e., 4x4 matrix is used, the encoder pin can be shifted to any other GPIO pin. The encoder switch-reading is done inside the main while loop. 
    
    3. The oled brightness is currently set to 0.4 (i.e., 40%), and the same can be changed in the "Initializing the 0.96inch OLED Display" portion of the code.
    
    4. The threshold for the touch-input (for sustain) can be set in the "Setting Touch-pin for Sustain Input" portion of the code.
    
    5. If the oled screen has different address (or different I2C speed, here 1,000,000 is used), the same can also be modified in the "Initializing the 0.96inch OLED Display" section.


# Steps to load the code in RPI-Pico, (many other tutorials are also available on the internet on how to load CircuitPython in RPI-Pico, please feel free to refer to them):
    1. For a new/ fresh RPI-Pico which is not setup for circuit python, press and hold the "bootsel" button on the Pico, and then plugin to the PC and release the button.
    
    2. The Pico should show-up as a drive "RPI-RP2", and in that drive copy the the CircuitPython's UF2 file, either from this repository or from the CircuitPython page, link mentioned above, near the heading.
    
    3. After the UF2 file is copied, the Pico now appears as a new drive ("CIRCUITPY") and it should contain the "lib" folder and the "code.py" file.
    
    4. In the lib-folder all the required libraries for code.py should be present, and one can copy the contents of the lib-folder attached in this repository or download the corresponding latest versions from the CircuitPython page. 
    
    *** Please make sure, the UF2 file and the libs used are of the same version, otherwise errors may occur ***.
    
    5. In the Pico's "code.py" file, copy the contents of the "16-BTn_MIDI_Controller_ver1.py" file present in this repository, and as soon as the changes are saved in the "code.py" file, the code should start running.
    
    6. Please make the required changes to the "code.py" file to match the hardware connections in your design.
    
