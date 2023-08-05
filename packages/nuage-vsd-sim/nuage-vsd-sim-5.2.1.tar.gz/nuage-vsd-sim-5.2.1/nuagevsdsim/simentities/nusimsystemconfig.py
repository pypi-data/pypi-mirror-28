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
NUSimSystemConfig
"""
from vspk import v5_0 as vsdk

from nuagevsdsim.simentities.nusimresource import NUSimResource

class NUSimSystemConfig(NUSimResource):
    """ Represents a SystemConfig

        Notes:
            The system configuration which can be dynamically managed using rest api.
    """

    __vspk_class__ = vsdk.NUSystemConfig
    __unique_fields__ = ['externalID']
    __mandatory_fields__ = []
    __default_fields__ = {
        'AARFlowStatsInterval': 30,
        'AARProbeStatsInterval': 30,
        'ZFBRequestRetryTimer': 30,
        'PGIDLowerLimit': 65536,
        'PGIDUpperLimit': 2147483647,
        'VMCacheSize': 5000,
        'VMPurgeTime': 60,
        'VMResyncDeletionWaitTime': 2,
        'VMResyncOutstandingInterval': 1000,
        'VMUnreachableCleanupTime': 7200,
        'VMUnreachableTime': 3600,
        'VNFTaskTimeout': 3600,
        'VPortInitStatefulTimer': 300,
        'VSSStatsInterval': 30,
        'pageMaxSize': 500,
        'pageSize': 50,
        'accumulateLicensesEnabled': False,
        'perDomainVlanIdEnabled': False,
        'virtualFirewallRulesEnabled': False,
        'elasticClusterName': 'nuage_elasticsearch',
        'allowEnterpriseAvatarOnNSG': True,
        'csprootAuthenticationMethod': 'LOCAL',
        'statsMinDuration': 2592000,
        'stickyECMPIdleTimeout': 0,
        'attachProbeToIPsecNPM': False,
        'attachProbeToVXLANNPM': False,
        'subnetResyncInterval': 10,
        'dynamicWANServiceDiffTime': 1
    }
    __get_parents__ = ['me']
    __create_parents__ = []

    def __init__(self):
        super(NUSimSystemConfig, self).__init__()