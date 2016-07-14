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


def _get_interfaces():
    rv = []

    # We aren't interested in loopback devices since they are identical
    # across the nodes and, most the time, are useless in outer world.
    interfaces = filter(
        lambda i: not i.startswith('lo'), netifaces.interfaces())

    for name, info in zip(interfaces, map(netifaces.ifaddresses, interfaces)):
        interface = {'name': name}

        if netifaces.AF_LINK in info:
            # I don't know about the case when few MAC addresses are
            # detected on one device. So let's get the first one and
            # consider it as a device address.
            interface['mac_address'] = info[netifaces.AF_LINK][0]['addr']

        if netifaces.AF_INET in info:
            interface['ipv4_addresses'] = info[netifaces.AF_INET]

        rv.append(interface)

    return rv


def _get_inventory():
    return {
        'interfaces': _get_interfaces(),
    }


def _get_lookup_endpoint(ironic_endpoint):
    return '%s/drivers/asgard/vendor_passthru/lookup' % ironic_endpoint


def main():
    payload = {'inventory': _get_inventory()}

    # Since we anyway need to store a node UUID for doing heartbeat,
    # let's pass it for lookup if available. Passing UUID will trigger
    # more faster lookup in backend side.
    node_uuid = common.get_node_uuid()
    if node_uuid is not None:
        payload['node_uuid'] = node_uuid

    # Do lookup request.
    endpoint = _get_lookup_endpoint(common.get_ironic_endpoint())
    resp = requests.post(endpoint, json=payload)

    # Save node UUID in order to enable heartbeats.
    if resp.status_code == requests.codes.ok:
        common.set_node_uuid(resp.json['node']['uuid'])
