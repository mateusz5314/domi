from machine import Pin

import temp_sensor

if __name__ == '__main__':
    print("ThermPump software")
    CHECK_DELAY_S = 5
    OB_LED = Pin("LED", Pin.OUT)
    WATER_TEMP_PIN = Pin.board.GP0
    MOTOR_ENABLER = Pin(Pin.board.GP1, Pin.OUT)

    water_temp_sensor = temp_sensor.DS18B20(pin_num=WATER_TEMP_PIN)

    OB_LED.on()
    while True:
        # Get temperature
        try:
            water_temp = water_temp_sensor.get_temperature()

            if water_temp > 28:
                MOTOR_ENABLER.high()
            else:
                MOTOR_ENABLER.low()
            print(f"Water temperature {water_temp}\u00B0C, Motor: {MOTOR_ENABLER.value()}")
        except KeyboardInterrupt:
            break

    OB_LED.off()
    print("Closed.")
