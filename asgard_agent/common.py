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

import io
import os

from asgard_agent import exceptions


_UUID = os.path.join('/etc', 'ironic-uuid')


def set_node_uuid(uuid):
    with io.open(_UUID, 'wt', encoding='utf-8') as f:
        f.write(uuid)


def get_node_uuid():
    try:
        with io.open(_UUID, 'rt', encoding='utf-8') as f:
            return f.read().strip()
    except IOError:
        return None


def get_ironic_endpoint():
    if 'ironic_api_url' not in KERNEL_PARAMS:
        raise exceptions.IronicEndpointNotFound(
            'ironic_api_url option is not passed to Linux kernel.')

    endpoint = KERNEL_PARAMS['ironic_api_url']
    if endpoint.endswith('/'):
        endpoint = endpoint[:-1]
    return endpoint


def _get_kernel_params():
    rv = {}

    with io.open('/proc/cmdline', 'r', encoding='utf-8') as f:
        cmdline = f.read().strip()

    for param in cmdline.split():
        kv = param.split('=')
        rv[kv[0]] = kv[1] if len(kv) > 1 else True

    return rv
KERNEL_PARAMS = _get_kernel_params()
