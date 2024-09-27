import asyncio
import machine
import onewire
import ds18x20

class DS18B20:
    def __init__(self, pin_num):
        self.conversion_time_s = 0.750
        self.ds_pin = machine.Pin(pin_num)
        self.ds_sensor = ds18x20.DS18X20(onewire.OneWire(self.ds_pin))

        # Scan for DS18B20 devices
        self.roms = self.ds_sensor.scan()
        if not self.roms:
            raise Exception("DS18B20 not found!")
        print("DS18B20 found:", ["".join(f"{byte:02X}" for byte in device) for device in self.roms])

    async def get_temperature(self):
        """
        Returns temperature from first attached DS18B20 sensor.
        """
        self.ds_sensor.convert_temp()
        await asyncio.sleep(self.conversion_time_s)
        temperature = self.ds_sensor.read_temp(self.roms[0])
        return temperature
