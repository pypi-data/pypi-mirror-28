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
import glob
import os

from .nusimroot import NUSimRoot
from .nusimresource import NUSimResource

from .nusimaddressmap import NUSimAddressMap
from .nusimaddressrange import NUSimAddressRange
from .nusimaggregatemetadata import NUSimAggregateMetadata
from .nusimalarm import NUSimAlarm
from .nusimallalarm import NUSimAllAlarm
from .nusimapplication import NUSimApplication
from .nusimapplicationbinding import NUSimApplicationBinding
from .nusimapplicationperformancemanagement import NUSimApplicationperformancemanagement
from .nusimapplicationperformancemanagementbinding import NUSimApplicationperformancemanagementbinding
from .nusimautodiscovercluster import NUSimAutoDiscoverCluster
from .nusimautodiscovereddatacenter import NUSimAutodiscovereddatacenter
from .nusimautodiscoveredgateway import NUSimAutoDiscoveredGateway
from .nusimautodiscoverhypervisorfromcluster import NUSimAutoDiscoverHypervisorFromCluster
from .nusimavatar import NUSimAvatar
from .nusimbfdsession import NUSimBFDSession
from .nusimbgpneighbor import NUSimBGPNeighbor
from .nusimbgppeer import NUSimBGPPeer
from .nusimbgpprofile import NUSimBGPProfile
from .nusimbootstrap import NUSimBootstrap
from .nusimbootstrapactivation import NUSimBootstrapActivation
from .nusimbrconnection import NUSimBRConnection
from .nusimbridgeinterface import NUSimBridgeInterface
from .nusimbulkstatistics import NUSimBulkStatistics
from .nusimcaptiveportalprofile import NUSimCaptivePortalProfile
from .nusimcertificate import NUSimCertificate
from .nusimcloudmgmtsystem import NUSimCloudMgmtSystem
from .nusimcommand import NUSimCommand
from .nusimconnectionendpoint import NUSimConnectionendpoint
from .nusimcontainer import NUSimContainer
from .nusimcontainerinterface import NUSimContainerInterface
from .nusimcontainerresync import NUSimContainerResync
from .nusimcosremarkingpolicy import NUSimCOSRemarkingPolicy
from .nusimcosremarkingpolicytable import NUSimCOSRemarkingPolicyTable
from .nusimcsnatpool import NUSimCSNATPool
from .nusimctranslationmap import NUSimCTranslationMap
from .nusimcustomproperty import NUSimCustomProperty
from .nusimdemarcationservice import NUSimDemarcationService
from .nusimdestinationurl import NUSimDestinationurl
from .nusimdhcpoption import NUSimDHCPOption
from .nusimdiskstat import NUSimDiskStat
from .nusimdomain import NUSimDomain
from .nusimdomainfipacltemplate import NUSimDomainFIPAclTemplate
from .nusimdomainfipacltemplateentry import NUSimDomainFIPAclTemplateEntry
from .nusimdomaintemplate import NUSimDomainTemplate
from .nusimdscpforwardingclassmapping import NUSimDSCPForwardingClassMapping
from .nusimdscpforwardingclasstable import NUSimDSCPForwardingClassTable
from .nusimdscpremarkingpolicy import NUSimDSCPRemarkingPolicy
from .nusimdscpremarkingpolicytable import NUSimDSCPRemarkingPolicyTable
from .nusimducgroup import NUSimDUCGroup
from .nusimducgroupbinding import NUSimDUCGroupBinding
from .nusimegressaclentrytemplate import NUSimEgressACLEntryTemplate
from .nusimegressacltemplate import NUSimEgressACLTemplate
from .nusimegressadvfwdentrytemplate import NUSimEgressAdvFwdEntryTemplate
from .nusimegressadvfwdtemplate import NUSimEgressAdvFwdTemplate
from .nusimegressqospolicy import NUSimEgressQOSPolicy
from .nusimenterprise import NUSimEnterprise
from .nusimenterprisenetwork import NUSimEnterpriseNetwork
from .nusimenterprisepermission import NUSimEnterprisePermission
from .nusimenterpriseprofile import NUSimEnterpriseProfile
from .nusimenterprisesecureddata import NUSimEnterpriseSecuredData
from .nusimenterprisesecurity import NUSimEnterpriseSecurity
from .nusimeventlog import NUSimEventLog
from .nusimfirewallacl import NUSimFirewallAcl
from .nusimfirewallrule import NUSimFirewallRule
from .nusimfloatingip import NUSimFloatingIp
from .nusimfloatingipacltemplate import NUSimFloatingIPACLTemplate
from .nusimfloatingipacltemplateentry import NUSimFloatingIPACLTemplateEntry
from .nusimgateway import NUSimGateway
from .nusimgatewaysecureddata import NUSimGatewaySecuredData
from .nusimgatewaysecurity import NUSimGatewaySecurity
from .nusimgatewaytemplate import NUSimGatewayTemplate
from .nusimglobalmetadata import NUSimGlobalMetadata
from .nusimgroup import NUSimGroup
from .nusimgroupkeyencryptionprofile import NUSimGroupKeyEncryptionProfile
from .nusimhostinterface import NUSimHostInterface
from .nusimhsc import NUSimHSC
from .nusimikecertificate import NUSimIKECertificate
from .nusimikeencryptionprofile import NUSimIKEEncryptionprofile
from .nusimikegateway import NUSimIKEGateway
from .nusimikegatewayconfig import NUSimIKEGatewayConfig
from .nusimikegatewayconnection import NUSimIKEGatewayConnection
from .nusimikegatewayprofile import NUSimIKEGatewayProfile
from .nusimikepsk import NUSimIKEPSK
from .nusimikesubnet import NUSimIKESubnet
from .nusiminfrastructureaccessprofile import NUSimInfrastructureAccessProfile
from .nusiminfrastructureconfig import NUSimInfrastructureConfig
from .nusiminfrastructuregatewayprofile import NUSimInfrastructureGatewayProfile
from .nusiminfrastructurevscprofile import NUSimInfrastructureVscProfile
from .nusimingressaclentrytemplate import NUSimIngressACLEntryTemplate
from .nusimingressacltemplate import NUSimIngressACLTemplate
from .nusimingressadvfwdentrytemplate import NUSimIngressAdvFwdEntryTemplate
from .nusimingressadvfwdtemplate import NUSimIngressAdvFwdTemplate
from .nusimingressexternalservicetemplate import NUSimIngressExternalServiceTemplate
from .nusimingressexternalservicetemplateentry import NUSimIngressExternalServiceTemplateEntry
from .nusimingressqospolicy import NUSimIngressQOSPolicy
from .nusimipreservation import NUSimIPReservation
from .nusimjob import NUSimJob
from .nusimkeyservermember import NUSimKeyServerMember
from .nusimkeyservermonitor import NUSimKeyServerMonitor
from .nusimkeyservermonitorencryptedseed import NUSimKeyServerMonitorEncryptedSeed
from .nusimkeyservermonitorseed import NUSimKeyServerMonitorSeed
from .nusimkeyservermonitorsek import NUSimKeyServerMonitorSEK
from .nusiml2domain import NUSimL2Domain
from .nusiml2domaintemplate import NUSimL2DomainTemplate
from .nusiml4service import NUSimL4Service
from .nusiml4servicegroup import NUSimL4ServiceGroup
from .nusiml7applicationsignature import NUSimL7applicationsignature
from .nusimldapconfiguration import NUSimLDAPConfiguration
from .nusimlicense import NUSimLicense
from .nusimlicensestatus import NUSimLicenseStatus
from .nusimlink import NUSimLink
from .nusimlocation import NUSimLocation
from .nusimlteinformation import NUSimLTEInformation
from .nusimltestatistics import NUSimLtestatistics
from .nusimme import NUSimMe
from .nusimmetadata import NUSimMetadata
from .nusimmirrordestination import NUSimMirrorDestination
from .nusimmonitoringport import NUSimMonitoringPort
from .nusimmonitorscope import NUSimMonitorscope
from .nusimmulticastchannelmap import NUSimMultiCastChannelMap
from .nusimmulticastlist import NUSimMultiCastList
from .nusimmulticastrange import NUSimMultiCastRange
from .nusimmultinicvport import NUSimMultiNICVPort
from .nusimnatmapentry import NUSimNATMapEntry
from .nusimnetworklayout import NUSimNetworkLayout
from .nusimnetworkmacrogroup import NUSimNetworkMacroGroup
from .nusimnetworkperformancebinding import NUSimNetworkPerformanceBinding
from .nusimnetworkperformancemeasurement import NUSimNetworkPerformanceMeasurement
from .nusimnexthop import NUSimNextHop
from .nusimnsgateway import NUSimNSGateway
from .nusimnsgatewaytemplate import NUSimNSGatewayTemplate
from .nusimnsggroup import NUSimNSGGroup
from .nusimnsginfo import NUSimNSGInfo
from .nusimnsgroutingpolicybinding import NUSimNSGRoutingPolicyBinding
from .nusimnsgupgradeprofile import NUSimNSGUpgradeProfile
from .nusimnsport import NUSimNSPort
from .nusimnsporttemplate import NUSimNSPortTemplate
from .nusimnsredundantgatewaygroup import NUSimNSRedundantGatewayGroup
from .nusimospfarea import NUSimOSPFArea
from .nusimospfinstance import NUSimOSPFInstance
from .nusimospfinterface import NUSimOSPFInterface
from .nusimoverlayaddresspool import NUSimOverlayAddressPool
from .nusimoverlaymirrordestination import NUSimOverlayMirrorDestination
from .nusimoverlaymirrordestinationtemplate import NUSimOverlayMirrorDestinationTemplate
from .nusimoverlaypatnatentry import NUSimOverlayPATNATEntry
from .nusimpatipentry import NUSimPATIPEntry
from .nusimpatmapper import NUSimPATMapper
from .nusimpatnatpool import NUSimPATNATPool
from .nusimperformancemonitor import NUSimPerformanceMonitor
from .nusimpermission import NUSimPermission
from .nusimpgexpression import NUSimPGExpression
from .nusimpgexpressiontemplate import NUSimPGExpressionTemplate
from .nusimpolicydecision import NUSimPolicyDecision
from .nusimpolicyentry import NUSimPolicyEntry
from .nusimpolicygroup import NUSimPolicyGroup
from .nusimpolicygrouptemplate import NUSimPolicyGroupTemplate
from .nusimpolicyobjectgroup import NUSimPolicyObjectGroup
from .nusimpolicystatement import NUSimPolicyStatement
from .nusimport import NUSimPort
from .nusimportmapping import NUSimPortMapping
from .nusimporttemplate import NUSimPortTemplate
from .nusimproxyarpfilter import NUSimProxyARPFilter
from .nusimpsnatpool import NUSimPSNATPool
from .nusimpspatmap import NUSimPSPATMap
from .nusimptranslationmap import NUSimPTranslationMap
from .nusimpublicnetworkmacro import NUSimPublicNetworkMacro
from .nusimqos import NUSimQOS
from .nusimqospolicer import NUSimQosPolicer
from .nusimratelimiter import NUSimRateLimiter
from .nusimredirectiontarget import NUSimRedirectionTarget
from .nusimredirectiontargettemplate import NUSimRedirectionTargetTemplate
from .nusimredundancygroup import NUSimRedundancyGroup
from .nusimredundantport import NUSimRedundantPort
from .nusimroutingpolicy import NUSimRoutingPolicy
from .nusimsharednetworkresource import NUSimSharedNetworkResource
from .nusimsiteinfo import NUSimSiteInfo
from .nusimspatsourcespool import NUSimSPATSourcesPool
from .nusimsshkey import NUSimSSHKey
from .nusimssidconnection import NUSimSSIDConnection
from .nusimstaticroute import NUSimStaticRoute
from .nusimstatistics import NUSimStatistics
from .nusimstatisticspolicy import NUSimStatisticsPolicy
from .nusimstatscollectorinfo import NUSimStatsCollectorInfo
from .nusimsubnet import NUSimSubnet
from .nusimsubnettemplate import NUSimSubnetTemplate
from .nusimsystemconfig import NUSimSystemConfig
from .nusimtca import NUSimTCA
from .nusimtier import NUSimTier
from .nusimtrunk import NUSimTrunk
from .nusimunderlay import NUSimUnderlay
from .nusimuplinkconnection import NUSimUplinkConnection
from .nusimuplinkrd import NUSimUplinkRD
from .nusimuser import NUSimUser
from .nusimusercontext import NUSimUserContext
from .nusimvcenter import NUSimVCenter
from .nusimvcentercluster import NUSimVCenterCluster
from .nusimvcenterdatacenter import NUSimVCenterDataCenter
from .nusimvcentereamconfig import NUSimVCenterEAMConfig
from .nusimvcenterhypervisor import NUSimVCenterHypervisor
from .nusimvcentervrsconfig import NUSimVCenterVRSConfig
from .nusimvirtualfirewallpolicy import NUSimVirtualFirewallPolicy
from .nusimvirtualfirewallrule import NUSimVirtualFirewallRule
from .nusimvirtualip import NUSimVirtualIP
from .nusimvlan import NUSimVLAN
from .nusimvlantemplate import NUSimVLANTemplate
from .nusimvm import NUSimVM
from .nusimvminterface import NUSimVMInterface
from .nusimvmresync import NUSimVMResync
from .nusimvnf import NUSimVNF
from .nusimvnfcatalog import NUSimVNFCatalog
from .nusimvnfdescriptor import NUSimVNFDescriptor
from .nusimvnfdomainmapping import NUSimVNFDomainMapping
from .nusimvnfinterface import NUSimVNFInterface
from .nusimvnfinterfacedescriptor import NUSimVNFInterfaceDescriptor
from .nusimvnfmetadata import NUSimVNFMetadata
from .nusimvnfthresholdpolicy import NUSimVNFThresholdPolicy
from .nusimvpnconnection import NUSimVPNConnection
from .nusimvport import NUSimVPort
from .nusimvportmirror import NUSimVPortMirror
from .nusimvrs import NUSimVRS
from .nusimvrsaddressrange import NUSimVRSAddressRange
from .nusimvrsmetrics import NUSimVRSMetrics
from .nusimvrsredeploymentpolicy import NUSimVRSRedeploymentpolicy
from .nusimvsc import NUSimVSC
from .nusimvsd import NUSimVSD
from .nusimvsdcomponent import NUSimVSDComponent
from .nusimvsgredundantport import NUSimVsgRedundantPort
from .nusimvsp import NUSimVSP
from .nusimwanservice import NUSimWANService
from .nusimwirelessport import NUSimWirelessPort
from .nusimzfbautoassignment import NUSimZFBAutoAssignment
from .nusimzfbrequest import NUSimZFBRequest
from .nusimzone import NUSimZone
from .nusimzonetemplate import NUSimZoneTemplate

modules = glob.glob('{0:s}/*.py'.format(os.path.dirname(__file__)))
__all__ = [os.path.basename(f)[:-3] for f in modules]