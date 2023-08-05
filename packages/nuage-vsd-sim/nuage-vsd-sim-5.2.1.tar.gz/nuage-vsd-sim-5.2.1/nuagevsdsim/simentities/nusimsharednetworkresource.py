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
NUSimSharedNetworkResource
"""
from vspk import v5_0 as vsdk

from nuagevsdsim.simentities.nusimresource import NUSimResource

class NUSimSharedNetworkResource(NUSimResource):
    """ Represents a SharedNetworkResource

        Notes:
            This defines shared infrastructure resources that are created by user with CSPROOT role. These resources can be used by all the enterprises in the data center for various purposes. Examples of  shared resources are public subnet, floating subnet, public L2 domain.
    """

    __vspk_class__ = vsdk.NUSharedNetworkResource
    __unique_fields__ = ['externalID']
    __mandatory_fields__ = ['name', 'address', 'netmask', 'type']
    __default_fields__ = {
        
    }
    __get_parents__ = ['enterprise', 'me', 'patmapper']
    __create_parents__ = ['me']

    def __init__(self):
        super(NUSimSharedNetworkResource, self).__init__()