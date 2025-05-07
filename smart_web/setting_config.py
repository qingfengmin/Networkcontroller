import ipaddress
from reabase import reamysql
from read_files import readfile as rf

class config_data:
    def __init__(self):
        if not hasattr(self, '_initialized'):  # 防止重复初始化
            self.default_network = '172.16.1.0'
            self.default_mask = '255.255.255.0'
            self.sql = reamysql()

            self.receive_id = rf().reslist['resource']
            #读取配置文件中的资源ID,用于读取数据库中的信息
            self.internet_segment = self.sql.read(self.receive_id,'ip_address').decode('utf-8')
            self.prefix_length = self.sql.read(self.receive_id,'ip_mask')
            self.connect_network = []
            self._initialized = True

    def __get_range(self,start,end):
        #在上个版本中整个代码还需要指定类型才可以调取数据,如今可以直接获取MYSQL数据中的信息即可
        result_range = list(range(int(start), int(end) + 1))
        return result_range

    def vlan(self):
        vlan_start = self.sql.read(self.receive_id, 'vlan_before')
        vlan_end = self.sql.read(self.receive_id, 'vlan_after')
        print(vlan_start,vlan_end)
        return self.__get_range( vlan_start, vlan_end)

    def BD(self):
        BD_start = self.sql.read(self.receive_id, 'BD_before')
        BD_end = self.sql.read(self.receive_id, 'BD_after')
        return self.__get_range(BD_start , BD_end)

    def vni(self):
        vni_start = self.sql.read(self.receive_id, 'vni_before')
        vni_end = self.sql.read(self.receive_id, 'vni_after')
        return self.__get_range( vni_start , vni_end)

    def loopback(self):
        return self.__ip_address(self.default_network, self.default_mask)

    def __ip_address(self, network, mask):
        # 不提供默认值，强制用户指定,这个隐藏函数抓马呢用于为环回口分配IP地址
        try:
            network_str = f"{network}/{mask}"
            ip_network = ipaddress.IPv4Network(network_str, strict=False)
            ip_list = {str(ip): str(ip_network.netmask) for ip in ip_network.hosts()}
            # print(ip_list)
            return ip_list
        except ValueError as e:
            print(f"输入的网络地址或子网掩码无效: {e}")
            return []

    def subnetwork_partition(self,network=None,mask=None):
        #被用于划分网络地址,可以指定网络地址和子网掩码,如果不指定,则使用默认值,返回一个列表,包含所有的子网地址
        if network is None or mask is None:
            network_str = f"{self.internet_segment}"
        else:
            network_str = f"{network}"
        try:
            ip_network = ipaddress.IPv4Network(network_str, strict=False)
            subnets = list(ip_network.subnets(new_prefix=self.prefix_length))
            self.connect_network = subnets
            return self.connect_network
        except ValueError as e:
            print(f"输入的网络地址或子网掩码无效: {e}")
            return []

    # def update_config(self, **kwargs):
    #     #整个函数放在最后面因为暂时用不上,但是然后需要为程序更新可以用上
    #     if 'vlan_range' in kwargs:
    #         self.__default_ranges['vlan'] = list(range(kwargs['vlan_range'], kwargs['vlan_range'][1]+1))
    #     if 'BD_range' in kwargs:
    #         self.__default_ranges['BD'] = list(range(kwargs['BD_range'][0], kwargs['BD_range'][1]+1))
    #     if 'vni_range' in kwargs:
    #         self.__default_ranges['vni'] = list(range(kwargs['vni_range'][0], kwargs['vni_range'][1]+1))
    #     if 'network' in kwargs:
    #         self.default_network = kwargs['network']
    #     if 'mask' in kwargs:
    #         self.default_mask = kwargs['mask']
    #     if 'internet_segment' in kwargs:
    #         self.internet_segment = kwargs['internet_segment']



