from machine import Pin
import uasyncio as asyncio

import time

class F5463BH:
    def __init__(self, A, B, C, D, E, F, G, DP, DDOT, DIG1, DIG2, DIG3, DIG4):
        self.__A =    Pin(A,    Pin.OUT, Pin.PULL_DOWN)
        self.__B =    Pin(B,    Pin.OUT, Pin.PULL_DOWN)
        self.__C =    Pin(C,    Pin.OUT, Pin.PULL_DOWN)
        self.__D =    Pin(D,    Pin.OUT, Pin.PULL_DOWN)
        self.__E =    Pin(E,    Pin.OUT, Pin.PULL_DOWN)
        self.__F =    Pin(F,    Pin.OUT, Pin.PULL_DOWN)
        self.__G =    Pin(G,    Pin.OUT, Pin.PULL_DOWN)
        self.__DP =   Pin(DP,   Pin.OUT, Pin.PULL_DOWN)
        self.__DDOT = Pin(DDOT, Pin.OUT, Pin.PULL_UP)
        self.__DIG1 = Pin(DIG1, Pin.OUT, Pin.PULL_UP)
        self.__DIG2 = Pin(DIG2, Pin.OUT, Pin.PULL_UP)
        self.__DIG3 = Pin(DIG3, Pin.OUT, Pin.PULL_UP)
        self.__DIG4 = Pin(DIG4, Pin.OUT, Pin.PULL_UP)

        self.__DIGITS_SEGMENTS = {
            "DIG1" : 0b00000010,
            "DIG2" : 0b00000010,
            "DIG3" : 0b00000010,
            "DIG4" : 0b00000010
        }

        asyncio.create_task(self.__refresh_screen())

    async def write(self, dig1, dig2, dig3, dig4, dot1=False, dot2=False, dot3=False, dot4=False, ddot=False):
        if ddot:
            self.__DDOT.high()
        else:
            self.__DDOT.low()

        digits_map = (
            (dig1, dot1, "DIG1"),
            (dig2, dot2, "DIG2"),
            (dig3, dot3, "DIG3"),
            (dig4, dot4, "DIG4"),
        )

        for digit, dot, dig_seg in digits_map:
             await asyncio.sleep(0.0001)
             await self.__update_digit(digit, dot, dig_seg)


    async def __update_digit(self, digit, dot, dig_seg):
        patterns = [
            0b1111110,  # 0
            0b0110000,  # 1
            0b1101101,  # 2
            0b1111001,  # 3
            0b0110011,  # 4
            0b1011011,  # 5
            0b1011111,  # 6
            0b1110000,  # 7
            0b1111111,  # 8
            0b1111011   # 9
        ]

        pattern = patterns[digit]
        self.__DIGITS_SEGMENTS[dig_seg] = ((pattern << 1) | (1 if dot else 0))

    def __clear_pins(self, list):
        for pin in list:
            pin.high()


    async def __usleep(self, us):
        start = time.ticks_us()
        while time.ticks_diff(time.ticks_us(), start) < us:
            await asyncio.sleep(0)

    async def __refresh_screen(self):
        pin_en_seg_map = (
            (self.__DIG1, "DIG1"),
            (self.__DIG3, "DIG3"),
            (self.__DIG2, "DIG2"),
            (self.__DIG4, "DIG4")
        )
        segments = [self.__A, self.__B, self.__C, self.__D, self.__E, self.__F, self.__G, self.__DP]
        segments.reverse()

        while True:
            for enable, seg in pin_en_seg_map:
                self.__clear_pins(segments)
                enable.high()
                for i in range(len(segments)):
                    if self.__DIGITS_SEGMENTS[seg] & (1 << i):
                        segments[i].low()
                    else:
                        segments[i].high()
                await self.__usleep(500)
                enable.low()