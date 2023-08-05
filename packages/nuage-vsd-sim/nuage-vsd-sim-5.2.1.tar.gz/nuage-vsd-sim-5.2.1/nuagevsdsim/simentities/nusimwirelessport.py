# -*- coding: utf-8 -*-
# BSD 3-Clause License
#
# Copyright (c) 2017, Nokia
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
NUSimWirelessPort
"""
from vspk import v5_0 as vsdk

from nuagevsdsim.simentities.nusimresource import NUSimResource

class NUSimWirelessPort(NUSimResource):
    """ Represents a WirelessPort

        Notes:
            Represents a wireless (WiFi) interface configured on a Network Service Gateway (NSG) instance.  The WirelessPort instance may map to a physical WiFi card or a WiFi port.
    """

    __vspk_class__ = vsdk.NUWirelessPort
    __unique_fields__ = ['name', 'physicalName']
    __mandatory_fields__ = ['name', 'physicalName', 'wifiFrequencyBand', 'wifiMode', 'portType', 'countryCode', 'frequencyChannel']
    __default_fields__ = {
        'wifiFrequencyBand': 'FREQ_2_4_GHZ',
        'wifiMode': 'WIFI_B_G_N',
        'portType': 'ACCESS',
        'frequencyChannel': 'CH_0'
    }
    __get_parents__ = ['nsgateway']
    __create_parents__ = ['nsgateway']

    def __init__(self):
        super(NUSimWirelessPort, self).__init__()