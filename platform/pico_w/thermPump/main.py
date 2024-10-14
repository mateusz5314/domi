import asyncio
from machine import Pin

import temp_sensor
import display

async def main():
    print("ThermPump software")
    MOTOR_ENABLE_THR = 28
    MOTOR_DISABLE_THR = 27
    CHECK_DELAY_S = 1
    OB_LED = Pin("LED", Pin.OUT)
    WATER_TEMP_PIN = Pin.board.GP0
    MOTOR_ENABLER = Pin(Pin.board.GP1, Pin.OUT, Pin.PULL_UP)

    try:
        water_temp_sensor = temp_sensor.DS18B20(pin_num=WATER_TEMP_PIN)
    except Exception as e:
        print("Could not find DS18B20 device.")
        return
    temp_display = display.F5463BH(Pin.board.GP20, Pin.board.GP16, Pin.board.GP12, Pin.board.GP10,
                                   Pin.board.GP9, Pin.board.GP19, Pin.board.GP13, Pin.board.GP11,
                                   Pin.board.GP15, Pin.board.GP21, Pin.board.GP18,
                                   Pin.board.GP17, Pin.board.GP14)

    OB_LED.on()
    while True:
        try:
            water_temp = await water_temp_sensor.get_temperature()

            if water_temp > MOTOR_ENABLE_THR:
                MOTOR_ENABLER.high()
            elif water_temp < MOTOR_DISABLE_THR:
                MOTOR_ENABLER.low()
            await asyncio.sleep(0.0005)
            print(f"Water temperature {water_temp}\u00B0C, Motor: {MOTOR_ENABLER.value()}")
            formatted_number = f"{water_temp:02.2f}"
            await temp_display.write(int(formatted_number[0]), int(formatted_number[1]),
                                     int(formatted_number[3]), int(formatted_number[4]), dot2=True)
            await asyncio.sleep(CHECK_DELAY_S)
        except KeyboardInterrupt:
            break

    OB_LED.off()
    print("Closed.")

if __name__ == '__main__':
    asyncio.run(main())