<h1 align="center">Overseer</h1>
<p align="center">
  <img src="https://github.com/soup-bowl/overseer/assets/11209477/59c0fc8f-0725-4775-bc2c-4e0891a47236" alt="" />
</p>



Uses a **[Raspberry Pi Pico W](https://www.raspberrypi.com/products/raspberry-pi-pico/)** and a **Pimoroni [Inky Pack](https://shop.pimoroni.com/products/pico-inky-pack?variant=40044626051155)** to display on a wall-mounted Raspberry Pi to show select statistics from network and server resources.

## Execution 

Copy the `utils` and `.py` files to the root of the Raspberry Pi Pico, when in MicroPython mode and connected using Thonny, or another way to access the ttyACM0.

`urllib` will also need to be installed via Thonny or mip.

## Configuration

Configuration is done via a JSON file. [An example file is found in the repository](/config.json.example) with configuration needs specified.

The system supports the following displays for the network monitor screen:

* Pihole view - Displays block count & percentage.
* Synology NAS - Displays overall storage utilisation & percentage.
* Prometheus - Gets information for a job (user in config) and shows CPU & RAM utilisation, and temperature.
