# Copyright 2019 Internap.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from hamcrest import assert_that, is_

from tests.arista import enable, create_vlan, create_interface_vlan, configuring_interface_vlan, \
    assert_interface_configuration, with_eapi
from tests.util.protocol_util import ProtocolTest, SshTester, with_protocol


class TestAristaNoMplsIp(ProtocolTest):
    tester_class = SshTester
    test_switch = "arista"

    @with_protocol
    def test_interface_with_no_mpls_ip(self, t):
        enable(t)
        create_vlan(t, "299")
        create_interface_vlan(t, "299")

        configuring_interface_vlan(t, "299", do="no mpls ip")

        assert_interface_configuration(t, "Vlan299", [
            "interface Vlan299",
            "   no mpls ip"
        ])

    @with_protocol
    @with_eapi
    def test_running_config_with_no_mpls_ip_via_api(self, t, api):
        enable(t)

        create_vlan(t, "299")
        create_interface_vlan(t, "299")
        configuring_interface_vlan(t, "299", do="no mpls ip")

        result = api.enable("show running-config interfaces Vlan299", strict=True, encoding="text")

        assert_that(result, is_([
            {
                "command": "show running-config interfaces Vlan299",
                "encoding": "text",
                "response": {
                    "output": "interface Vlan299\n   no mpls ip\n"
                },
                "result": {
                    "output": "interface Vlan299\n   no mpls ip\n"
                }
            }
        ]))

    @with_protocol
    def test_mpls_ip(self, t):
        enable(t)
        create_vlan(t, "299")
        create_interface_vlan(t, "299")

        configuring_interface_vlan(t, "299", do="mpls ip")

        assert_interface_configuration(t, "Vlan299", [
            "interface Vlan299"
        ])
