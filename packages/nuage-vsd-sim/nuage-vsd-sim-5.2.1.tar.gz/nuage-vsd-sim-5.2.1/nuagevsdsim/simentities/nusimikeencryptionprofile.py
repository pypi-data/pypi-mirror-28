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
NUSimIKEEncryptionprofile
"""
from vspk import v5_0 as vsdk

from nuagevsdsim.simentities.nusimresource import NUSimResource

class NUSimIKEEncryptionprofile(NUSimResource):
    """ Represents a IKEEncryptionprofile

        Notes:
            Represents an IKE Profile
    """

    __vspk_class__ = vsdk.NUIKEEncryptionprofile
    __unique_fields__ = ['externalID']
    __mandatory_fields__ = []
    __default_fields__ = {
        'DPDInterval': 0,
        'DPDMode': 'REPLY_ONLY',
        'DPDTimeout': 0,
        'IPsecAuthenticationAlgorithm': 'HMAC_SHA256',
        'IPsecEncryptionAlgorithm': 'AES256',
        'IPsecSALifetime': 3600,
        'IPsecSAReplayWindowSize': 'WINDOW_SIZE_32',
        'ISAKMPAuthenticationMode': 'PRE_SHARED_KEY',
        'ISAKMPDiffieHelmanGroupIdentifier': 'GROUP_5_1536_BIT_DH',
        'ISAKMPEncryptionAlgorithm': 'AES256',
        'ISAKMPEncryptionKeyLifetime': 28800,
        'ISAKMPHashAlgorithm': 'SHA256'
    }
    __get_parents__ = ['enterprise']
    __create_parents__ = ['enterprise']

    def __init__(self):
        super(NUSimIKEEncryptionprofile, self).__init__()