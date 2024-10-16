import asyncio
from machine import Pin

import temp_sensor
import display
import wifi_adapter
import CRestApi
import data_manager

async def main():
    print("ThermPump software")
    STATIC_IF_CFG = ('192.168.10.2', '255.255.255.0', '192.168.10.1', '192.168.10.1')
    HOSTNAME = "poolthermpump"
    SEND_DATA_OVER_WIFI = True
    MOTOR_ENABLE_THR = 28
    MOTOR_DISABLE_THR = 27
    CHECK_DELAY_S = 1
    OB_LED = Pin("LED", Pin.OUT)
    WATER_TEMP_PIN = Pin.board.GP0
    MOTOR_ENABLER = Pin(Pin.board.GP1, Pin.OUT, Pin.PULL_UP)

    data = data_manager.tp_data("Pool solar therm pump")
    try:
        water_temp_sensor = temp_sensor.DS18B20(pin_num=WATER_TEMP_PIN)
    except Exception as e:
        print("Could not find DS18B20 device.")
        return
    temp_display = display.F5463BH(Pin.board.GP20, Pin.board.GP16, Pin.board.GP12, Pin.board.GP10,
                                   Pin.board.GP9, Pin.board.GP19, Pin.board.GP13, Pin.board.GP11,
                                   Pin.board.GP15, Pin.board.GP21, Pin.board.GP18,
                                   Pin.board.GP17, Pin.board.GP14)

    ext_sender = None
    if SEND_DATA_OVER_WIFI:
        ext_sender = wifi_adapter.wifi_adapter()
        await ext_sender.connect(static_if_cfg=STATIC_IF_CFG, hostname=HOSTNAME)
        if ext_sender.is_connected():
            ext_api = CRestApi.CRestApi(port=80)
            ext_api.add_route(CRestApi.RestMethods.GET, '/data', data.get_json_str)
            ext_api.add_route(CRestApi.RestMethods.POST, '/data', data.update_time)
            await ext_api.start()

    OB_LED.on()
    while True:
        try:
            data.update_temp(await water_temp_sensor.get_temperature())
            if data.get_temp() > MOTOR_ENABLE_THR:
                data.update_motor(1)
            elif data.get_temp() < MOTOR_DISABLE_THR:
                data.update_motor(0)

            MOTOR_ENABLER.value(data.get_motor_state())
            await asyncio.sleep(0.0005)
            print(f"Water temperature {data.get_temp()}\u00B0C, Motor: {data.get_motor_state()}")

            await temp_display.write(*data.get_formatted_temp_digits(),
                                     dot2=True, dot4=True if ext_sender is not None and
                                                             ext_sender.is_connected()
                                                          else False)
            await asyncio.sleep(CHECK_DELAY_S)
        except KeyboardInterrupt:
            break

    OB_LED.off()
    print("Closed.")

if __name__ == '__main__':
    asyncio.run(main())