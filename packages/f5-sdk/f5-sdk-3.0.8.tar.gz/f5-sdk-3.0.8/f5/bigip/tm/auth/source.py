# coding=utf-8
#
# Copyright 2017 F5 Networks Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""BIG-IP® auth module

REST URI
    ``http://localhost/mgmt/tm/auth/source``

GUI Path
    ``System --> Users --> Authentication``

REST Kind
    ``tm:auth:source:*``
"""

from f5.bigip.resource import UnnamedResource


class Source(UnnamedResource):
    """BIG-IP® auth source resource"""
    def __init__(self, auth):
        super(Source, self).__init__(auth)
        self._meta_data['required_json_kind'] = 'tm:auth:source:sourcestate'
