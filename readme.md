<h1 align="center">Overseer</h1>
<p align="center">
  <img src="https://github.com/soup-bowl/overseer/assets/11209477/7456aa83-eaeb-4d2c-925d-1d1798af25ba" alt="" />
</p>

Uses a **[Raspberry Pi Pico W](https://www.raspberrypi.com/products/raspberry-pi-pico/)** and a **Pimoroni [Inky Pack](https://shop.pimoroni.com/products/pico-inky-pack?variant=40044626051155)** to display select statistics from network and server resources.

## Execution 

Copy the `utils` and `.py` files to the root of the Raspberry Pi Pico, when in MicroPython mode and connected using Thonny, or another way to access the ttyACM0.

`urllib` will also need to be installed via Thonny or mip.

## Configuration

Configuration is done via a JSON file. [An example file is found in the repository](/config.json.example) with configuration needs specified.
