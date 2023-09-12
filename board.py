import CONFIG
from network_manager import NetworkManager
import uasyncio
from urllib import urequest
import time
import utime
from pimoroni import Button
import jpegdec
import random

from display import Display
from remote import Remote

pico_screen = Display()

WIDTH, HEIGHT = pico_screen.display.get_bounds()

network_manager = NetworkManager(CONFIG.WIFI_COUNTRY)
uasyncio.get_event_loop().run_until_complete(network_manager.client(CONFIG.WIFI_SSID, CONFIG.WIFI_PSK))

button_a = Button(12)
button_b = Button(13)
button_c = Button(14)

def format_bytes(num):
    units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
    i = 0

    while num >= 1024 and i < len(units)-1:
        num /= 1024
        i += 1

    formatted_num = '{:.2f}'.format(num)

    result = f"{formatted_num} {units[i]}"

    return result


# set up
pico_screen.quick_text("Ready")
time.sleep(0.5)

print("Ready for input!")

while True:
    if button_a.read():
        pico_screen.inform_loading()
        pico_screen.clear()
        
        FILENAME = "placekitten.jpg"
        ENDPOINT = "http://placekitten.com/{0}/{1}"
        
        url = ENDPOINT.format(WIDTH, HEIGHT + random.randint(0, 10))
        print("Requesting URL: {}".format(url))
        socket = urequest.urlopen(url)

        # Load the image data into RAM (if you have enough!)
        data = bytearray(1024 * 10)
        socket.readinto(data)
        socket.close()

        jpeg = jpegdec.JPEG(pico_screen.display)
        jpeg.open_RAM(data)
        jpeg.decode(0, 0)

        pico_screen.display.set_pen(15)
        pico_screen.display.rectangle(0, HEIGHT - 14, WIDTH, 14)

        pico_screen.display.set_pen(0)
        pico_screen.display.text(url, 5, HEIGHT - 9, scale=1)

        pico_screen.commit()
        
        time.sleep(0.5)
    elif button_b.read():
        pico_screen.inform_loading()
        pico_screen.clear()
        
        jpeg = jpegdec.JPEG(pico_screen.display)
        jpeg.open_file("fine.jpg")
        jpeg.decode()
        
        pico_screen.commit()
        
        time.sleep(0.5)
    elif button_c.read():
        start_time = utime.time() + 350 # Invalidate the first run - cheap trick.

        while True:
            if button_a.is_pressed or button_b.is_pressed:
                    break
            
            if abs(start_time - utime.time()) > 300: 
                pico_screen.inform_loading()
                pico_screen.clear(True)
                
                # PiHole Display
                # ---
                pihole = Remote.get_pihole()
                if pihole is not None:
                    pico_screen.write_line(
                        "PiHole",
                        f"Block {pihole['ads_blocked_today']}/{pihole['dns_queries_today']}"
                    )
                    pico_screen.write_line("", f"{pihole['ads_percentage_today']}% blocked")
                else:
                    pico_screen.write_line("PiHole", "OFFLINE", 10)
                # ---
                
                # Synology NAS
                # ---
                synnas = Remote.get_synology_nas()
                if synnas is not None and 'data' in synnas:
                    total_volume = 0
                    used_volume = 0
                    for volume in synnas['data']['volumes']:
                        total_volume += int(volume['size']['total'])
                        used_volume += int(volume['size']['used'])

                    percentage_used = (used_volume / total_volume) * 100

                    pico_screen.write_line(
                        "NAS",
                        f"{format_bytes(used_volume)} / {format_bytes(total_volume)} ({percentage_used:.0f}%)"
                    )
                else:
                    pico_screen.write_line("NAS", "OFFLINE", 10)
                # ---
                    
                pico_screen.commit()
                
                start_time = utime.time()

            time.sleep(0.1)
    time.sleep(0.1)



