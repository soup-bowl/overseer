<h1 align="center">Overseer</h1>
<p align="center">
  <img src="https://github.com/soup-bowl/overseer/assets/11209477/7456aa83-eaeb-4d2c-925d-1d1798af25ba" alt="" />
</p>

Uses a **[Raspberry Pi Pico W](https://www.raspberrypi.com/products/raspberry-pi-pico/)** and a **Pimoroni [Inky Pack](https://shop.pimoroni.com/products/pico-inky-pack?variant=40044626051155)** to display select statistics from network and server resources.

## Execution 

Copy the `utils` and `.py` files to the root of the Raspberry Pi Pico, when in MicroPython mode and connected using Thonny, or another way to access the ttyACM0.

This depends on:

* ntptime

## Configuration

Configuration is done via a JSON file. [An example file is found in the repository](/config.json.example) with configuration needs specified.

## Usage

`list` format allows for a data array. Each object in the array needs a "title" to be shown on the left-hand side, and a string of lines to be shown on the rest.

For example, the following JSON:

```json
{
  "format": "list",
  "data": [
    {
      "title": "PiHole",
      "content": [
        "Block 6,869/22,037",
        "31.2% blocked"
      ]
    },
    {
      "title": "NAS",
      "content": [
        "991.78 GB/1.79 TB (54%)"
      ]
    }
  ]
}
```

Will show up as:

```
PiHole  Block 6,869/22,037
        31.2% blocked
NAS     991.78 GB/1.79 TB (54%)
```

The endpoint to send data to will be shown on-screen when the device starts up.
