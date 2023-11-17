import ntptime
import time

ntptime.host = "1.europe.pool.ntp.org"

class Time:
    def get():
        try:
            ntptime.settime()
            current_time = time.localtime()
            formatted_time = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
                current_time[0], current_time[1], current_time[2],
                current_time[3], current_time[4], current_time[5]
            )
            return formatted_time
        except:
            return "Error"
