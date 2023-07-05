<p align="center">
  <img src="https://github.com/soup-bowl/swan-monitor/assets/11209477/a592b14d-dfd5-4c6d-83ac-67953252a62b" alt="" />
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

Save as `configuration.yml` next to the **main.py**. 
