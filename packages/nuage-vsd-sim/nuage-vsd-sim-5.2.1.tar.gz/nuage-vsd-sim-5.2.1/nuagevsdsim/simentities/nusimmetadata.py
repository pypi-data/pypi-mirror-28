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
NUSimMetadata
"""
from vspk import v5_0 as vsdk

from nuagevsdsim.simentities.nusimresource import NUSimResource

class NUSimMetadata(NUSimResource):
    """ Represents a Metadata

        Notes:
            Metadata associated to a entity.
    """

    __vspk_class__ = vsdk.NUMetadata
    __unique_fields__ = ['externalID']
    __mandatory_fields__ = ['blob']
    __default_fields__ = {
        
    }
    __get_parents__ = ['addressmap', 'addressrange', 'alarm', 'allalarm', 'autodiscoveredgateway', 'avatar', 'bfdsession', 'bgpneighbor', 'bgppeer', 'bgpprofile', 'bootstrap', 'bootstrapactivation', 'bridgeinterface', 'bulkstatistics', 'certificate', 'cms', 'component', 'container', 'containerinterface', 'containerresync', 'cosremarkingpolicy', 'cosremarkingpolicytable', 'destinationurl', 'dhcpoption', 'domain', 'domaintemplate', 'dscpforwardingclassmapping', 'dscpforwardingclasstable', 'dscpremarkingpolicy', 'dscpremarkingpolicytable', 'eamconfig', 'egressaclentrytemplate', 'egressacltemplate', 'egressadvfwdentrytemplate', 'egressadvfwdtemplate', 'egressdomainfloatingipaclentrytemplate', 'egressdomainfloatingipacltemplate', 'egressfloatingipaclentrytemplate', 'egressfloatingipacltemplate', 'egressqospolicy', 'enterprise', 'enterprisenetwork', 'enterprisepermission', 'enterpriseprofile', 'enterprisesecureddata', 'enterprisesecurity', 'eventlog', 'floatingip', 'gateway', 'gatewaysecureddata', 'gatewaysecurity', 'gatewaytemplate', 'globalmetadata', 'group', 'groupkeyencryptionprofile', 'hostinterface', 'hsc', 'ikecertificate', 'ikeencryptionprofile', 'ikegateway', 'ikegatewayconfig', 'ikegatewayconnection', 'ikegatewayprofile', 'ikepsk', 'ikesubnet', 'infraconfig', 'infrastructureaccessprofile', 'infrastructuregatewayprofile', 'infrastructurevscprofile', 'ingressaclentrytemplate', 'ingressacltemplate', 'ingressadvfwdentrytemplate', 'ingressadvfwdtemplate', 'ingressexternalserviceentrytemplate', 'ingressexternalservicetemplate', 'ingressqospolicy', 'ipreservation', 'job', 'keyservermember', 'keyservermonitor', 'keyservermonitorencryptedseed', 'keyservermonitorseed', 'keyservermonitorsek', 'l2domain', 'l2domaintemplate', 'ldapconfiguration', 'license', 'link', 'location', 'ltestatistics', 'me', 'mirrordestination', 'monitoringport', 'multicastchannelmap', 'multicastlist', 'multicastrange', 'multinicvport', 'natmapentry', 'networklayout', 'networkmacrogroup', 'nexthop', 'nsgateway', 'nsgatewaytemplate', 'nsgredundancygroup', 'nsgroutingpolicybinding', 'nsport', 'nsporttemplate', 'nsredundantport', 'ospfarea', 'ospfinstance', 'ospfinterface', 'overlaymirrordestination', 'overlaymirrordestinationtemplate', 'patnatpool', 'permission', 'policydecision', 'policygroup', 'policygrouptemplate', 'port', 'porttemplate', 'publicnetwork', 'qos', 'qospolicer', 'ratelimiter', 'redirectiontarget', 'redirectiontargettemplate', 'redundancygroup', 'resync', 'routingpolicy', 'service', 'sharednetworkresource', 'site', 'staticroute', 'statistics', 'statisticscollector', 'statisticspolicy', 'subnet', 'subnettemplate', 'systemconfig', 'tca', 'tier', 'uplinkroutedistinguisher', 'user', 'vcenter', 'vcentercluster', 'vcenterdatacenter', 'vcenterhypervisor', 'virtualfirewallpolicy', 'virtualfirewallrule', 'virtualip', 'vlan', 'vlantemplate', 'vm', 'vminterface', 'vpnconnection', 'vport', 'vportmirror', 'vrs', 'vrsaddressrange', 'vrsconfig', 'vsc', 'vsd', 'vsgredundantport', 'vsp', 'zfbrequest', 'zone', 'zonetemplate']
    __create_parents__ = ['addressmap', 'addressrange', 'alarm', 'allalarm', 'autodiscoveredgateway', 'avatar', 'bfdsession', 'bgpneighbor', 'bgppeer', 'bgpprofile', 'bootstrap', 'bootstrapactivation', 'bridgeinterface', 'bulkstatistics', 'certificate', 'cms', 'component', 'container', 'containerinterface', 'containerresync', 'cosremarkingpolicy', 'cosremarkingpolicytable', 'destinationurl', 'dhcpoption', 'domain', 'domaintemplate', 'dscpforwardingclassmapping', 'dscpforwardingclasstable', 'dscpremarkingpolicy', 'dscpremarkingpolicytable', 'eamconfig', 'egressaclentrytemplate', 'egressacltemplate', 'egressadvfwdentrytemplate', 'egressadvfwdtemplate', 'egressdomainfloatingipaclentrytemplate', 'egressdomainfloatingipacltemplate', 'egressfloatingipaclentrytemplate', 'egressfloatingipacltemplate', 'egressqospolicy', 'enterprise', 'enterprisenetwork', 'enterprisepermission', 'enterpriseprofile', 'enterprisesecureddata', 'enterprisesecurity', 'eventlog', 'floatingip', 'gateway', 'gatewaysecureddata', 'gatewaysecurity', 'gatewaytemplate', 'globalmetadata', 'group', 'groupkeyencryptionprofile', 'hostinterface', 'hsc', 'ikecertificate', 'ikeencryptionprofile', 'ikegateway', 'ikegatewayconfig', 'ikegatewayconnection', 'ikegatewayprofile', 'ikepsk', 'ikesubnet', 'infraconfig', 'infrastructureaccessprofile', 'infrastructuregatewayprofile', 'infrastructurevscprofile', 'ingressaclentrytemplate', 'ingressacltemplate', 'ingressadvfwdentrytemplate', 'ingressadvfwdtemplate', 'ingressexternalserviceentrytemplate', 'ingressexternalservicetemplate', 'ingressqospolicy', 'ipreservation', 'job', 'keyservermember', 'keyservermonitor', 'keyservermonitorencryptedseed', 'keyservermonitorseed', 'keyservermonitorsek', 'l2domain', 'l2domaintemplate', 'ldapconfiguration', 'license', 'link', 'location', 'ltestatistics', 'me', 'mirrordestination', 'monitoringport', 'multicastchannelmap', 'multicastlist', 'multicastrange', 'multinicvport', 'natmapentry', 'networklayout', 'networkmacrogroup', 'nexthop', 'nsgateway', 'nsgatewaytemplate', 'nsgredundancygroup', 'nsgroutingpolicybinding', 'nsport', 'nsporttemplate', 'nsredundantport', 'ospfarea', 'ospfinstance', 'ospfinterface', 'overlaymirrordestination', 'overlaymirrordestinationtemplate', 'patnatpool', 'permission', 'policydecision', 'policygroup', 'policygrouptemplate', 'port', 'porttemplate', 'publicnetwork', 'qos', 'qospolicer', 'ratelimiter', 'redirectiontarget', 'redirectiontargettemplate', 'redundancygroup', 'resync', 'routingpolicy', 'service', 'sharednetworkresource', 'site', 'staticroute', 'statistics', 'statisticscollector', 'statisticspolicy', 'subnet', 'subnettemplate', 'systemconfig', 'tca', 'tier', 'uplinkroutedistinguisher', 'user', 'vcenter', 'vcentercluster', 'vcenterdatacenter', 'vcenterhypervisor', 'virtualfirewallpolicy', 'virtualfirewallrule', 'virtualip', 'vlan', 'vlantemplate', 'vm', 'vminterface', 'vpnconnection', 'vport', 'vportmirror', 'vrs', 'vrsaddressrange', 'vrsconfig', 'vsc', 'vsd', 'vsgredundantport', 'vsp', 'zfbrequest', 'zone', 'zonetemplate']

    def __init__(self):
        super(NUSimMetadata, self).__init__()