import ipaddress
import xml.etree.ElementTree as ET
from random import choice
from Configuring_the_database import config, generic, RT_before
from setting_config import config_data as setting

class ospf_auto:
    def __init__(self):
        self.xml_list = []
        self.up_GE_list = []
        self.up_LoopBack_list = []
        self.ns = {'ifm':'http://www.huawei.com/netconf/vrp'}
        self.ip_list = {}
        self.vlan = list(setting().vlan())
        self.loopback_network = list(setting().loopback().keys())
        self.loopback_mask = list(setting().loopback().values())

    def __get_interface_num(self, xml_data):
        for interface in ET.fromstring(xml_data).findall('.//ifm:interface', self.ns):
            if_name, if_status = interface.find('ifm:ifName', self.ns).text, interface.find('.//ifm:ifOperStatus', self.ns).text
            if if_status == 'up':
                (self.up_GE_list if if_name.startswith('GE') else self.up_LoopBack_list).append(if_name)
        return self.up_GE_list, self.up_LoopBack_list

    def __add_xml(self, xml_content):
        self.xml_list.append(xml_content)

    def __get_vlan_config(self, address, mask):
        try:
            vlan_id = choice(self.vlan)
            return [config().create_vlan(vlan_id), config().interface_addrsss(f'vlanif{vlan_id}', address, mask)]
        except ValueError as e:
            print(f"输入的网络地址或子网掩码无效: {e}")
            return []

    def ospf_config(self, process, area_id):
        self.__add_xml(generic['lldp_enable'])
        loopback_ip = choice(self.loopback_network)
        self.__add_xml(config().interface_addrsss(loopback_ip, f'LoopBack{choice(RT_before)}', choice(self.loopback_mask)))
        self.__add_xml(str((config().ospf_Process(process, loopback_ip, area_id))))
        all_config_copy = self.xml_list.copy()
        self.xml_list.clear()
        return all_config_copy

    # def ospf_area(self,process,):
    
if __name__ == '__main__':
    # ospf_auto()
    meirui = ospf_auto().ospf_config('1','0.0.0.1')
    for i in meirui:
        print(i)
        # print(meirui)