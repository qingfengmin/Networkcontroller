from ncclient import manager

# 修改为字符串
Template = '''
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
'''
template1 = '''
    <config>
      <nvo3 xmlns="http://www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0">
        <nvo3Nves>
          <nvo3Nve>+
            <ifName>Nve1</ifName>
            <vniMembers>
              <vniMember operation="merge">
                <vniId>10</vniId>
                <protocol>bgp</protocol>
              </vniMember>
            </vniMembers>
          </nvo3Nve>
        </nvo3Nves>
      </nvo3>
    </config>
''','''
    <config>
      <bgp xmlns="http://www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0">
        <bgpcomm>
          <bgpSite operation="merge">
            <bgpEnable>true</bgpEnable>
            <asNumber>100</asNumber>
          </bgpSite>
          <bgpVrfs>
            <bgpVrf operation="merge">
              <vrfName>_public_</vrfName>
              <vrfRidAutoSel>false</vrfRidAutoSel>
              <routerId>172.16.1.1</routerId>
            </bgpVrf>
          </bgpVrfs>
        </bgpcomm>
      </bgp>
    </config>
''','''
    <config>
      <bgp xmlns="http://www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0">
        <bgpcomm>
          <bgpVrfs>
            <bgpVrf>
              <vrfName>_public_</vrfName>
              <bgpPeers>
                <bgpPeer operation="merge">
                  <peerAddr>172.16.1.2</peerAddr>
                  <remoteAs>100</remoteAs>
				    <localIfName>LoopBack0</localIfName>
                </bgpPeer>
              </bgpPeers>
            </bgpVrf>
          </bgpVrfs>
        </bgpcomm>
      </bgp>
    </config>
''','''
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
                      <remoteAddress>172.16.1.2</remoteAddress>
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
''','''
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
                      <remoteAddress>172.16.1.2</remoteAddress>
                    </peerAF>
                  </peerAFs>
                </bgpVrfAF>
              </bgpVrfAFs>
            </bgpVrf>
          </bgpVrfs>
        </bgpcomm>
      </bgp>
    </config>
''','''
	     <config>
       <ifm xmlns="http://www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0">
         <interfaces>
           <interface operation="merge">
             <ifName>vlanif300</ifName>
			 <ifmAm4>
              <am4CfgAddrs>
                <am4CfgAddr operation="merge">
                  <subnetMask>255.255.255.0</subnetMask>
                  <addrType>main</addrType>
                  <ifIpAddr>192.168.3.254</ifIpAddr>
                </am4CfgAddr>
              </am4CfgAddrs>
            </ifmAm4>
           </interface>
         </interfaces>
       </ifm>
     </config>
'''

rpc1 = '''
<execute-action xmlns="http://www.huawei.com/netconf/capability/base/1.0">
<action>
<vlan xmlns="http://www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0">
    <shVlanBatchCrt>
        <vlans>0000000000000000000000000000000000000000000000000000000000000000000000000008000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000:0000000000000000000000000000000000000000000000000000000000000000000000000008000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000</vlans>
    </shVlanBatchCrt>
</vlan>
</action>
</execute-action>
'''


with manager.connect(host='172.16.1.1', port=830, username='python',
                         password='Huawei@123',
                     hostkey_verify=False, look_for_keys=False,
                     allow_agent=False, device_params={'name': 'huawei'}) as m:

    for i in range(0,1):
        # response = m.edit_config(target='running',config=i)
        # response = m.get_config(source='running',filter=i)
        # response = m.get_config(source='running')
        # response = m.rpc(to_ele(rpc1))
        response = m.get(filter=Template)
        print(response)
    # 打印 GE 和 LoopBack 接口号
    #     response_xml = response.strip()
    #
    #     # 解析 XML 数据
    #     root = ET.fromstring(response)
    #     # 定义命名空间
    #     ns = {'ifm': 'http://www.huawei.com/netconf/vrp'}
    #
    #     # 筛选出接口状态为 up 且接口类型为 GE 口和 Loopback 的接口
    #     up_ge_interfaces = []
    #     up_loopback_interfaces = []
    #
    #     for interface in root.findall('.//ifm:interface', ns):
    #         if_name = interface.find('ifm:ifName', ns).text
    #         if_status = interface.find('.//ifm:ifOperStatus', ns).text
    #
    #         if if_status == 'up':
    #             if if_name.startswith('GE'):
    #                 up_ge_interfaces.append(if_name)
    #             elif if_name.startswith('LoopBack'):
    #                 up_loopback_interfaces.append(if_name)
    #
    #     # 打印结果
    #     print("接口状态为 UP 的 GE 接口:")
    #     for ge_if in up_ge_interfaces:
    #         print(ge_if)
    #
    #     print("\n接口状态为 UP 的 Loopback 接口:")
    #     for loopback_if in up_loopback_interfaces:
    #         print(loopback_if)