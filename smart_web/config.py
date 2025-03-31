from ncclient import manager

# 修改为字符串
Template = '''
    <filter type="subtree">
      <ethernet xmlns="http://www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0">
        <ethernetIfs>
          <ethernetIf>
            <ifName>GE1/0/4</ifName>
            <l2Attribute>
              <linkType></linkType>
              <pvid></pvid>
              <trunkVlans></trunkVlans>
            </l2Attribute>
          </ethernetIf>
        </ethernetIfs>
      </ethernet>
    </filter>
'''

num = '''
5020000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000080000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000:5020000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000080000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
'''
template1 = f'''
    <config>
       <ethernet xmlns="http://www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0">
         <ethernetIfs>
           <ethernetIf>
             <ifName>GE1/0/2</ifName>
             <l2Attribute operation="merge">
               <linkType>trunk</linkType>
			   <trunkVlans>{num}</trunkVlans>
			</l2Attribute>
           </ethernetIf>
         </ethernetIfs>
       </ethernet>
     </config>
'''

rpc1 = '''
<execute-action xmlns="http://www.huawei.com/netconf/capability/base/1.0">
<action>
<vlan xmlns="http://www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0">
    <shVlanBatchCrt>
        <vlans></vlans>
    </shVlanBatchCrt>
</vlan>
</action>
</execute-action>
'''


with manager.connect(host='192.168.100.101', port=830, username='python',
                         password='Huawei@123',
                     hostkey_verify=False, look_for_keys=False,
                     allow_agent=False, device_params={'name': 'huawei'}) as m:

    # for i in template1:
        response = m.edit_config(target='running',config=template1)
        # response = m.get_config(source='running',filter=i)
        # response = m.get_config(source='running')
        # response = m.rpc(to_ele(rpc1))
        # response = m.get(filter=Template)
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