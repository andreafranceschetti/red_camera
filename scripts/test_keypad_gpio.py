from red_camera.keypad import KeypadFactory
from time import sleep

if __name__ == "__main__":
    KEYPAD = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]
    ROW_PINS = [4, 17, 18, 27, 22]
    COL_PINS = [9, 10, 24, 23]
    kp = KeypadFactory().create_keypad(
        keypad=KEYPAD,
        row_pins=ROW_PINS,
        col_pins=COL_PINS,
        repeat=True,
        repeat_rate=5,
        key_delay=100,
    )

    def printkey(key):
        print(key)

    kp.registerKeyPressHandler(printkey)

    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        pass

    kp.cleanup()
