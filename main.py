from network_manager import NetworkManager
import uasyncio
import json
import usocket as socket
from umqtt.simple import MQTTClient

from utils.display import Display
from utils.nettime import Time

conf = json.load(open('config.json'))
disp = Display(dark_mode=conf['dark'])

network_manager = NetworkManager(conf['network']['country'])
uasyncio.get_event_loop().run_until_complete(network_manager.client(conf['network']['ssid'], conf['network']['psk']))

disp.quick_text(f"Waiting for input\n{network_manager.ifaddress()}")

# Callback for handling received messages
def on_message(topic, msg):
    print("Received message:", msg.decode('utf8'))
    data = json.loads(msg.decode('utf8'))
    disp.inform_loading()
    disp.clear()

    disp.write_info([
        conf['name'],
        network_manager.ifaddress(),
        Time.get(),
    ])

    for entries in data['data']:
        for i, entry in enumerate(entries['content']):
            disp.write_line(entries['title'] if i == 0 else '', entry)

    disp.commit()

mqtt_client = MQTTClient(conf['mqtt']['client'], conf['mqtt']['address'], port=1883)
mqtt_client.connect()
mqtt_client.set_callback(on_message)
mqtt_client.subscribe(conf['mqtt']['topic'])

while True:
    try:
        mqtt_client.check_msg()

    except OSError as e:
        cl.close()
        print('connection closed')

mqtt_client.disconnect()
