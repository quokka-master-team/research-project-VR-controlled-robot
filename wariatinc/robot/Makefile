SHELL := bash
API_TOKEN="2WcPd9AcWXROqQpB4ie1iFIPFc7_AzAQNJAEkU32RFDXMEBE"
API_URL="https://api.ngrok.com/tunnels"
SSH_USER="robot"
SSH_KEY_FILE="~/.ssh/id_rsa"
SUDO_PASS="bot"

create_hostini:
	@echo "1. Creating hosts.ini file"
	@tunnel_info=$$(curl -s -X GET -H "Authorization: Bearer $(API_TOKEN)" -H "Ngrok-Version: 2" "$(API_URL)" | jq -r '.tunnels[] | select(.forwards_to == "localhost:22")'); \
	echo "tunnel_info: $$tunnel_info"; \
	host_port=$$(echo "$$tunnel_info" | jq -r '.public_url' | awk -F ':' '{ host = $$1; for (i = 2; i < NF; i++) host = host ":" $$i; port = $$NF; print host, port }'); \
	read -r host port <<< "$$host_port"; \
	host=$${host#tcp://};\
	sed -i "2s/.*/$$host:$$port/" hosts.ini
	@echo "2. hosts.ini file created"

config: create_hostini
	@echo "2.1 Run playbook config.yml"
	@ansible-playbook -i hosts.ini playbooks/config.yml -u $(SSH_USER) --private-key $(SSH_KEY_FILE) -e "ansible_sudo_pass=$(SUDO_PASS)" --tags "wireguard" 

config_ovh: 
	@echo "2.1 Run playbook config.yml"
	@ansible-playbook -i hosts.ini playbooks/config.yml --tags "ssh"

# 	echo -en "[nuc]\n$$host:$$port" > hosts.i[defaults]
host_key_checking = falseni
# @ansible-playbook -i hosts.ini playbooks/config.yml -u ubuntu --private-key $(SSH_KEY_FILE) -e "ansible_sudo_pass=bjFvqWNzuRmZ" --tags "packages"
