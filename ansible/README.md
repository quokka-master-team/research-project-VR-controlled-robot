# Ansible Collection - wariatinc.robot

Documentation for the collection.

## Command for developers

### Connect using ssh to OVH server
```
ssh devuser@vps-035c50e6.vps.ovh.net
```
### Connect using ssh to NUC server
```
ssh robot@vps-035c50e6.vps.ovh.net -p 1024
```
### Connect using xrdp to OVH server
```
vps-035c50e6.vps.ovh.net:3389

name: devuser
password: ***

name: lszarecki
password: ***

name: jkoniuszewski
password: ***
```
### Connect using xrdp to NUC server
```
vps-035c50e6.vps.ovh.net:3390

name: robot
password: ***

name: lszarecki
password: ***

name: jkoniuszewski
password: ***
```

## Opening port forwarding

```
ansible-playbook -i hosts.ini playbooks/config.yml --tags "nft" --limit ovh_server
```

## Creating users on server
```
ansible-playbook -i hosts.ini playbooks/config.yml --tags="users" -vv --limit ovh_server
```

## Get packages on server
```
ansible-playbook -i hosts.ini playbooks/config.yml --tags "packages" --limit ovh_server
```

## Wireguard peer config with access to public internet
```
[Interface]
PrivateKey = << peer private key >>
Address = 10.0.0.5/32
DNS = 1.0.0.1, 2606:4700:4700::1001, 8.8.8.8, 2001:4860:4860::8844
PostUp = ping -c1 10.0.0.1

[Peer]
PublicKey = << vpn public key >>
AllowedIPs = 10.0.0.1/32, 0.0.0.0/0, ::/0
Endpoint = vps-035c50e6.vps.ovh.net:51820
PersistentKeepalive = 25
```

## Wireguard server config
```
# Ansible managed
[Interface]
Address = 10.0.0.1/24
ListenPort = 51820
SaveConfig = true
PrivateKey = << server private key >>

[Peer]
PublicKey = << peer public key >>
AllowedIPs = 10.0.0.9

# Other peers to wireguard tunnel
[Peer]
# lukasz
PublicKey = << peer public key >>
AllowedIPs = 10.0.0.2/32

[Peer]
# hubert
PublicKey = << peer public key >>
AllowedIPs = 10.0.0.3/32

[Peer]
# michal
PublicKey = << peer public key >>
AllowedIPs = 10.0.0.4/32

[Peer]
# gcp
PublicKey = aUsa4hoiORbATGsjmRWK6H62xVlMlUaF4fzFrQWyXTs=
AllowedIPs = 10.0.0.8/32
```