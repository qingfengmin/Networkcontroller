from ncclient import manager
from ncclient.xml_ import to_ele
from Configuring_the_database import generic as gen
import xml.etree.ElementTree as ET


class netconf_auto:
    def __init__(self, host):
        self.host = host
        self.session = {
            'port': 830,
            'username': 'python',
            'password': 'Huawei@123',
            'hostkey_verify': False,
            'look_for_keys': False,
            'allow_agent': False,
            'device_params': {"name": "huawei"}
        }

    def __get_netconf(self):
        client = manager
        session = client.connect(**self.session, host=self.host)
        return session

    def display_config(self):
        client = self.__get_netconf()
        Brush = client.get_config(source='running')
        return Brush

    def display_config_filter(self, filter):
        filt = self.__get_netconf()
        Brush = filt.get_config(source='running', filter=filter)
        return Brush

    def display_config_get(self):
        client = self.__get_netconf()
        Brush = client.get()
        return Brush

    def display_config_get_filter(self, filter):
        filt = self.__get_netconf()
        Brush = filt.get(filter=filter)
        output = Brush.data_xml
        return output

    def dly_config(self, config_xml):
        dly = self.__get_netconf()
        output = dly.rpc(to_ele(config_xml))
        return output

    def dly_key(self, keys):
        with  self.__get_netconf() as key:
            output = key.edit_config(target='running', config=keys)
        return output

    def get_interfaces(self):
        filt = gen['lldp_filter']
        output = self.display_config_get_filter(filt)
        root = ET.fromstring(output)
        # 获取设备名称和接口映射
        device_name, interface_mapping = self.__parsing_xml(root)
        # 构建返回的字典
        result = {
            self.host: {
                'devices_name': device_name,
                'interface': interface_mapping
            }
        }
        return result

    def __parsing_xml(self, xml_data):
        ns = {'nc': 'urn:ietf:params:xml:ns:netconf:base:1.0', 'huawei': 'http://www.huawei.com/netconf/vrp'}
        sys_name = xml_data.find('.//huawei:lldp/huawei:lldpSys/huawei:lldpSysInformation/huawei:sysName', ns).text
        # 初始化接口映射字典
        interface_mapping = {}

        # 遍历所有 lldpInterface 元素
        for interface in xml_data.findall('.//huawei:lldpInterface', ns):
            if_name = interface.find('huawei:ifName', ns).text
            # 检查是否为 GE 接口
            if if_name.startswith('GE'):
                neighbors = interface.findall('huawei:lldpNeighbors/huawei:lldpNeighbor', ns)
                for neighbor in neighbors:
                    system_name = neighbor.find('huawei:systemName', ns).text
                    # 检查是否为 CE 设备
                    if system_name.startswith('CE'):
                        # 将 GE 接口与 CE 设备的映射关系添加到接口映射字典中
                        interface_mapping[if_name] = system_name
                        # 只取第一个匹配的 CE 设备，跳出内层循环
                        break

        return sys_name, interface_mapping

