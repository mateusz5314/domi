from machine import RTC

class tp_data:
    def __init__(self, name):
        self.rtc = RTC()
        self.temp = 0
        self.motor_e = 0
        self.name = name

    def update_time(self, date_time):
        try:
            obj = date_time['datetime']
            year = int(obj['year'])
            month = int(obj['month'])
            day = int(obj['day'])
            weekday = int(obj['weekday'])
            hour = int(obj['hour'])
            minute = int(obj['minute'])
            second = int(obj['second'])
            microsecond = int(obj['microsecond']) / 1000
        except Exception as e:
            print(f"Incoming datetime corrupted: {e}")
            return {"status": False, "reason": f"Incoming datetime corrupted {e}"}
        self.rtc.datetime((year,
                           month,
                           day,
                           weekday,
                           hour,
                           minute,
                           second,
                           microsecond))
        return {"status": True, "reason": "Date and time updated"}

    def update_temp(self, temp):
        self.temp = temp

    def update_motor(self, motor_e):
        self.motor_e = motor_e

    def get_name(self):
        return self.name

    def get_motor_state(self):
        return self.motor_e

    def get_temp(self):
        return self.temp

    def get_formatted_temp_digits(self):
        formatted_temp = f"{self.temp:02.2f}"
        return (int(formatted_temp[0]), int(formatted_temp[1]),
                int(formatted_temp[3]), int(formatted_temp[4]))

    def get_current_time(self):
        ct = self.rtc.datetime()
        formatted_time = f"{ct[0]:04}-{ct[1]:02}-{ct[2]:02} {ct[4]:02}:{ct[5]:02}:{ct[6]:02}"
        return formatted_time

    def get_json_str(self):
        return {
            "name": self.get_name(),
            "temp": self.get_temp(),
            "motor": self.get_motor_state(),
            "time": self.get_current_time()
        }
