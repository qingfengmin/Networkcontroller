import random

RT_before = [f'{i}' for i in range(0, 255)]
RT_head = random.choice(RT_before)
RT_tail = random.choice(RT_before)
AS_list = [f'{i}' for i in range(1, 65536)]
fixed_as = random.choice(AS_list)

class config:
    def __init__(self):
        self.vpn_RT = f'{RT_head}:{RT_tail}'
        self.vpn_RT1 = f'{RT_tail}:{RT_head}'
        self.RD = f'{random.choice(RT_head)}:{random.choice(RT_tail)}'

    def interface_addrsss(self, interface,network,mask):
        looback = f'''
	     <config>
       <ifm xmlns="http://www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0">
         <interfaces>
           <interface operation="merge">
             <ifName>{interface}</ifName>
			 <ifmAm4>
              <am4CfgAddrs>
                <am4CfgAddr operation="merge">
                  <subnetMask>{mask}</subnetMask>
                    <addrType>main</addrType>
                  <ifIpAddr>{network}</ifIpAddr>
                </am4CfgAddr>
              </am4CfgAddrs>
            </ifmAm4>
           </interface>
         </interfaces>
       </ifm>
     </config>
        '''
        return looback

    def ospf_Process(self, process, router_id, area_id):
        ospf = f'''
            <config>
      <ospfv2 xmlns="http://www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0">
        <ospfv2comm>
          <ospfSites>
            <ospfSite operation="merge">
              <processId>{process}</processId>
              <routerId>{router_id}</routerId>
              <vrfName>_public_</vrfName>
                <areas>
                <area operation="merge">
                  <areaId>{area_id}</areaId>
                  <areaType>Normal</areaType>
                </area>
              </areas>
            </ospfSite>
          </ospfSites>
        </ospfv2comm>
      </ospfv2>
    </config>'''
        return ospf

    def ospf_network(self, process, area_id, interface):
        ospf_interface = f'''
            <config>
      <ospfv2 xmlns="http://www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0">
        <ospfv2comm>
          <ospfSites>
            <ospfSite>
              <processId>{process}</processId>
              <areas>
                <area>
                  <areaId>{area_id}</areaId>
                  <interfaces>
                    <interface operation="merge">
                      <ifName>{interface}</ifName>
                      <networkType>broadcast</networkType>
                    </interface>
                  </interfaces>
                </area>
              </areas>
            </ospfSite>
          </ospfSites>
        </ospfv2comm>
      </ospfv2>
    </config>
'''
        return ospf_interface

    def vxlan_BD(self, bd_id, vni):
        vxlan_core = f'''
    <config>
      <evc xmlns="http://www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0">
        <bds>
          <bd operation="merge">
            <bdId>{bd_id}</bdId>
            <statistic>disable</statistic>
            <macLearn>enable</macLearn>
          </bd>
        </bds>
      </evc>
    </config>
'''
        bd_vni = f'''
    <config>
      <nvo3 xmlns="http://www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0">
        <nvo3Vni2Bds>
          <nvo3Vni2Bd operation="merge">
            <vniId>{vni}</vniId>
            <bdId>{bd_id}</bdId>
          </nvo3Vni2Bd>
        </nvo3Vni2Bds>
      </nvo3>
    </config>
'''
        vxlan = f'''
    <config>
      <nvo3 xmlns="http://www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0">
        <nvo3Nves>
          <nvo3Nve>
            <ifName>Nve1</ifName>
            <vniMembers>
              <vniMember operation="merge">
                <vniId>{vni}</vniId>
                <protocol>bgp</protocol>
              </vniMember>
            </vniMembers>
          </nvo3Nve>
        </nvo3Nves>
      </nvo3>
    </config>
'''
        return vxlan_core,bd_vni,vxlan

    def l3evpn(self, bd_id,RD,export_rt,import_rt):
        ex_RT = f'''
    <config>
      <evpn xmlns="http://www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0">
        <evpnInstances>
          <evpnInstance operation="merge">
            <evpnName>{bd_id}</evpnName>
            <bdId>{bd_id}</bdId>
            <evpnRD>{RD}</evpnRD>
			<evpnRTs>
              <evpnRT operation="merge">
                <vrfRTValue>{export_rt}</vrfRTValue>
                <vrfRTType>export_extcommunity</vrfRTType>
				<vrfRTValue>2:2</vrfRTValue>
                <vrfRTType>import_extcommunity</vrfRTType>
              </evpnRT>
            </evpnRTs>
          </evpnInstance>
        </evpnInstances>
      </evpn>
    </config>
'''
        im_rt = f'''
    <config>
      <evpn xmlns="http://www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0">
        <evpnInstances>
          <evpnInstance operation="merge">
            <evpnName>{bd_id}</evpnName>
            <bdId>{bd_id}</bdId>
            <evpnRD>{RD}</evpnRD>
			<evpnRTs>
              <evpnRT operation="merge">
				<vrfRTValue>{import_rt}</vrfRTValue>
                <vrfRTType>import_extcommunity</vrfRTType>
              </evpnRT>
            </evpnRTs>
          </evpnInstance>
        </evpnInstances>
      </evpn>
    </config>
'''

        return  ex_RT,im_rt

    def nve_source(self, address: str):
        nve = f'''
    <config>
      <nvo3 xmlns="http://www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0">
        <nvo3Nves>
          <nvo3Nve operation="merge">
            <ifName>Nve1</ifName>
            <nveType>mode-l2</nveType>
            <srcAddr>{address}</srcAddr>
          </nvo3Nve>
        </nvo3Nves>
      </nvo3>
    </config>
        '''
        return nve

    #
    def bgp(self,fixed_as,router_id):
        bgp_template = f'''
    <config>
      <bgp xmlns="http://www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0">
        <bgpcomm>
          <bgpSite operation="merge">
            <bgpEnable>true</bgpEnable>
            <asNumber>{fixed_as}</asNumber>
          </bgpSite>
          <bgpVrfs>
            <bgpVrf operation="merge">
              <vrfName>_public_</vrfName>
              <vrfRidAutoSel>false</vrfRidAutoSel>
              <routerId>{router_id}</routerId>
            </bgpVrf>
          </bgpVrfs>
        </bgpcomm>
      </bgp>
    </config>
        '''
        return bgp_template

    def bgp_neighbor(self, address,fixed_as, interface):
        bgp_neighbor = f'''
    <config>
      <bgp xmlns="http://www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0">
        <bgpcomm>
          <bgpVrfs>
            <bgpVrf>
              <vrfName>_public_</vrfName>
              <bgpPeers>
                <bgpPeer operation="merge">
                  <peerAddr>{address}</peerAddr>
                  <remoteAs>{fixed_as}</remoteAs>
				    <localIfName>{interface}</localIfName>
                </bgpPeer>
              </bgpPeers>
            </bgpVrf>
          </bgpVrfs>
        </bgpcomm>
      </bgp>
    </config>
        '''
        evpn = f'''
    <config>
      <bgp xmlns="http://www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0">
        <bgpcomm>
          <bgpVrfs>
            <bgpVrf>
              <vrfName>_public_</vrfName>
              <bgpVrfAFs>
                <bgpVrfAF operation="merge">
                  <afType>evpn</afType>
                  <policyVpnTarget>false</policyVpnTarget>
                  <peerAFs>
                    <peerAF operation="merge">
                      <remoteAddress>{address}</remoteAddress>
                      <advertiseArp>true</advertiseArp>
                      <allowAsLoopEnable>false</allowAsLoopEnable>
                    </peerAF>
                  </peerAFs>
                </bgpVrfAF>
              </bgpVrfAFs>
            </bgpVrf>
          </bgpVrfs>
        </bgpcomm>
      </bgp>
    </config>
     '''
        ipv4_un =   f'''
    <config>
      <bgp xmlns="http://www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0">
        <bgpcomm>
          <bgpVrfs>
            <bgpVrf>
              <vrfName>_public_</vrfName>
              <bgpVrfAFs>
                <bgpVrfAF>
                  <afType>ipv4uni</afType>
                  <peerAFs>
                    <peerAF operation="delete">
                      <remoteAddress>{address}</remoteAddress>
                    </peerAF>
                  </peerAFs>
                </bgpVrfAF>
              </bgpVrfAFs>
            </bgpVrf>
          </bgpVrfs>
        </bgpcomm>
      </bgp>
    </config>
        '''

        return bgp_neighbor,evpn,ipv4_un

    def create_vlan(self, vlanid):
        vlan = f'''
    <config>
      <vlan xmlns="http://www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0">
        <vlans>
          <vlan operation="merge">
            <vlanId>{vlanid}</vlanId>
            <vlanType>common</vlanType>
            <vlanif operation="merge">
              <cfgBand>1</cfgBand>
              <dampTime>0</dampTime>
            </vlanif>
          </vlan>
        </vlans>
      </vlan>
    </config>
        '''
        return vlan

    def GE_interface(self,inteface,vlanlist):
        GE = f'''
        <config>
       <ethernet xmlns="http://www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0">
         <ethernetIfs>
           <ethernetIf operation="merge">
             <ifName>{inteface}</ifName>
             <l2Enable>enable</l2Enable>
             <l2Attribute operation="merge">
               <linkType>trunk</linkType>
               <pvid>1</pvid>
			   <trunkVlans>{vlanlist}</trunkVlans>
             </l2Attribute>
           </ethernetIf>
         </ethernetIfs>
       </ethernet>
     </config>
'''
        return GE




generic = {'int_filter':'''
    <filter type="subtree">
      <ifm xmlns="http://www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0">
        <interfaces>
          <interface>
            <ifName></ifName>
            <ifPhyType/>
            <ifParentIfName/>
            <ifNumber/>
          </interface>
        </interfaces>
      </ifm>
    </filter>
''','lldp_enable':'''
    <config>
      <lldp xmlns="http://www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0">
        <lldpSys operation="merge">
          <lldpEnable>enabled</lldpEnable>
          <mdnStatus>disabled</mdnStatus>
        </lldpSys>
      </lldp>
    </config>
''','lldp_filter':'''
	<filter type="subtree">
      <lldp xmlns="http://www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0">
        <lldpSys>
          <lldpSysInformation>
            <sysName></sysName>
          </lldpSysInformation>
        </lldpSys>
        <lldpInterfaces>
          <lldpInterface>
            <lldpIfInformation>
              <portId></portId>
            </lldpIfInformation>
			<lldpNeighbors>
              <lldpNeighbor>
				<systemName></systemName>
              </lldpNeighbor>
            </lldpNeighbors>
          </lldpInterface>
        </lldpInterfaces>
      </lldp>
    </filter>
''','evpn_overlay':'''
	<config>
      <evn xmlns="http://www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0">
        <evnGlobal operation="merge">
          <evpnOverLay>true</evpnOverLay>
        </evnGlobal>
      </evn>
    </config>
''','nve1':'''
    <config>
       <ifm xmlns="http://www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0">
         <interfaces>
           <interface operation="merge">
             <ifName>Nve1</ifName>
           </interface>
         </interfaces>
       </ifm>
    </config>
'''}

