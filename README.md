# RaBe Ansible

Main [Ansible](https://ansible.com) play repository for [Radio Bern RaBe](http://rabe.ch).

This repository contains the main plays used at RaBe for managing
infrastructure. It also serves as the entrypoint to all things related to
our use of Ansible.

You may find a listing of our ansible roles in the [Ansible Galaxy](https://galaxy.ansible.com/radiorabe/).

Currently Ansible is in the PoC phase so you should not expect anything stable
from this repo.

## Usage

Check this out to somewhere that can reach the RaBe infrastructure and then run the following commands to get initialized.

```bash
pip install -r requirements.txt
export ANSIBLE_INVENTORY_PLUGINS=plugins/inventory/
export NETBOX_TOKEN=<your personal netbox token>

# if your local user doesn't match your RaBe admin user
export ANSIBLE_REMOTE_USER=<admin.user>

# grab used roles from galaxy
ansible-galaxy install -r roles/requirements.yml

# if your system does not trust the IPA provided CA
curl -k -o RaBe_CA.crt http://ipa-01.service.int.rabe.ch/ipa/config/ca.crt
export CURL_CA_BUNDLE='./RaBe_CA.crt'
```

To test if you can access all the nodes in the inventory you can run a debug play.

```bash
ansible-playbook playbooks/debug/debug.yml
```

You may now run in checkmode against all of the RaBe infra.

```bash
ansible-playbook site.yml --check --diff
```

You can run changes on individual hosts and host groups using `-l`.

```bash
# run on vm-0014 (without --check, be careful)
ansible-playbook site.yml --diff -l vm-0014

# run on all rabbitmq machines (with --check)
ansible-playbook site.yml --check --diff -l tags_rabbitmq
```

Up until now, every command was run as your admin user from the `REMOTE_USER` env
variable. If you want to run commands as root through `sudo` you need to tell
Ansible to do so using the become (`-b`) and ask password (`-K`) flags.`

```bash
ansible-playbook playbooks/debug/debug.yml -b -K
```

## Contributing

### pre-commit hook

```bash
pip install pre-commit
pip install -r requirements-dev.txt -U
pre-commit install
```

## License

AGPLv3

## Author Information

Copyright (c) 2018-2019 [Radio Bern RaBe](http://www.rabe.ch).
