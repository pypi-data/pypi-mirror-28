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

from f5.bigip.resource import AsmResource
from f5.bigip.resource import Collection


class Json_Profiles_s(Collection):
    """BIG-IP® ASM Json-Profiles sub-collection.

    Due to the bug that prevents from creating this object in 11.5.4 Final,
    I am disabling this for anything lower than 11.6.0.
    This will be subject to change at some point
    """
    def __init__(self, policy):
        super(Json_Profiles_s, self).__init__(policy)
        self._meta_data['minimum_version'] = '11.6.0'
        self._meta_data['object_has_stats'] = False
        self._meta_data['allowed_lazy_attributes'] = [Json_Profile]
        self._meta_data['required_json_kind'] = 'tm:asm:policies:json-profiles:json-profilecollectionstate'
        self._meta_data['attribute_registry'] = {
            'tm:asm:policies:json-profiles:json-profilestate': Json_Profile
        }


class Json_Profile(AsmResource):
    """BIG-IP® ASM Json-Profile resource."""
    def __init__(self, json_profiles_s):
        super(Json_Profile, self).__init__(json_profiles_s)
        self._meta_data['required_json_kind'] = 'tm:asm:policies:json-profiles:json-profilestate'
