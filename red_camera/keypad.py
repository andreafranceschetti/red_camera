from gpiozero import Button, DigitalInputDevice, DigitalOutputDevice

class KeyPad:
    """keypad device"""

    def __init__(self, rows = [29, 31, 33, 35], cols = [32, 36, 38, 40]) -> None:
        """ initialize this class with your gpio hardware configuration """

        self.rows = [DigitalOutputDevice(n) for n in rows]
        self.cols = [Button(n, pull_up=False, bounce_time=0.05) for n in cols]
    

    def read(self):
        for r, row in enumerate(self.rows):
            row.on()
            for c, button in enumerate(self.cols):
                if button.is_pressed:
                    return r, c
            r.off()
        return None, None
    
                    