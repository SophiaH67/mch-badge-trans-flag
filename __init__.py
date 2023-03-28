import display
import time
from machine import Pin
from neopixel import NeoPixel
import nvs
import buttons
import mch22


class State:
    night_mode = False


# Pin 19 controls the power supply to SD card and neopixels
powerPin = Pin(19, Pin.OUT)

# Pin 5 is the LED's data line
dataPin = Pin(5, Pin.OUT)

# create a neopixel object for 5 pixels (the little sail)
np = NeoPixel(dataPin, 5)

# turn on power to the LEDs
powerPin.on()


def on_home_button(pressed):
    if pressed:
        mch22.exit_python()


def on_a_button(pressed):
    if pressed:
        State.night_mode = not State.night_mode

        if State.night_mode:
            powerPin.off()
            # Draw a black rectangle over the screen
            display.drawRect(0, 0, display.width(), display.height(), True, 0x000000)
            display.flush()
        else:
            powerPin.on()
            draw_trans_flag()


buttons.attach(buttons.BTN_HOME, on_home_button)
buttons.attach(buttons.BTN_A, on_a_button)

blue_hex = 0x5BCEFA
pink_hex = 0xF5A9B8
white_hex = 0xFFFFFF


def hex_to_rgb(hex_color):
    return (hex_color >> 16, (hex_color >> 8) & 0xFF, hex_color & 0xFF)


blue_rgb = hex_to_rgb(blue_hex)
pink_rgb = hex_to_rgb(pink_hex)
white_rgb = hex_to_rgb(white_hex)

display_height = display.height()
display_width = display.width()

"""
top left: 2
top center: 3
middle center: 1
bottom center: 0
bottom right: 4
"""
neopixels_local = [blue_rgb, pink_rgb, white_rgb, pink_rgb, blue_rgb]


def cycle_neopixels():
    for i in range(5):
        np[i] = neopixels_local[i]

    # Shuffle the list
    neopixels_local.insert(0, neopixels_local.pop())

    np.write()


def draw_trans_flag():
    # Main display
    for i in range(5):
        color = (
            blue_hex
            if i == 0 or i == 4
            else pink_hex
            if i == 1 or i == 3
            else white_hex
        )

        y_offset = display_height // 5 * i

        display.drawRect(0, y_offset, display_width, display_height // 5, True, color)

    display.flush()


# Main loop
draw_trans_flag()

while True:
    cycle_neopixels()
    time.sleep(1)
