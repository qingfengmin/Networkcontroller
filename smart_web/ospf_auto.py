import ipaddress
import xml.etree.ElementTree as ET
from random import choice

from Configuring_the_database import config, generic, RT_before


class ospf_auto:
    def __init__(self):
        # 初始化一个空列表来存储 XML 内容
        self.xml_list = []
        self.up_GE_list = []
        self.up_LoopBack_list = []
        self.ns = {'ifm':'http://www.huawei.com/netconf/vrp'}
        self.ip_list = {}

    def __get_interface_num(self,xml_data):
        # 去除字符串开头和结尾的空白字符
        root = ET.fromstring(xml_data)

        for interface in root.findall('.//ifm:interface', self.ns):
            if_name = interface.find('ifm:ifName', self.ns).text
            if_status = interface.find('.//ifm:ifOperStatus', self.ns).text

            if if_status == 'up':
                if if_name.startswith('GE'):
                    self.up_GE_list.append(if_name)
                elif if_name.startswith('LoopBack'):
                    self.up_LoopBack_list.append(if_name)
        return self.up_GE_list, self.up_LoopBack_list

    def ip_address(self,network='172.16.1.0',mask='255.255.255.0'):
        try:
            # 组合网络地址和子网掩码
            network_str = f"{network}/{mask}"
            # 创建 IPv4 网络对象
            ip_network = ipaddress.IPv4Network(network_str, strict=False)
            # 生成网段下的所有 IP 地址
            ip_list = {str(ip):str(ip_network.netmask) for ip in ip_network.hosts()}
            print(ip_list)
            return ip_list
        except ValueError as e:
            print(f"输入的网络地址或子网掩码无效: {e}")
            return []

    def __add_xml(self, xml_content):
        self.xml_list.append(xml_content)

    # def get_vlan_config(self,vlan_id=choice(vlan_list),address,mask):
    #     vlan_config1 = config().create_vlan(vlan_id)
    #     vlanif_address = config().interface_addrsss(f'vlanif{vlan_id}',address,mask)


    def ospf_config(self,process,area_id):
        self.__add_xml(generic['lldp_enable'])
        loopback_ip = choice(list(self.ip_list.keys()))
        print(loopback_ip)
        loopback_id = f'LoopBack{choice(RT_before)}'
        loopback_config = config().interface_addrsss(loopback_ip,loopback_id,'255.255.255.255')
        self.__add_xml(loopback_config)
        ospf_View = config().ospf_Process(process,loopback_ip,area_id)
        self.__add_xml(ospf_View)
