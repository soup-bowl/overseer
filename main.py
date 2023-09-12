import CONFIG
from network_manager import NetworkManager
import uasyncio
from urllib import urequest
import time
import utime
from pimoroni import Button
import jpegdec
import random

from utils.display import Display
from utils.remote import Remote
from utils.process import Process

pico_screen = Display()

WIDTH, HEIGHT = pico_screen.display.get_bounds()

network_manager = NetworkManager(CONFIG.WIFI_COUNTRY)
uasyncio.get_event_loop().run_until_complete(network_manager.client(CONFIG.WIFI_SSID, CONFIG.WIFI_PSK))

button_a = Button(12)
button_b = Button(13)
button_c = Button(14)

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
                    data = Process.display_block_data(pihole)
                    pico_screen.write_line("PiHole", data)
                else:
                    pico_screen.write_line("PiHole", "OFFLINE", 10)
                # ---
                
                # Synology NAS
                # ---
                synnas = Remote.get_synology_nas()
                if synnas is not None and 'data' in synnas:
                    pico_screen.write_line("NAS", Process.display_nas_data(synnas['data']['volumes']))
                else:
                    pico_screen.write_line("NAS", "OFFLINE", 10)
                # ---
                    
                pico_screen.commit()
                
                start_time = utime.time()

            time.sleep(0.1)
    time.sleep(0.1)



