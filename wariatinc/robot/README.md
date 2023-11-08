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