from network_manager import NetworkManager
import uasyncio
import json
from pimoroni import Button
import usocket as socket

from utils.display import Display

conf = json.load(open('config.json'))

pico_screen = Display(dark_mode=True)

WIDTH, HEIGHT = pico_screen.display.get_bounds()

network_manager = NetworkManager(conf['network']['country'])
uasyncio.get_event_loop().run_until_complete(network_manager.client(conf['network']['ssid'], conf['network']['psk']))

button_a = Button(12)
button_b = Button(13)
button_c = Button(14)

pico_screen.quick_text(f"Waiting for input\n{network_manager.ifaddress()}")

addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)
print('listening on', addr)

while True:
    try:
        cl, addr = s.accept()
        print('client connected from', addr)
        request = cl.recv(1024)
        print("Response was:", request)
        request = str(request, 'utf-8')

        if "POST /" in request:
            json_start = request.find('{')
            json_end = request.rfind('}')
            if json_start != -1 and json_end != -1:
                json_data = request[json_start:json_end + 1]

                try:
                    data = json.loads(json_data)
                    print("Parsed JSON data:", data)

                    # Process screen with input data.
                    pico_screen.inform_loading()
                    pico_screen.clear()

                    pico_screen.write_timestamp()

                    for entries in data['data']:
                        for i, entry in enumerate(entries['content']):
                            pico_screen.write_line(entries['title'] if i == 0 else '', entry)

                    pico_screen.commit()

                except Exception as e:
                    print("Error parsing JSON data:", e)

            response = 'HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n'
        elif "GET / " in request or "GET / HTTP" in request:
            response = 'HTTP/1.0 200 OK\r\nContent-type: application/json\r\n\r\n'
            response += json.dumps({"message": "online"})
        else:
            response = 'HTTP/1.0 501 Not Implemented\r\nContent-type: text/html\r\n\r\n'

        cl.send(response)
        cl.close()

    except OSError as e:
        cl.close()
        print('connection closed')

