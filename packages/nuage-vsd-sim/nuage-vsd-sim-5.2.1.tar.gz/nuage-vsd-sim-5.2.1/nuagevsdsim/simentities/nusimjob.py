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
NUSimJob
"""
from vspk import v5_0 as vsdk

from nuagevsdsim.simentities.nusimresource import NUSimResource

class NUSimJob(NUSimResource):
    """ Represents a Job

        Notes:
            Represents JOB entity. The job API accepts a command and parameters and executes the job and returns the results. Jobs API are typically used for long running tasks.
    """

    __vspk_class__ = vsdk.NUJob
    __unique_fields__ = ['externalID']
    __mandatory_fields__ = ['command']
    __default_fields__ = {
        
    }
    __get_parents__ = ['enterprise', 'gateway', 'me', 'nsgateway', 'vport']
    __create_parents__ = ['domain', 'domaintemplate', 'egressaclentrytemplate', 'egressacltemplate', 'egressadvfwdentrytemplate', 'egressadvfwdtemplate', 'enterprise', 'gateway', 'hsc', 'ingressaclentrytemplate', 'ingressacltemplate', 'ingressadvfwdentrytemplate', 'ingressadvfwdtemplate', 'ingressexternalserviceentrytemplate', 'ingressexternalservicetemplate', 'l2domain', 'l2domaintemplate', 'me', 'nsgateway', 'policygroup', 'policygrouptemplate', 'redirectiontarget', 'redirectiontargettemplate', 'vcenter', 'vcentercluster', 'vcenterhypervisor', 'virtualfirewallrule', 'vnf', 'vport', 'vrs', 'vsc', 'vsd', 'zfbrequest']

    def __init__(self):
        super(NUSimJob, self).__init__()