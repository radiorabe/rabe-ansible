from __future__ import absolute_import, division, print_function

import pynetbox
from ansible.plugins.inventory import BaseInventoryPlugin

__metaclass__ = type

DOCUMENTATION = """
    name: rabify
    plugin_type: inventory
    author:
        - Lucas Bickel (@hairmare)
    short_description: Rabify NetBox inventory
    description:
        - Update data from NetBox inventory with RaBe specifics.
        - Updates ansible_host variable to the ip of the admin interface for a host.
        - Some of the code in here was based on the netbox inventory plugin in ansible.
    extends_documentation_fragment:
        - constructed
    options:
        plugin:
            description: token that ensures this is a source file for the 'rabify' plugin.
            required: True
            choices: ['rabify']
        api_endpoint:
            description: Endpoint of the NetBox API
            required: True
            env:
                - name: NETBOX_API
        validate_certs:
            description:
                - Allows connection when SSL certificates are not valid. Set to C(false) when certificates are not trusted.
            default: True
            type: boolean
        token:
            required: True
            description: NetBox token.
            env:
                # in order of precedence
                - name: NETBOX_TOKEN
                - name: NETBOX_API_KEY
        vm_admin_prefix:
            description:
                - The CIDR that VMs are expected to have their management interface in.
            default: "10.136.0.0/16"
        device_admin_prefix:
            description:
                - THE CIDR that other Devices are expected to have their management interface in.
            default: "10.128.0.0/16"
        device_interface_ignore:
            description:
                - Ignore device interfaces with this name.
            default: "IPMI"
"""


class InventoryModule(BaseInventoryPlugin):

    NAME = "rabify"

    def parse(self, inventory, loader, path, cache=True):
        super(InventoryModule, self).parse(inventory, loader, path, cache)
        self._read_config_data(path=path)

        self.api_endpoint = self.get_option("api_endpoint")
        self.api_token = self.get_option("token")
        self.validate_certs = self.get_option("validate_certs")
        self.vm_admin_prefix = self.get_option("vm_admin_prefix")
        self.device_admin_prefix = self.get_option("device_admin_prefix")
        self.device_interface_ignore = self.get_option("device_interface_ignore")

        self.inventory = inventory

        self.main()

    def main(self):
        nb = pynetbox.api(
            self.api_endpoint, token=self.api_token, ssl_verify=self.validate_certs
        )
        for host in self.inventory.hosts:
            ip = None
            try:
                ip = nb.ipam.ip_addresses.get(
                    virtual_machine=host, parent=self.vm_admin_prefix
                )
            except Exception:
                pass
            try:
                ips = nb.ipam.ip_addresses.filter(
                    device=host, parent=self.device_admin_prefix
                )
                for addr in ips:
                    if addr.interface.name != self.device_interface_ignore:
                        ip = addr
            except Exception:
                pass

            if ip:
                self.inventory.set_variable(
                    host, "ansible_host", ip.address.split("/")[0]
                )
