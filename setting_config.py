import ipaddress

class config_data:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__init__()
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):  # 防止重复初始化
            self.__default_ranges = {
                'vlan': list(range(1, 101)),
                'BD': list(range(1, 101)),
                'vni': list(range(1, 101))
            }
            self.default_network = '172.16.1.0'
            self.default_mask = '255.255.255.0'
            self.internet_segment = '10.1.100.0/24'
            self.prefix_length = 30
            self.connect_network = []
            self._initialized = True

    def update_config(self, **kwargs):
        """统一配置更新接口"""
        if 'vlan_range' in kwargs:
            self.__default_ranges['vlan'] = list(range(kwargs['vlan_range'][0], kwargs['vlan_range'][1]+1))
        if 'BD_range' in kwargs:
            self.__default_ranges['BD'] = list(range(kwargs['BD_range'][0], kwargs['BD_range'][1]+1))
        if 'vni_range' in kwargs:
            self.__default_ranges['vni'] = list(range(kwargs['vni_range'][0], kwargs['vni_range'][1]+1))
        if 'network' in kwargs:
            self.default_network = kwargs['network']
        if 'mask' in kwargs:
            self.default_mask = kwargs['mask']
        if 'internet_segment' in kwargs:
            self.internet_segment = kwargs['internet_segment']


    def __ip_address(self, network, mask):
        # 不提供默认值，强制用户指定
        try:
            network_str = f"{network}/{mask}"
            ip_network = ipaddress.IPv4Network(network_str, strict=False)
            ip_list = {str(ip): str(ip_network.netmask) for ip in ip_network.hosts()}
            # print(ip_list)
            return ip_list
        except ValueError as e:
            print(f"输入的网络地址或子网掩码无效: {e}")
            return []

    def __get_range(self, range_type, start=None, end=None):
        default_range = self.__default_ranges.get(range_type)
        if start is None or end is None:
            result_range = default_range
        else:
            result_range = list(range(int(start), int(end) + 1))
        return result_range

    def vlan(self, start_vlan=None, end_vlan=None):
        return self.__get_range('vlan', start_vlan, end_vlan)

    def BD(self, start_BD=None, end_BD=None):
        return self.__get_range('BD', start_BD, end_BD)

    def vni(self, start_vni=None, end_vni=None):
        return self.__get_range('vni', start_vni, end_vni)

    def loopback(self):
        return self.__ip_address(self.default_network, self.default_mask)

    def subnetwork_partition(self,network=None,mask=None):
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




