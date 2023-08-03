
from gpiozero import Button
from enum import Enum
from rcp import iso_minus, iso_plus

class KeyPadCommands(Enum):

    ZOOM = 0
    AUTOFOCUS = 1


class KeyPad:


    def __init__(self) -> None:
        self.row = [Button(n) for n in range(0,4)]
        self.col = [Button(n) for n in range(5,9)]



        self.config = [
            [iso_plus, iso_minus, None, None],
            [None, None, None, None],
            [None, None, None, None],
            [None, None, None, None],
    ]
    

    def check(self):
        for r in self.row:
            for c in self.col:
                if r.is_pressed and c.is_pressed:
                    return r, c
        
        return None, None
    
                    