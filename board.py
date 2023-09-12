import WIFI_CONFIG
from network_manager import NetworkManager
import uasyncio
import ujson
from urllib import urequest
import time
from pimoroni import Button
import jpegdec
import random
from display import Display
from remote import Remote

pico_screen = Display()

WIDTH, HEIGHT = pico_screen.display.get_bounds()

network_manager = NetworkManager(WIFI_CONFIG.COUNTRY)
uasyncio.get_event_loop().run_until_complete(network_manager.client(WIFI_CONFIG.SSID, WIFI_CONFIG.PSK))

button_a = Button(12)
button_b = Button(13)
button_c = Button(14)

def parse_qotd(text):
    text = text.split("\n")
    return (
        text[6][2:].replace("[[", "").replace("]]", "").replace("<br>", '\n').replace("<br />", '\n'),  # Quote
        text[8].split("|")[2][5:-4]                                                                     # Author
    )

# set up
pico_screen.quick_text("Press C")
time.sleep(0.5)

print("Ready for input!")

while True:
    if button_a.read():
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

        pico_screen.display.set_update_speed(1)
        pico_screen.display.update()
        
        time.sleep(0.5)
    elif button_b.read():
        pico_screen.clear()
        
        ENDPOINT = "https://en.wikiquote.org/w/api.php?format=json&action=expandtemplates&prop=wikitext&text={{{{Wikiquote:Quote%20of%20the%20day/{3}%20{2},%20{0}}}}}"
        MONTHNAMES = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        
        last_date = ""

        date = list(time.localtime())[:3]
        date.append(MONTHNAMES[date[1] - 1])

        if "{3} {2}, {0}".format(*date) == last_date:
            time.sleep(60)
            continue

        url = ENDPOINT.format(*date)
        print("Requesting URL: {}".format(url))
        j = ujson.load(urequest.urlopen(url))

        text = j['expandtemplates']['wikitext']

        text, author = parse_qotd(text)

        print(text)

        pico_screen.display.set_pen(15)
        pico_screen.display.clear()
        pico_screen.display.set_pen(0)
        pico_screen.display.text("QoTD - {2} {3} {0:04d}".format(*date), 10, 10, scale=2)
        pico_screen.display.text(text, 10, 30, wordwrap=WIDTH - 20, scale=1)
        pico_screen.display.text(author, 10, 108, scale=1)

        pico_screen.display.update()

        last_date = "{3} {2}, {0}".format(*date)
        
        time.sleep(0.5)
    elif button_c.read():
        pihole = Remote.get_pihole()

        pico_screen.clear(True)
        
        # PiHole Display
        # ---
        if pihole is not None:
            pico_screen.write_line(
                "PiHole",
                f"Block {pihole['ads_blocked_today']}/{pihole['dns_queries_today']}"
            )
            pico_screen.write_line("", f"{pihole['ads_percentage_today']}% blocked")
        else:
            pico_screen.write_line("PiHole", "OFFLINE")
        # ---
            
        pico_screen.commit()
        time.sleep(0.5)
    time.sleep(0.1)  # this number is how frequently the Pico checks for button presses

