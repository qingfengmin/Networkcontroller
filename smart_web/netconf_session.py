from ncclient import manager
from ncclient.xml_ import to_ele
from Configuring_the_database import generic as gen
import xml.etree.ElementTree as ET


class netconf_auto:
    def __init__(self, host):
        #构造函数，传入设备IP地址,基于ncclient库,使用netconf协议,将各种所需的参数封装在session字典中
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
        #用于获取netconf连接的私有方法,使用ncclient库的manager.connect方法,传入session字典,返回连接对象
        client = manager
        session = client.connect(**self.session, host=self.host)
        return session

    def display_config(self):
        #用于获取设备配置的方法,使用__get_netconf方法获取连接对象,调用get_config方法,传入source='running',返回配置对象,在后续开发上可能会用到
        client = self.__get_netconf()
        Brush = client.get_config(source='running')
        return Brush

    def display_config_filter(self, filter):
        #用于查看设备配置的方法,区别在于可以使用filter参数,传入filter参数,过滤用户所需的参数,返回配置对象,在后续开发上可能会用到
        filt = self.__get_netconf()
        Brush = filt.get_config(source='running', filter=filter)
        return Brush

    def display_config_get(self):
        #用于获取设备配置的方法,使用__get_netconf方法获取连接对象,调用get方法,返回配置对象,在后续开发上可能会用到
        client = self.__get_netconf()
        Brush = client.get()
        return Brush

    def display_config_get_filter(self, filter):
        #用于查看设备配置的方法,区别在于可以使用filter参数,传入filter参数,过滤用户所需的参数,返回配置对象,在后续开发上可能会用到
        filt = self.__get_netconf()
        Brush = filt.get(filter=filter)
        output = Brush.data_xml
        return output

    def dly_config(self, config_xml):
        #基于ncclient库的rpc方法,传入config_xml参数,返回配置对象,在后续开发上可能会用到,可以自定义XML
        dly = self.__get_netconf()
        output = dly.rpc(to_ele(config_xml))
        return output

    def dly_key(self, keys):
        #用于配置设备的方法,传入keys参数,返回配置对象,在后续开发上可能会用到,可以自定义XML,当前控制器的主要配置方式
        with  self.__get_netconf() as key:
            output = key.edit_config(target='running', config=keys)
        return output

    def get_interfaces(self):
        #可以获取设备的接口信息,返回一个字典,包含设备名称和接口映射,在sharing_data的get_device方法中被调用
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
        #基于get_interfaces方法的私有方法,用于解析XML,返回设备名称和接口映射,在get_interfaces方法中被调用
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

