<p align="center">
  <img src="https://github.com/soup-bowl/swan-monitor/assets/11209477/66d4b37e-a73e-4afd-b589-c9f6e7ca97a3" alt="" />
</p>

Simulate with

```bash
python main.py --simulate --type phatssd1608 --colour yellow
```

## Configuration Schema

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
```

Save as `configuration.yml` next to the **main.py**. 
