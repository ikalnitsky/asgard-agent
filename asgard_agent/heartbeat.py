# Copyright (c) 2016 Mirantis, Inc
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import netifaces
import requests

from asgard_agent import common
from asgard_agent import exceptions


def _normalize_mac(mac_address):
    return mac_address.lower().replace('-', ':')


def _get_ssh_address():
    if 'BOOTIF' not in common.KERNEL_PARAMS:
        raise exceptions.BootInterfaceNotFound(
            'BOOTIF option is not passed to Linux kernel. Your PXE '
            'firmware either misconfigured or does not support it.')

    # Strip out first 3 characters because they are PXE related stuff.
    # Example: 01-08-00-27-33-70-c4 -> 08-00-27-33-70-c4
    bootif = _normalize_mac(common.KERNEL_PARAMS['BOOTIF'][3:])

    for name in netifaces.interfaces():
        info = netifaces.ifaddresses(name)
        if bootif == _normalize_mac(info[netifaces.AF_LINK][0]['addr']):
            try:
                # So far Ironic doesn't support multiple IP addresses.
                # Pick up first one and pray. :)
                return info[netifaces.AF_INET][0]['addr']
            except (KeyError, IndexError):
                raise exceptions.IPAddressNotFound(
                    'IP address on interface with MAC %s not found'
                    % bootif)

    raise exceptions.BootInterfaceNotFound(
        'Network interface with MAC address %s was not found.' % bootif)


def main():
    endpoint = '%s/nodes/%s/vendor_passthru/heartbeat' % (
        common.get_ironic_endpoint(),
        common.get_node_uuid()
    )

    requests.post(endpoint, json={
        'callback_url': 'ssh://%s' % _get_ssh_address()
    })
