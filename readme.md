<h1 align="center">Swan Monitor</h1>
<p align="center">
  <img src="https://github.com/soup-bowl/swan-monitor/assets/11209477/a592b14d-dfd5-4c6d-83ac-67953252a62b" alt="" />
</p>

Uses a Pimoroni [Inky pHAT](https://shop.pimoroni.com/products/inky-phat?variant=12549254905939) display on a wall-mounted Raspberry Pi to show select statistics from network and server resources.

## Execution 

Installation is done like all other Python packages. Recommended to install & execute within a **venv**. 

```bash
python main.py --simulate --type phatssd1608 --colour yellow
```

To display on a Inky, omit `--simulate`.

## Configuration

Swan is configured by a `configuration.yml` file present in the main execution point.

### Example

```yml
name: Example Network
stages:
  - label: PiHole
    type: pihole
    address: "192.168.1.2"
    auth: YourKeyForPiHoleAPI
  - label: Server
    type: isup
    address: coolthing.com
  - label: LinodeServer
    type: linode
    address: instance_id
    auth: api_token
  - label: NAS
    type: synology
    address: 192.168.1.5:5000
    user: api
    auth: api_token
```

