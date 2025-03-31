import ipaddress

class config_data:
    def __init__(self):
        self.__default_ranges = {
            'vlan': list(range(1, 101)),
            'BD': list(range(1, 101)),
            'vni': list(range(1, 101))
        }
        # 这里保留的默认值作为 Loopback 端口网段
        self.default_network = '172.16.1.0'
        self.default_mask = '255.255.255.0'
        self.internet_segment = '10.1.100.0/24'
        self.prefix_length = 30
        self.connect_network = []


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

if __name__ == '__main__':
    meirui = config_data().subnetwork_partition()
    print(meirui)



