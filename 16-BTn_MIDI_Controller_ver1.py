# Ada-fruit Midi Library
# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT
#
# Keypad Midi Controller
# By Rounak Dutta
#
# Huge Thank You! to Adafruit Industries for the libraries and
# the circuit-python environment
#
import board
import digitalio
import displayio
import busio
import terminalio
import touchio
# from analogio import AnalogIn
import time
# import random
import usb_midi
import adafruit_midi
# from adafruit_midi.control_change import ControlChange
from adafruit_midi.note_off import NoteOff
from adafruit_midi.note_on import NoteOn
# from adafruit_midi.pitch_bend import PitchBend
import adafruit_displayio_ssd1306
from adafruit_display_text import label
# Release default Terminal Output in the OLED Display
displayio.release_displays()

# ############################### Connections ###################################
# Currrent Keypad Setup                                                         #
# Keypad Pins:      a   b   c   d   e   f   g   h   i   j   k                   #
# RPI Pico Pins:    GP0 GP1 GP2 GP3 GP4 GP5 GP6 GP7 GP8 GP9 GP10                #
#                                                                               #
# Matrix:           1(c,b)   2(c,d)   3(c,e)   4(h,i)                           #
#                   5(a,b)   6(a,d)   7(a,e)   8(g,i)                           #
#                   9(f,k)   10(f,d)  11(f,e)  12(f,i)                          #
#                   13(j,k)  14(j,d)  15(j,e)  16(j,i)                          #
#                   Encoder-Switch (h,k)                                        #
#                                                                               #
# Ecoder Connection:  L to R knob facing towards viewer:                        #
#                     clk (pin-1): GP14 and dt (pin-3): GP15, com (pin-2): Gnd  #
#                                                                               #
# I2C 0.96 Blue OLED Connections: sda-pin: GP20 and scl-pin: GP21;              #
#                            vdd, vss to 3.3V and gnd respectively              #
#                            Address: 0x3C                                      #
# ###############################################################################

# Initializing GPIOs for the button matrix
a = digitalio.DigitalInOut(board.GP0)
c = digitalio.DigitalInOut(board.GP2)
f = digitalio.DigitalInOut(board.GP5)
g = digitalio.DigitalInOut(board.GP6)
h = digitalio.DigitalInOut(board.GP7)
j = digitalio.DigitalInOut(board.GP9)

b = digitalio.DigitalInOut(board.GP1)
b.direction = digitalio.Direction.INPUT
b.pull = digitalio.Pull.DOWN
d = digitalio.DigitalInOut(board.GP3)
d.direction = digitalio.Direction.INPUT
d.pull = digitalio.Pull.DOWN
e = digitalio.DigitalInOut(board.GP4)
e.direction = digitalio.Direction.INPUT
e.pull = digitalio.Pull.DOWN
i = digitalio.DigitalInOut(board.GP8)
i.direction = digitalio.Direction.INPUT
i.pull = digitalio.Pull.DOWN
k = digitalio.DigitalInOut(board.GP10)
k.direction = digitalio.Direction.INPUT
k.pull = digitalio.Pull.DOWN


# Function to read keyboard and return list of buttons pressed
# Modify according to the Keyboard matrix used
# The O/P pins are re-init to I/P to avoid damage when mutiple keys are pressed
dbDelay1 = 0.001
dbDelay2 = 0.050
trDelay = 0.0001

def scanKbd():
    buttonsPressed = []

    a.direction = digitalio.Direction.OUTPUT
    a.value = True
    time.sleep(trDelay)
    if b.value is True:
        time.sleep(dbDelay1)
        if b.value is True:
            buttonsPressed.append(5)
    if d.value is True:
        time.sleep(dbDelay1)
        if d.value is True:
            buttonsPressed.append(6)
    if e.value is True:
        time.sleep(dbDelay1)
        if e.value is True:
            buttonsPressed.append(7)
    a.direction = digitalio.Direction.INPUT
    a.pull = digitalio.Pull.DOWN
    time.sleep(trDelay)

    c.direction = digitalio.Direction.OUTPUT
    c.value = True
    time.sleep(trDelay)
    if b.value is True:
        time.sleep(dbDelay1)
        if b.value is True:
            buttonsPressed.append(1)
    if d.value is True:
        time.sleep(dbDelay1)
        if d.value is True:
            buttonsPressed.append(2)
    if e.value is True:
        time.sleep(dbDelay1)
        if e.value is True:
            buttonsPressed.append(3)
    c.direction = digitalio.Direction.INPUT
    c.pull = digitalio.Pull.DOWN
    time.sleep(trDelay)

    f.direction = digitalio.Direction.OUTPUT
    f.value = True
    time.sleep(trDelay)
    if k.value is True:
        time.sleep(dbDelay1)
        if k.value is True:
            buttonsPressed.append(9)
    if d.value is True:
        time.sleep(dbDelay1)
        if d.value is True:
            buttonsPressed.append(10)
    if e.value is True:
        time.sleep(dbDelay1)
        if e.value is True:
            buttonsPressed.append(11)
    if i.value is True:
        time.sleep(dbDelay1)
        if i.value is True:
            buttonsPressed.append(12)
    f.direction = digitalio.Direction.INPUT
    f.pull = digitalio.Pull.DOWN
    time.sleep(trDelay)

    j.direction = digitalio.Direction.OUTPUT
    j.value = True
    time.sleep(trDelay)
    if k.value is True:
        time.sleep(dbDelay1)
        if k.value is True:
            buttonsPressed.append(13)
    if d.value is True:
        time.sleep(trDelay)
        if d.value is True:
            buttonsPressed.append(14)
    if e.value is True:
        time.sleep(dbDelay1)
        if e.value is True:
            buttonsPressed.append(15)
    if i.value is True:
        time.sleep(dbDelay1)
        if i.value is True:
            buttonsPressed.append(16)
    j.direction = digitalio.Direction.INPUT
    j.pull = digitalio.Pull.DOWN
    time.sleep(trDelay)

    g.direction = digitalio.Direction.OUTPUT
    g.value = True
    time.sleep(trDelay)
    if i.value is True:
        time.sleep(dbDelay1)
        if i.value is True:
            buttonsPressed.append(8)
    g.direction = digitalio.Direction.INPUT
    g.pull = digitalio.Pull.DOWN
    time.sleep(trDelay)

    h.direction = digitalio.Direction.OUTPUT
    h.value = True
    time.sleep(trDelay)
    if i.value is True:
        time.sleep(dbDelay1)
        if i.value is True:
            buttonsPressed.append(4)
    h.direction = digitalio.Direction.INPUT
    h.pull = digitalio.Pull.DOWN
    time.sleep(trDelay)

    return buttonsPressed


# Initializing Analog Input Pin: (maybe for future)
# velPot = AnalogIn(board.GP26)

# Setting Up RPI built-in LED (maybe for future)
# led = digitalio.DigitalInOut(board.GP25)
# led.direction = digitalio.Direction.OUTPUT

# Setting Touch-pin for Sustain Input
# sustain = touchio.TouchIn(board.GP16)

# Setting the Rotary encoder Pins
encClk = digitalio.DigitalInOut(board.GP14)
encClk.direction = digitalio.Direction.INPUT
encClk.pull = digitalio.Pull.UP
encDt = digitalio.DigitalInOut(board.GP15)
encDt.direction = digitalio.Direction.INPUT
encDt.pull = digitalio.Pull.UP

# Initializing the USB MIDI channel
midi = adafruit_midi.MIDI(
    midi_in=usb_midi.ports[0], in_channel=0, midi_out=usb_midi.ports[1], out_channel=0
)

# Midi Note Values
# Oct.
#       C   C#  D   D#  E   F   F#  G   G#  A   A#  B
#   0   0   1   2   3   4   5   6   7   8   9   10  11
#   1   12  13  14  15  16  17  18  19  20  21  22  23
#   2   24  25  26  27  28  29  30  31  32  33  34  35
#   3   36  37  38  39  40  41  42  43  44  45  46  47
#   4   48  49  50  51  52  53  54  55  56  57  58  59
# ...
# Pitch Bend is 14-bit-value (not used), while notes and related messages are 7-bits

# Default Values
noteStart = 48  # (C4)
noteStr = [
    "C_ ", "C# ", "D_ ", "D# ", "E_ ", "F_ ", "F# ", "G_ ", "G# ", "A_ ", "A# ", "B_ "
    ]
sclStr = ["chr", "min", "maj", "mnP", "mjP", "dor", "phr", "lyd", "mix", "mnH"]
chrdStr = ["pwr", "maj", "min", "dim"]

# Offsets w.r.t the root-note, 16 in number because of 16-key keypad
chrOffsets = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]  # chromatic
minOffsets = [0, 2, 3, 5, 7, 8, 10, 12, 14, 15, 17, 19, 20, 22, 24, 26]  # Minor
majOffsets = [0, 2, 4, 5, 7, 9, 11, 12, 14, 16, 17, 19, 21, 23, 24, 26]  # Major
minPentOffsets = [0, 3, 5, 7, 10, 12, 15, 17, 19, 22, 24, 27, 29, 31, 34, 36]  # Min Pen
majPentOffsets = [0, 2, 4, 7, 9, 12, 14, 16, 19, 21, 24, 26, 28, 31, 33, 36]   # Maj Pen
dorOffsets = [0, 2, 3, 5, 7, 9, 10, 12, 14, 15, 17, 19, 21, 22, 24, 26]  # Dorian
phrOffsets = [0, 1, 3, 5, 7, 8, 10, 12, 13, 15, 17, 19, 20, 22, 24, 25]  # Phrygian
lydOffsets = [0, 2, 4, 6, 7, 9, 11, 12, 14, 16, 18, 19, 21, 23, 24, 26]  # Lydian
mixOffsets = [0, 2, 4, 5, 7, 9, 10, 12, 14, 16, 17, 19, 21, 22, 24, 26]  # Mixolydian
mnhOffsets = [0, 2, 3, 5, 7, 8, 11, 12, 14, 15, 17, 19, 20, 23, 24, 26]  # Harmonic Min

# Creating/ updating the noteList to be sent over midi, based on selected scale
def noteListUpdate(sclSel):
    noteList = []
    if (sclSel == 0):
        for nt in range(0, 16, 1):
            noteList.append(noteStart + chrOffsets[nt])
    elif (sclSel == 1):
        for nt in range(0, 16, 1):
            noteList.append(noteStart + minOffsets[nt])
    elif (sclSel == 2):
        for nt in range(0, 16, 1):
            noteList.append(noteStart + majOffsets[nt])
    elif (sclSel == 3):
        for nt in range(0, 16, 1):
            noteList.append(noteStart + minPentOffsets[nt])
    elif (sclSel == 4):
        for nt in range(0, 16, 1):
            noteList.append(noteStart + majPentOffsets[nt])
    elif (sclSel == 5):
        for nt in range(0, 16, 1):
            noteList.append(noteStart + dorOffsets[nt])
    elif (sclSel == 6):
        for nt in range(0, 16, 1):
            noteList.append(noteStart + phrOffsets[nt])
    elif (sclSel == 7):
        for nt in range(0, 16, 1):
            noteList.append(noteStart + lydOffsets[nt])
    elif (sclSel == 8):
        for nt in range(0, 16, 1):
            noteList.append(noteStart + mixOffsets[nt])
    elif (sclSel == 9):
        for nt in range(0, 16, 1):
            noteList.append(noteStart + mnhOffsets[nt])
    return noteList

# Initializing Variables
keyIndex = 0
oldKeyIndex = 0
octIndex = 0
oldOctIndex = 0
glbVelocity = 100
curNotes = []
prevNotesSent = []
dispNtList = []
selectCtrl = 0
sclSel = 0
chrdMode = 0
chrdType = 1
chrdRoot = []

# Prev state for reading encoder
encPrevState = encClk.value
# Initialize to chromatic note-list
noteList = noteListUpdate(sclSel)


# Initializing the 0.96inch OLED Display
oledI2C = busio.I2C(scl=board.GP21, sda=board.GP20, frequency=1000000)
display_bus = displayio.I2CDisplay(oledI2C, device_address=0x3C)
# Change the brightness in the following line, if required
display = adafruit_displayio_ssd1306.SSD1306(
    display_bus, width=128, height=64, brightness=0.4
    )

# Initialize and display the splash Screen
dispBuff = displayio.Group(max_size=10)
Intro_hdr1 = label.Label(
    terminalio.FONT, text="16-BTn MIDI", color=0x00FF00, x=34, y=8
    )
Intro_hdr2 = label.Label(
    terminalio.FONT, text="by Rounak", color=0x00FF00, x=38, y=20
    )
Intro_hdr3 = label.Label(
    terminalio.FONT, text="Pwrd by CircuitPython", color=0x00FF00, x=2, y=50
    )
dispBuff.append(Intro_hdr1)
dispBuff.append(Intro_hdr2)
dispBuff.append(Intro_hdr3)
display.show(dispBuff)
time.sleep(1)

# Initialize Main Display Screen
dispBuff = displayio.Group(max_size=10)

# Display the current Keypad Config and Settings
ntStrLen = len(noteStr)
for note in range(0, 16, 1):
    xVal = 8 + 16*(note % 4)
    yVal = 8 + 16*int(note / 4)
    note += keyIndex
    note = note % ntStrLen
    if (note < 0):
        note += ntStrLen
    dispNtTxt = label.Label(
        terminalio.FONT, text=noteStr[note], color=0x00FF00, x=xVal, y=yVal
        )
    dispNtList.append(dispNtTxt)
for ntDispObj in dispNtList:
    dispBuff.append(ntDispObj)

dispVelTxt = label.Label(terminalio.FONT, text="Vel.: ", color=0xFFFFFF, x=80, y=8)
dispVelNum = label.Label(terminalio.FONT, text="def", color=0xFFFFFF, x=110, y=8)
dispVelNum.text = "%3d" % glbVelocity
dispKeyTxt = label.Label(terminalio.FONT, text="Trn.: ", color=0xFFFFFF, x=80, y=20)
dispKeyNum = label.Label(terminalio.FONT, text="def", color=0xFFFFFF, x=110, y=20)
dispKeyNum.text = "%3d" % keyIndex
dispOctTxt = label.Label(terminalio.FONT, text="Oct.: ", color=0xFFFFFF, x=80, y=32)
dispOctNum = label.Label(terminalio.FONT, text="def", color=0xFFFFFF, x=110, y=32)
dispOctNum.text = "%3d" % (octIndex + 4)
dispSclTxt1 = label.Label(terminalio.FONT, text="Scl.: ", color=0xFFFFFF, x=80, y=44)
dispSclTxt2 = label.Label(terminalio.FONT, text=sclStr[0], color=0xFFFFFF, x=110, y=44)
dispChrdTxt1 = label.Label(terminalio.FONT, text="Chrd: ", color=0xFFFFFF, x=80, y=56)
dispChrdTxt2 = label.Label(terminalio.FONT, text="off", color=0xFFFFFF, x=110, y=56)
# Selection Arrow
if (selectCtrl == 0):
    dispSelTxt = label.Label(terminalio.FONT, text=">", color=0xFFFFFF, x=74, y=8)
elif (selectCtrl == 1):
    dispSelTxt = label.Label(terminalio.FONT, text=">", color=0xFFFFFF, x=74, y=20)
elif (selectCtrl == 2):
    dispSelTxt = label.Label(terminalio.FONT, text=">", color=0xFFFFFF, x=74, y=32)
elif (selectCtrl == 3):
    dispSelTxt = label.Label(terminalio.FONT, text=">", color=0xFFFFFF, x=74, y=44)
elif (selectCtrl == 4):
    dispSelTxt = label.Label(terminalio.FONT, text=">", color=0xFFFFFF, x=74, y=56)
# Append all the display objects to the display-buffer
dispBuff.append(dispVelTxt)
dispBuff.append(dispVelNum)
dispBuff.append(dispKeyTxt)
dispBuff.append(dispKeyNum)
dispBuff.append(dispOctTxt)
dispBuff.append(dispOctNum)
dispBuff.append(dispSelTxt)
dispBuff.append(dispSclTxt1)
dispBuff.append(dispSclTxt2)
dispBuff.append(dispChrdTxt1)
dispBuff.append(dispChrdTxt2)
# Show the display-buffer on OLED screen
display.show(dispBuff)

# Update the display-Keypad Area
def updateKpd():
    for index in range(0, 16, 1):
        note = noteList[index] % 12
        note += keyIndex
        note = note % ntStrLen
        if (note < 0):
            note += ntStrLen
        dispNtList[index].text = noteStr[note]
    display.show(dispBuff)

# Update the display-Keypad area for chord mode
def updateChrdKpd():
    ntIndex = 0
    for index in range(0, 16, 1):
        if ((index + 1) % 4 == 0):
            chrdIndex = int((index + 1) / 4) - 1
            dispNtList[index].text = chrdStr[chrdIndex]
        else:
            note = noteList[ntIndex] % 12
            note += keyIndex
            note = note % ntStrLen
            if (note < 0):
                note += ntStrLen
            dispNtList[index].text = noteStr[note]
            ntIndex += 1
    display.show(dispBuff)

# Send Midi-Notes Notes ON and OFF
def sendMidiNotes(buttonsPressed):
    global prevNotesSent
    global curNotes
    curNotes = []
    for button in buttonsPressed:
        noteVal = (octIndex*12 + keyIndex + noteList[button-1])
        curNotes.append(noteVal)
        if (noteVal not in prevNotesSent):
                midi.send(NoteOn(noteVal, glbVelocity))
                prevNotesSent.append(noteVal)
    for prevNt in prevNotesSent:
        if (prevNt not in curNotes):
            midi.send(NoteOff(prevNt, glbVelocity))
            prevNotesSent.remove(prevNt)

# Send Midi-Chords ON and OFF, based on button-pressed and chord-type
def sendMidiChords(buttonsPressed):
    global prevNotesSent
    global chrdType
    global octIndex
    global keyIndex
    global curNotes
    chrdRoot = []
    curNotes = []
    for button in buttonsPressed:
        if (button % 4 == 0):
            chrdType = int(button / 4)
            dispChrdTxt2.text = chrdStr[chrdType - 1]
        else:
            chrdRoot.append(button - int(button / 4))  
    if (chrdRoot):
        noteVal = (octIndex*12 + keyIndex + noteList[chrdRoot[-1] - 1])
        curNotes.append(noteVal)
        # Power Chord, i.e., root and 5th
        if (chrdType == 1):
            fifthNote = noteVal + 7
            curNotes.append(fifthNote)
            if (noteVal not in prevNotesSent):
                midi.send(NoteOn(noteVal, glbVelocity))
                midi.send(NoteOn(fifthNote, glbVelocity))
                prevNotesSent.append(noteVal)
                prevNotesSent.append(fifthNote)
        # Major Chord, i.e., root, 3rd and 5th
        elif (chrdType == 2):
            thirdNote = noteVal + 4
            fifthNote = noteVal + 7
            curNotes.append(thirdNote)
            curNotes.append(fifthNote)
            if (noteVal not in prevNotesSent):
                midi.send(NoteOn(noteVal, glbVelocity))
                midi.send(NoteOn(thirdNote, glbVelocity))
                midi.send(NoteOn(fifthNote, glbVelocity))
                prevNotesSent.append(noteVal)
                prevNotesSent.append(thirdNote)
                prevNotesSent.append(fifthNote)
        # Minor Chord, i.e., root, b3rd and 5th
        elif (chrdType == 3):
            thirdNote = noteVal + 3
            fifthNote = noteVal + 7
            curNotes.append(thirdNote)
            curNotes.append(fifthNote)
            if (noteVal not in prevNotesSent):
                midi.send(NoteOn(noteVal, glbVelocity))
                midi.send(NoteOn(thirdNote, glbVelocity))
                midi.send(NoteOn(fifthNote, glbVelocity))
                prevNotesSent.append(noteVal)
                prevNotesSent.append(thirdNote)
                prevNotesSent.append(fifthNote)
        # Diminished Chord, i.e., root, b3rd and b5th
        elif (chrdType == 4):
            thirdNote = noteVal + 3
            fifthNote = noteVal + 6
            curNotes.append(thirdNote)
            curNotes.append(fifthNote)
            if (noteVal not in prevNotesSent):
                midi.send(NoteOn(noteVal, glbVelocity))
                midi.send(NoteOn(thirdNote, glbVelocity))
                midi.send(NoteOn(fifthNote, glbVelocity))
                prevNotesSent.append(noteVal)
                prevNotesSent.append(thirdNote)
                prevNotesSent.append(fifthNote)
    for prevNt in prevNotesSent:
        if (prevNt not in curNotes):
            midi.send(NoteOff(prevNt, glbVelocity))
            prevNotesSent.remove(prevNt)

# Starting the functional Loop
while True:
    # Reading Touch-Input
    # sustain.threshold = 9000
    # print(sustain.value)
    # time.sleep(1)

    # Reading the Keypad
    buttonsPressed = scanKbd()
    # if(buttonsPressed):
    #    buttonsPressed.sort()

    # Reading Control Select Button
    h.direction = digitalio.Direction.OUTPUT
    h.value = True
    time.sleep(trDelay)
    if k.value is True:
        time.sleep(dbDelay2)
        if k.value is True:
            selectCtrl += 1
            selectCtrl %= 5

        if (selectCtrl == 0):
            dispSelTxt.y = 8
        elif (selectCtrl == 1):
            dispSelTxt.y = 20
        elif (selectCtrl == 2):
            dispSelTxt.y = 32
        elif (selectCtrl == 3):
            dispSelTxt.y = 44	
        elif (selectCtrl == 4):
            dispSelTxt.y = 56
        time.sleep(0.1)
    h.direction = digitalio.Direction.INPUT
    h.pull = digitalio.Pull.DOWN
    time.sleep(trDelay)

    # Reading the Rotary Encoder for control change
    # little glitchy as interrupt is not used
    encCurState = encClk.value
    if (encCurState != encPrevState):
        if (encDt.value != encCurState):
            if (selectCtrl == 0):
                if (glbVelocity > 0):
                    glbVelocity -= 10
                    dispVelNum.text = "%3d" % glbVelocity
            elif (selectCtrl == 1):
                if (keyIndex > -12):
                    keyIndex -= 1
                    dispKeyNum.text = "%3d" % keyIndex
                    if (chrdMode == 0):
                        updateKpd()
                    else:
                        updateChrdKpd()
                    oldNoteList = noteList
            elif (selectCtrl == 2):
                if (octIndex > -3):
                    octIndex -= 1
                    dispOctNum.text = "%3d" % (octIndex + 4)
                    oldNoteList = noteList
            elif (selectCtrl == 3 and chrdMode == 0):
                if (sclSel > 0):
                    sclSel -= 1
                    oldNoteList = noteList
                    noteList = noteListUpdate(sclSel)
                    dispSclTxt2.text = sclStr[sclSel]
                    updateKpd()
            elif (selectCtrl == 4):
                if (chrdMode > 0):
                    chrdMode -= 1
                    noteList = noteListUpdate(sclSel)
                    updateKpd()
                    dispSclTxt2.text = sclStr[sclSel]
                    dispChrdTxt2.text = "off"
        else:
            if (selectCtrl == 0):
                if (glbVelocity < 120):
                    glbVelocity += 10
                    dispVelNum.text = "%3d" % glbVelocity
            elif (selectCtrl == 1):
                if (keyIndex < 12):
                    keyIndex += 1
                    dispKeyNum.text = "%3d" % keyIndex
                    if (chrdMode == 0):
                        updateKpd()
                    else:
                        updateChrdKpd()
                    oldNoteList = noteList
            elif (selectCtrl == 2):
                if (octIndex < 5):
                    octIndex += 1
                    dispOctNum.text = "%3d" % (octIndex + 4)
                    oldNoteList = noteList
            elif (selectCtrl == 3 and chrdMode == 0):
                if (sclSel < 9):
                    sclSel += 1
                    oldNoteList = noteList
                    noteList = noteListUpdate(sclSel)
                    dispSclTxt2.text = sclStr[sclSel]
                    updateKpd()
            elif (selectCtrl == 4):
                if (chrdMode < 1):
                    chrdMode += 1
                    noteList = noteListUpdate(0)
                    updateChrdKpd()
                    dispChrdTxt2.text = chrdStr[chrdType - 1]
                    dispSclTxt2.text = "N/A"
        encPrevState = encCurState

    if (chrdMode == 0):
        # Send the notes corresponding to pressed button(s) over USB midi
        # This also takes care of buttons released
        sendMidiNotes(buttonsPressed)
    elif (chrdMode == 1):
        # Send the chord-notes corresponding to pressed-btn (root) over USB midi
        # This also takes care of button released
        sendMidiChords(buttonsPressed)
