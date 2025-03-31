from setting_config import config_data as settings
from netconf_session import netconf_auto as nc
import random

class database:
    def __init__(self):
        self.Devices = {}
        self.__interface_infor = {}
        self.__hostlist = {}
        self.__loopback_network = list(settings().loopback().keys())

    def create_device(self, host, device_type):
        try:
            self.__hostlist[host] = device_type
            return self.__hostlist
        except ValueError as e:
            print(f"输入的网络地址或子网掩码无效: {e}")
            return []

    def delete_device(self, host):
        if host in self.__hostlist:
            del self.__hostlist[host]

    def init(self):
        for host in self.__hostlist:
            info = self.__neighbor(host)
            loopback_ip = random.choice(self.__loopback_network)
            self.Devices[host] = {
                'devices_name': info[host]['devices_name'],
                'loopback_ip': loopback_ip
            }
        self.Devices = self.__generate_vlan_config(self.__interface_infor)

    def __neighbor(self, host):
        device = nc(host).get_interfaces()
        self.__interface_infor.update(device)
        return device

    def __vlan_format(self,vlan_list):


    def __generate_vlan_config(self, lldp_info):
        vlan_range = settings().vlan()
        subnets = settings().subnetwork_partition()
        assigned_vlans = {}
        vlan_ip_networks = {}
        assigned_ips = set()
        vlan_config = {}

        for host_ip, info in lldp_info.items():
            interfaces = info['interface']
            vlan_config[host_ip] = {
                'devices_name': info['devices_name'],
                'loopback_ip': self.Devices.get(host_ip, {}).get('loopback_ip', ''),
                'interface': {},
                'vlanif': {}
            }

            for interface, neighbor_device in interfaces.items():
                neighbor_host = next((ip for ip, data in lldp_info.items() if data['devices_name'] == neighbor_device), None)
                link = tuple(sorted([(host_ip, interface), (neighbor_host, next(iface for iface, dev in lldp_info[neighbor_host]['interface'].items() if dev == info['devices_name']))]))

                vlan = assigned_vlans.get(link) or random.choice(vlan_range)
                assigned_vlans[link] = vlan
                vlan_config[host_ip]['interface'][interface] = vlan

                if vlan not in vlan_ip_networks:
                    if subnets:
                        vlan_ip_networks[vlan] = subnets.pop(0)
                    else:
                        print("没有可用的子网。")
                        continue

                ip_network = vlan_ip_networks.get(vlan)
                ip_generator = ip_network.hosts()
                ip = next((ip for ip in ip_generator if str(ip) not in assigned_ips), None)

                if not ip:
                    print(f"VLAN {vlan} 网段中没有可用的 IP 地址了。")
                    continue

                assigned_ips.add(str(ip))
                vlan_config[host_ip]['vlanif'][vlan] = str(ip)

        return vlan_config


if __name__ == '__main__':
    db = database()
    list1 = ['192.168.100.101', '192.168.100.102', '192.168.100.103']
    for i in list1:
        db.addDevice(i)
    db.init()
    print(db.Devices)
